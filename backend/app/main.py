from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import io
import os
import json
from datetime import datetime

import asyncio
from app.services.database import db_service
from app.services.prediction import predict_service
from app.services.features import feature_service, validate_csv_columns
from app.services.guidance import guidance_service
from app.services.emailer import emailer

# Paths relative to this file so the app works when run from E:\Projects\agmis\backend
_BASE_DIR = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
_STATIC_DIR = os.path.normpath(os.path.join(_BASE_DIR, "static"))
_TEMPLATES_DIR = os.path.normpath(os.path.join(_BASE_DIR, "templates"))

if not os.path.isdir(_STATIC_DIR):
    raise FileNotFoundError(f"Static directory not found: {_STATIC_DIR}")
if not os.path.isdir(_TEMPLATES_DIR):
    raise FileNotFoundError(f"Templates directory not found: {_TEMPLATES_DIR}")

app = FastAPI(title="AGMIS", description="Academic Guidance & Motivation Intelligence System")
app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")
templates = Jinja2Templates(directory=_TEMPLATES_DIR)
# Add tojson filter for Jinja2 (not built-in in FastAPI)
templates.env.filters["tojson"] = lambda v: json.dumps(v) if v is not None else "{}"


def _prd_distribution(students):
    """Build PRD 5-category counts from students (each has 'category')."""
    dist = {"excellent": 0, "good": 0, "average": 0, "at_risk": 0, "critical": 0}
    for s in students:
        # Convert to dict if it's a sqlite3.Row
        s_dict = dict(s) if not isinstance(s, dict) else s
        cat = (s_dict.get("category") or "Average").strip().lower().replace(" ", "_")
        if cat == "at_risk":
            dist["at_risk"] += 1
        elif cat in dist:
            dist[cat] += 1
        else:
            dist["average"] += 1
    return dist


@app.get("/health")
async def health():
    """Quick check - no matplotlib, no DB. Use to verify server is running."""
    return {"status": "ok", "message": "AGMIS is running"}


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request, error: int = 0):
    try:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": error},
        )
    except Exception as e:
        return HTMLResponse(
            f"<h1>AGMIS</h1><p>Template error: {e}</p><p><a href='/health'>Health</a></p>",
            status_code=500,
        )


@app.post("/login")
async def do_login(username: str = Form(...), password: str = Form(...)):
    with db_service.get_conn() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password),
        ).fetchone()
    
    if user:
        user = dict(user)
        # Check if first login is required (only for faculty and student)
        if user["role"] != "admin" and user.get("is_first_login") == 1:
            resp = RedirectResponse(url="/change-password", status_code=303)
            resp.set_cookie(key="temp_user_id", value=username) # Temp cookie for password change
            return resp

        if user["role"] == "admin":
            url = "/admin"
        elif user["role"] == "faculty":
            url = "/faculty/dashboard"
        else:
            url = "/student/dashboard"
        
        resp = RedirectResponse(url=url, status_code=303)
        resp.set_cookie(key="user_id", value=username, httponly=True, max_age=3600*24*7, path="/")
        db_service.add_audit_log(username, "LOGIN", f"Role: {user['role']}")
        return resp
    
    return RedirectResponse(url="/?error=1", status_code=303)


@app.get("/change-password", response_class=HTMLResponse)
async def change_password_page(request: Request):
    uname = request.cookies.get("temp_user_id")
    if not uname:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("change_password.html", {"request": request, "username": uname})


@app.post("/change-password")
async def do_change_password(request: Request, new_password: str = Form(...)):
    uname = request.cookies.get("temp_user_id")
    if not uname:
        return RedirectResponse(url="/")
    
    with db_service.get_conn() as conn:
        conn.execute(
            "UPDATE users SET password=?, is_first_login=0 WHERE username=?",
            (new_password, uname)
        )
    
    db_service.add_audit_log(uname, "PASSWORD_CHANGE", "Mandatory first-login password update")
    
    # After change, log them in normally
    user = db_service.get_user(uname)
    if not user:
        return RedirectResponse(url="/")
        
    if user["role"] == "faculty":
        url = "/faculty/dashboard"
    elif user["role"] == "admin":
        url = "/admin"
    else:
        url = "/student/dashboard"
    
    resp = RedirectResponse(url=url, status_code=303)
    resp.set_cookie(key="user_id", value=uname, httponly=True, max_age=3600*24*7, path="/")
    resp.delete_cookie("temp_user_id", path="/")
    return resp


@app.get("/logout")
async def logout():
    resp = RedirectResponse(url="/", status_code=303)
    resp.delete_cookie("user_id", path="/")
    return resp


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        admin_row = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
        if not admin_row or admin_row["role"] != "admin":
            return RedirectResponse(url="/")
        admin = dict(admin_row)

    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "admin": admin
        }
    )

@app.get("/admin/api/dashboard_stats")
async def admin_api_stats(request: Request):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        admin_row = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
        if not admin_row or admin_row["role"] != "admin":
            return JSONResponse({"error": "Unauthorized"}, status_code=403)
            
        total_faculty = conn.execute("SELECT COUNT(*) FROM users WHERE role='faculty' AND COALESCE(is_active, 1) = 1").fetchone()[0]
        total_students = conn.execute("SELECT COUNT(*) FROM users WHERE role='student' AND COALESCE(is_active, 1) = 1").fetchone()[0]
        total_subjects = conn.execute("SELECT COUNT(DISTINCT subject) FROM predictions").fetchone()[0]
        
        distribution = {
            "high_performer": 0,
            "stable": 0,
            "moderate_risk": 0,
            "high_risk": 0
        }
        students_risk = conn.execute("""
            SELECT risk_level FROM predictions p
            JOIN users u ON u.username = p.student_id
            WHERE u.role='student' AND COALESCE(u.is_active, 1) = 1
        """).fetchall()
        
        for row in students_risk:
            risk = row["risk_level"]
            if risk == "Low":
                distribution["stable"] += 1
            elif risk == "High":
                distribution["moderate_risk"] += 1
            elif risk == "Critical":
                distribution["high_risk"] += 1
            else:
                distribution["stable"] += 1

    return {
        "stats": {
            "faculty": total_faculty,
            "students": total_students,
            "subjects": total_subjects
        },
        "distribution": distribution
    }

@app.get("/admin/api/students")
async def admin_api_students(request: Request):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        admin_row = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
        if not admin_row or admin_row["role"] != "admin":
            return JSONResponse({"error": "Unauthorized"}, status_code=403)
    return db_service.get_all_students()

@app.get("/admin/api/faculty")
async def admin_api_faculty(request: Request):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        admin_row = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
        if not admin_row or admin_row["role"] != "admin":
            return JSONResponse({"error": "Unauthorized"}, status_code=403)
    return db_service.get_faculty_list()

@app.get("/admin/api/messages")
async def admin_api_messages(request: Request, subject_code: str = None, student_id: str = None, date_range_days: int = None):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        admin_row = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
        if not admin_row or admin_row["role"] != "admin":
            return JSONResponse({"error": "Unauthorized"}, status_code=403)
            
    msgs = db_service.get_all_messages(subject_code=subject_code, student_id=student_id, date_range_days=date_range_days)
    return msgs

@app.post("/admin/delete-faculty")
async def admin_api_delete_faculty(request: Request, username: str = Form(...)):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        admin_row = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
        if not admin_row or admin_row["role"] != "admin":
            return JSONResponse({"error": "Unauthorized"}, status_code=403)
    db_service.delete_user(username, uname)
    return JSONResponse({"status": "success"})

@app.post("/admin/update-faculty")
async def admin_api_update_faculty(
    request: Request,
    username: str = Form(...),
    name: str = Form(...),
    subject_name: str = Form(...),
    subject_code: str = Form(...)
):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        admin_row = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
        if not admin_row or admin_row["role"] != "admin":
            return JSONResponse({"error": "Unauthorized"}, status_code=403)
            
    with db_service.get_conn() as conn:
         conn.execute("UPDATE users SET name=?, subject_name=?, subject_code=? WHERE username=?", (name, subject_name, subject_code, username))
    db_service.add_audit_log(uname, "UPDATE_FACULTY", f"Updated faculty: {username}")
    return JSONResponse({"status": "success"})


@app.post("/admin/create-faculty")
async def create_faculty(
    request: Request,
    username: str = Form(...),
    name: str = Form(...),
    subject_name: str = Form(...),
    subject_code: str = Form(...),
    email: str = Form(None)
):
    # Auto-generate temporary password
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    temp_password = ''.join(secrets.choice(alphabet) for i in range(8))
    
    with db_service.get_conn() as conn:
        conn.execute(
            """INSERT INTO users (username, password, role, name, subject_name, subject_code, email, is_first_login, is_active)
               VALUES (?, ?, 'faculty', ?, ?, ?, ?, 1, 1)
               ON CONFLICT(username) DO UPDATE SET
               password=excluded.password,
               name=excluded.name,
               subject_name=excluded.subject_name,
               subject_code=excluded.subject_code,
               email=excluded.email,
               is_first_login=1,
               is_active=1""",
            (username, temp_password, name, subject_name, subject_code, email)
        )
    
    admin_id = request.cookies.get("user_id")
    db_service.add_audit_log(admin_id, "CREATE_FACULTY", f"Username: {username}, Subject: {subject_code}")
    
    return JSONResponse({
        "status": "success",
        "message": f"Faculty account created. Temp Password: {temp_password}",
        "temp_password": temp_password
    })


@app.post("/admin/reset-password")
async def reset_password(request: Request, username: str = Form(...)):
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    temp_password = ''.join(secrets.choice(alphabet) for i in range(8))
    
    with db_service.get_conn() as conn:
        conn.execute(
            "UPDATE users SET password=?, is_first_login=1 WHERE username=?",
            (temp_password, username)
        )
    
    admin_id = request.cookies.get("user_id")
    db_service.add_audit_log(admin_id, "RESET_PASSWORD", f"For user: {username}")
    
    return JSONResponse({
        "status": "success",
        "message": f"Password reset for {username}. New Temp Password: {temp_password}",
        "temp_password": temp_password
    })


@app.post("/admin/api/student/update")
async def admin_update_student(
    request: Request,
    username: str = Form(...),
    name: str = Form(...),
    year: str = Form(None),
    batch: str = Form(None)
):
    admin_id = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        conn.execute("UPDATE users SET name=? WHERE username=?", (name, username))
        conn.execute("REPLACE INTO student_profile (student_id, year, batch) VALUES (?, ?, ?)", (username, year, batch))
    db_service.add_audit_log(admin_id, "UPDATE_STUDENT", f"Updated student profile: {username}")
    return JSONResponse({"status": "success"})


@app.delete("/admin/api/student/{student_id}")
async def admin_delete_student(request: Request, student_id: str):
    admin_id = request.cookies.get("user_id")
    db_service.delete_user(student_id, "student")
    db_service.add_audit_log(admin_id, "DELETE_STUDENT", f"Soft-deleted student: {student_id}")
    return JSONResponse({"status": "success"})


@app.post("/admin/api/student/reset-password")
async def admin_reset_student_password(request: Request, username: str = Form(...)):
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    temp_password = ''.join(secrets.choice(alphabet) for i in range(8))
    
    with db_service.get_conn() as conn:
        conn.execute(
            "UPDATE users SET password=?, is_first_login=1 WHERE username=? AND role='student'",
            (temp_password, username)
        )
    
    admin_id = request.cookies.get("user_id")
    db_service.add_audit_log(admin_id, "RESET_STUDENT_PASSWORD", f"For student: {username}")
    
    return JSONResponse({
        "status": "success",
        "message": f"Password reset for {username}. New Temp Password: {temp_password}",
        "temp_password": temp_password
    })


@app.post("/api/notifications/add")
async def add_notification(
    request: Request,
    message: str = Form(...),
    subject_code: str = Form(None),
    n_type: str = Form('announcement')
):
    user_id = request.cookies.get("user_id")
    if not user_id: return JSONResponse({"status": "error"}, status_code=401)
    
    # Verify user is faculty or admin
    with db_service.get_conn() as conn:
        user = conn.execute("SELECT role FROM users WHERE username=?", (user_id,)).fetchone()
        if not user or user["role"] not in ['faculty', 'admin']:
            return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=403)
            
    db_service.add_notif(None, message, subject_code, n_type)
    return {"status": "success"}

import shutil
import os

UPLOAD_DIR = os.path.join("backend", "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/api/materials/{subject_code}")
async def get_materials(subject_code: str):
    return db_service.get_materials(subject_code)

@app.post("/api/materials/add")
async def add_material(
    request: Request,
    title: str = Form(...),
    type: str = Form(...), # pdf, docx, txt, pptx, video, link
    subject_code: str = Form(...),
    file: UploadFile = File(None),
    url: str = Form(None)
):
    faculty_id = request.cookies.get("user_id")
    if not faculty_id: return JSONResponse({"status": "error"}, status_code=401)
    
    final_url = url
    if file:
        # Structured directory per subject
        subj_dir = os.path.join(UPLOAD_DIR, subject_code)
        os.makedirs(subj_dir, exist_ok=True)
        
        file_path = os.path.join(subj_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        final_url = f"/static/uploads/{subject_code}/{file.filename}"
        
    try:
        db_service.add_material(subject_code, faculty_id, title, type, final_url)
        return {"status": "success"}
    except Exception as e:
        print(f"Error adding material: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.delete("/api/materials/{material_id}")
async def delete_material(request: Request, material_id: int):
    user_id = request.cookies.get("user_id")
    if not user_id: return JSONResponse({"status": "error"}, status_code=401)
    db_service.delete_material(material_id, user_id)
    return {"status": "success"}

@app.get("/api/events/{subject_code}")
async def get_events(subject_code: str):
    return db_service.get_calendar_events(subject_code)

@app.post("/api/events/add")
async def add_event(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    event_date: str = Form(...),
    event_type: str = Form(...),
    subject_code: str = Form(None)
):
    user_id = request.cookies.get("user_id")
    if not user_id: return JSONResponse({"status": "error"}, status_code=401)
    db_service.add_calendar_event(subject_code, title, description, event_date, event_type, user_id)
    return {"status": "success"}

@app.delete("/api/events/{event_id}")
async def delete_event(request: Request, event_id: int):
    user_id = request.cookies.get("user_id")
    if not user_id: return JSONResponse({"status": "error"}, status_code=401)
    db_service.delete_calendar_event(event_id, user_id)
    return {"status": "success"}

@app.get("/api/messages")
async def get_messages(request: Request, other_id: str = None, subject_code: str = None):
    user_id = request.cookies.get("user_id")
    if not user_id: return JSONResponse({"status": "error"}, status_code=401)
    
    with db_service.get_conn() as conn:
        user = conn.execute("SELECT role FROM users WHERE username=?", (user_id,)).fetchone()
        role = user["role"] if user else None
        
    return db_service.get_messages(user_id, role=role, other_id=other_id, subject_code=subject_code)

@app.post("/api/messages/send")
async def send_message(
    request: Request,
    receiver_id: str = Form(None),
    subject_code: str = Form(...),
    message: str = Form(...),
    tag: str = Form(None),
    parent_id: str = Form(None)
):
    sender_id = request.cookies.get("user_id")
    if not sender_id: return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=401)
    
    # Handle optional fields sent as empty strings
    receiver_id = receiver_id if receiver_id and receiver_id.strip() else None
    
    # Safely convert parent_id to int if present
    p_id = None
    if parent_id and parent_id.strip():
        try:
            p_id = int(parent_id)
        except (ValueError, TypeError):
            p_id = None
    
    # Inquiry Routing Logic
    if not receiver_id:
        if subject_code == "GLOBAL":
            receiver_id = None
        else:
            with db_service.get_conn() as conn:
                faculty = conn.execute(
                    "SELECT username, subject_code FROM users WHERE role='faculty' AND (subject_code=? OR subject_name=?)", 
                    (subject_code, subject_code)
                ).fetchone()
                if faculty:
                    receiver_id = faculty["username"]
                    # Force using the canonical subject_code from the faculty record
                    subject_code = faculty["subject_code"] or subject_code
                else:
                    return JSONResponse({"status": "error", "message": f"Faculty not found for subject: {subject_code}"}, status_code=404)
                
    try:
        db_service.send_message(sender_id, receiver_id, subject_code, message, tag=tag, parent_id=p_id)
        
        # Burnout Intelligence / Stress Signal
        if sender_id:
            user = db_service.get_user(sender_id)
            if user and user.get("role") == "student":
                keywords = ["confused", "fail", "understand", "stress", "anxious", "worried", "stuck", "overwhelmed"]
                has_keywords = any(kw in message.lower() for kw in keywords)
                
                with db_service.get_conn() as conn:
                    recent = conn.execute("SELECT COUNT(*) as c FROM messages WHERE sender_id=? AND sent_at > datetime('now', '-3 days')", (sender_id,)).fetchone()
                    msg_count = recent["c"] if recent else 0
                
                # If high frequency (>=5 in 3 days) or explicitly using stress keywords
                if has_keywords or msg_count >= 5:
                    alert_msg = f"Elevated Academic Stress Detected for {user['name']}. Multiple doubts or stress-related keywords used recently."
                    # Add alert for faculty
                    db_service.add_notif(None, alert_msg, subject_code=subject_code, n_type='alert')
                    # System note to the student acknowledging their struggle
                    db_service.add_notif(sender_id, "We noticed you've been working hard and might be feeling stressed. Don't hesitate to reach out for direct academic support.", subject_code=None, n_type='system')

        return {"status": "success"}
    except Exception as e:
        print(f"Error sending message: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.post("/api/messages/summarize")
async def summarize_messages(request: Request, subject_code: str = Form(...), other_id: str = Form(None)):
    user_id = request.cookies.get("user_id")
    if not user_id: return JSONResponse({"status": "error"}, status_code=401)
    
    with db_service.get_conn() as conn:
        user = conn.execute("SELECT role FROM users WHERE username=?", (user_id,)).fetchone()
        role = user["role"] if user else None
        
    msgs = db_service.get_messages(user_id, role=role, other_id=other_id, subject_code=subject_code)
    
    if len(msgs) == 0:
        return {"status": "success", "summary": "No messages to summarize."}
        
    # Heuristic summary
    tags = list(set([m.get("tag") for m in msgs if m.get("tag")]))
    tag_str = ", ".join(tags) if tags else "various topics"
    
    # Just grab the last few messages for context
    lines = []
    for m in reversed(msgs[:5]): # oldest first of the last 5
        sender = "Student" if str(m["sender_id"]) == str(other_id) else "Faculty/You"
        lines.append(f"{sender}: {m['message'][:50]}...")
        
    summary_text = f"Discussion primarily centered around {tag_str}. There were {len(msgs)} total messages in this thread.\n\nRecent context:\n" + "\n".join(lines)
    
    return {"status": "success", "summary": summary_text}

# ---------- Faculty dashboard (single route) ----------
@app.get("/faculty/dashboard", response_class=HTMLResponse)
async def faculty_dash(request: Request, year: int | None = None, batch: str | None = None):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        faculty_row = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
        if not faculty_row or faculty_row["role"] != "faculty":
            return RedirectResponse(url="/")
        faculty = dict(faculty_row)

        subj = faculty["subject_name"]
        base_sql = """
            SELECT p.*, u.name, sp.year, sp.batch
            FROM predictions p
            JOIN users u ON p.student_id = u.username
            LEFT JOIN student_profile sp ON sp.student_id = u.username
            WHERE p.subject=?
        """
        params = [subj]
        if year is not None:
            base_sql += " AND sp.year = ?"
            params.append(year)
        if batch:
            base_sql += " AND sp.batch = ?"
            params.append(batch)
        students = conn.execute(base_sql, params).fetchall()
        # Convert to list of dicts for template
        students = [dict(r) for r in students]
        
        # New: Get materials, events, and messages for dashboard
        materials = db_service.get_materials(faculty["subject_code"])
        events = db_service.get_calendar_events(faculty["subject_code"])
        messages = db_service.get_messages(uname, role='faculty', subject_code=faculty["subject_code"])
        
        # Populate sender names for the chat UI
        for m in messages:
            for field in ("sender_id", "receiver_id"):
                val = m.get(field)
                if val and str(val) != str(uname):
                    u_row = db_service.get_user(val)
                    m[field.replace("_id", "_name")] = u_row["name"] if u_row else val
                elif str(val) == str(uname):
                    m[field.replace("_id", "_name")] = "You"
                else:
                    m[field.replace("_id", "_name")] = "System/Global"
                    
        notifications = db_service.get_notifications(subject_codes=[faculty["subject_code"]])

    total = len(students)
    if total == 0:
        stats = {
            "total": 0,
            "avg_pred": 0,
            "at_risk_count": 0,
            "distribution": {"excellent": 0, "good": 0, "average": 0, "at_risk": 0, "critical": 0},
        }
        return templates.TemplateResponse(
            "faculty_dashboard.html",
            {
                "request": request,
                "faculty": faculty,
                "students": [],
                "stats": stats,
                "at_risk_students": [],
                "materials": materials,
                "events": events,
                "messages": messages,
                "notifications": notifications,
            },
        )

    distribution = _prd_distribution(students)
    avg_pred = round(sum(s["score"] for s in students) / total, 1)
    at_risk_count = len([s for s in students if s.get("risk_level") in ("High", "Critical")])
    at_risk_students = [
        {
            "student_id": s["student_id"],
            "name": s["name"],
            "current_cat": s.get("category") or "—",
            "pred_score": round(s["score"], 1),
            "risk_level": s.get("risk_level") or "—",
        }
        for s in students
        if s.get("risk_level") in ("High", "Critical")
    ]
    # Sort by predicted score ascending (highest risk first)
    at_risk_students.sort(key=lambda x: x["pred_score"])

    stats = {
        "total": total,
        "avg_pred": avg_pred,
        "at_risk_count": at_risk_count,
        "distribution": distribution,
    }

    return templates.TemplateResponse(
        "faculty_dashboard.html",
        {
            "request": request,
            "faculty": faculty,
            "students": students,
            "stats": stats,
            "at_risk_students": at_risk_students,
            "materials": materials,
            "events": events,
            "messages": messages,
            "notifications": notifications,
        },
    )


# Directory for generated credential CSVs (relative to backend folder when running from backend)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
STUDENT_PASSWORD = "1234"


@app.post("/faculty/upload")
async def upload(request: Request, year: int = Form(...), batch: str = Form(...), file: UploadFile = File(...)):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        faculty = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
    if not faculty:
        return JSONResponse({"status": "error", "message": "Not logged in"}, status_code=401)

    subj = faculty["subject_name"] or "Subject"
    try:
        raw = await file.read()
        df = pd.read_csv(io.BytesIO(raw))
        df.columns = [str(c).strip().lower() for c in df.columns]
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=400)

    err = validate_csv_columns(df)
    if err:
        return JSONResponse({"status": "error", "message": err}, status_code=400)

    credentials_rows = []
    count = 0
    for _, row in df.iterrows():
        row = row.to_dict()
        s_id = str(row.get("student_id", "")).strip()
        name = str(row.get("name", "")).strip()
        week = int(row.get("week", 0))
        if not s_id or not name:
            continue
        try:
            metrics = feature_service.build_features(row)
        except (KeyError, TypeError, ValueError) as e:
            return JSONResponse({"status": "error", "message": f"Invalid row (student_id={s_id}): {e}"}, status_code=400)
        w = db_service.get_weights_for_subject(subj) or {"subject": subj, "w_lec": 0.20, "w_prac": 0.10, "w_assign": 0.10, "w_internal": 0.20, "w_external": 0.40}
        
        hist_records = db_service.get_historical_records(s_id, subj)
        hist_scores = []
        for hr in hist_records:
            hr_metrics = [hr["lec_pct"] or 0, hr["prac_pct"] or 0, hr["assign_pct"] or 0, hr["internal"] or 0, hr["external"] or 0, hr["prac_marks"] or 0]
            hist_scores.append(predict_service.calculate_base_score(hr_metrics, w))
            
        with db_service.get_conn() as conn_d:
            d_row = conn_d.execute("SELECT COUNT(*) as c FROM messages WHERE sender_id=? AND subject_code=? AND tag IS NOT NULL", (s_id, faculty["subject_code"])).fetchone()
            doubt_intensity = d_row["c"] if d_row else 0
            
        pred = predict_service.predict_subject_score(metrics, weights=w, historical_scores=hist_scores, doubt_intensity=doubt_intensity)
        
        # This will create/update the user with role='student' and is_first_login=1
        db_service.save_faculty_data(s_id, name, subj, week, metrics, pred)
        db_service.set_student_profile(s_id, year, batch)
        lec_pct, prac_pct, assign_pct, internal, external, prac_marks = metrics
        student_data = {
            "attendance": (lec_pct + prac_pct) / 2,
            "internal_marks": internal,
            "submission_rate": assign_pct,
            "predicted_score": pred["score"],
            "attendance_trend": 0,
            "external_marks": external,
            "practical_marks": prac_marks,
            "lecture_pct": lec_pct,
            "practical_pct": prac_pct,
            "assignments_submitted": int(row.get("assignments_submitted", 0)),
            "assignments_total": int(row.get("assignments_total", 1)) or 1,
            "total_external": 75,
            "total_internal": 20,
        }
        guidance_list = guidance_service.generate_guidance(student_data)
        for g in guidance_list:
            db_service.add_notif(s_id, g["observation"], subj)
        if pred["score"] < 50 and emailer.is_configured():
            user_row = db_service.get_user(s_id)
            to_email = user_row.get("email") if user_row else None
            if to_email:
                emailer.send_email(
                    to_email,
                    f"Critical Risk Alert: {subj}",
                    f"Dear {name},\n\nYour predicted score in {subj} is {pred['score']:.1f}, which is in the critical range.\nPlease improve attendance, submit assignments, and prepare for internals.\n\nRegards,\nAGMIS",
                )
        credentials_rows.append({"name": name, "student_id": s_id, "password": STUDENT_PASSWORD})
        count += 1

    # Write credentials CSV: name, student_id, password
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_subj = "".join(c if c.isalnum() or c in " -_" else "_" for c in subj).strip() or "batch"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"student_credentials_{safe_subj}_{timestamp}.csv"
    csv_path = os.path.join(OUTPUT_DIR, csv_filename)
    cred_df = pd.DataFrame(credentials_rows)
    cred_df.to_csv(csv_path, index=False)

    db_service.add_audit_log(uname, "UPLOAD_CSV", f"Subject: {subj}, Records: {count}")

    return JSONResponse({
        "status": "success",
        "message": f"Uploaded {count} records.",
        "credentials_file": csv_filename,
    })


@app.post("/faculty/student/manual-entry")
async def add_or_update_student(
    request: Request,
    student_id: str = Form(...),
    name: str = Form(...),
    week: int = Form(...),
    lec_pct: float = Form(0.0),
    prac_pct: float = Form(0.0),
    assign_pct: float = Form(0.0),
    internal: float = Form(0.0),
    external: float = Form(0.0),
    prac_marks: float = Form(0.0)
):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        faculty = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
    if not faculty or faculty["role"] != "faculty":
        return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=401)
    
    subj = faculty["subject_name"]
    metrics = [lec_pct, prac_pct, assign_pct, internal, external, prac_marks]
    w = db_service.get_weights_for_subject(subj) or {"subject": subj, "w_lec": 0.20, "w_prac": 0.10, "w_assign": 0.10, "w_internal": 0.20, "w_external": 0.40}
    
    hist_records = db_service.get_historical_records(student_id, subj)
    hist_scores = []
    for hr in hist_records:
        hr_metrics = [hr["lec_pct"] or 0, hr["prac_pct"] or 0, hr["assign_pct"] or 0, hr["internal"] or 0, hr["external"] or 0, hr["prac_marks"] or 0]
        hist_scores.append(predict_service.calculate_base_score(hr_metrics, w))
        
    with db_service.get_conn() as conn_d:
        d_row = conn_d.execute("SELECT COUNT(*) as c FROM messages WHERE sender_id=? AND subject_code=? AND tag IS NOT NULL", (student_id, faculty["subject_code"])).fetchone()
        doubt_intensity = d_row["c"] if d_row else 0
        
    pred = predict_service.predict_subject_score(metrics, weights=w, historical_scores=hist_scores, doubt_intensity=doubt_intensity)
    
    db_service.save_faculty_data(student_id, name, subj, week, metrics, pred)
    # Give a default batch/year to allow it to show up on dashboard unfiltered
    try:
        db_service.set_student_profile(student_id, 1, "A")
    except: pass
    
    db_service.add_audit_log(uname, "MANUAL_STUDENT_ENTRY", f"Student: {student_id}")
    return JSONResponse({"status": "success", "message": "Student data saved successfully."})


@app.delete("/faculty/student/{student_id}")
async def delete_student(request: Request, student_id: str):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        faculty = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
    if not faculty or faculty["role"] != "faculty":
        return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=401)
        
    subj = faculty["subject_name"]
    with db_service.get_conn() as conn:
        conn.execute("DELETE FROM records WHERE student_id=? AND subject=?", (student_id, subj))
        conn.execute("DELETE FROM predictions WHERE student_id=? AND subject=?", (student_id, subj))
        
    db_service.add_audit_log(uname, "DELETE_STUDENT", f"Student: {student_id}")
    return JSONResponse({"status": "success", "message": "Student deleted."})


@app.post("/faculty/student/reset-password")
async def faculty_reset_student_password(request: Request, student_id: str = Form(...)):
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        faculty = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
    if not faculty or faculty["role"] != "faculty":
        return JSONResponse({"status": "error", "message": "Unauthorized"}, status_code=401)
        
    subj = faculty["subject_name"]
    # Verify student belongs to this faculty's subject
    with db_service.get_conn() as conn:
        record = conn.execute("SELECT * FROM predictions WHERE student_id=? AND subject=?", (student_id, subj)).fetchone()
        if not record:
            return JSONResponse({"status": "error", "message": "Student not found in your subject"}, status_code=404)
            
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    temp_password = ''.join(secrets.choice(alphabet) for i in range(8))
    
    with db_service.get_conn() as conn:
        conn.execute(
            "UPDATE users SET password=?, is_first_login=1 WHERE username=? AND role='student'",
            (temp_password, student_id)
        )
        
    db_service.add_audit_log(uname, "FACULTY_RESET_STUDENT_PASSWORD", f"For student: {student_id}")
    
    return JSONResponse({
        "status": "success",
        "message": f"Password reset for {student_id}. New Temp Password: {temp_password}",
        "temp_password": temp_password
    })


@app.get("/faculty/student/{student_id}", response_class=HTMLResponse)
async def faculty_student_view(request: Request, student_id: str):
    """Faculty view of an individual student's data: history, current, future prediction."""
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        faculty_row = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
        if not faculty_row:
            return RedirectResponse(url="/")
        faculty = dict(faculty_row)
        
        subj = faculty["subject_name"]
        if not subj:
            row = conn.execute(
                "SELECT subject FROM predictions WHERE student_id=? ORDER BY ROWID DESC LIMIT 1",
                (student_id,),
            ).fetchone()
            if row and row["subject"]:
                subj = row["subject"]
                faculty["subject_name"] = subj
        
        user_row = conn.execute("SELECT * FROM users WHERE username=?", (student_id,)).fetchone()
        if not user_row:
            return RedirectResponse(url="/faculty/dashboard", status_code=303)
        user = dict(user_row)
        
        records_rows = conn.execute(
            "SELECT * FROM records WHERE student_id=? AND subject=? ORDER BY week",
            (student_id, subj),
        ).fetchall()
        preds_rows = conn.execute(
            "SELECT * FROM predictions WHERE student_id=? AND subject=?",
            (student_id, subj),
        ).fetchall()
        all_preds_rows = conn.execute(
            "SELECT student_id, score FROM predictions WHERE subject=? ORDER BY score DESC",
            (subj,),
        ).fetchall()
    
    records = [dict(r) for r in records_rows]
    preds = [dict(p) for p in preds_rows]
    all_preds = [dict(p) for p in all_preds_rows]
    
    last_pred = preds[0] if preds else None
    last_record = records[-1] if records else None

    if last_record:
        lec = last_record.get("lec_pct") or 0
        prac = last_record.get("prac_pct") or 0
        assign = last_record.get("assign_pct") or 0
        internal = last_record.get("internal") or 0
        external = last_record.get("external") or 0
        weighted_score = round(
            (lec * 0.2 + prac * 0.1 + assign * 0.1 + (internal / 20) * 100 * 0.2 + (external / 75) * 100 * 0.4),
            1,
        )
    else:
        weighted_score = round(last_pred["score"], 1) if last_pred else 0

    performance = {"category": (last_pred and last_pred.get("category")) or "Average", "weighted_score": weighted_score}
    prediction = {
        "score": round(last_pred["score"], 1) if last_pred else 0,
        "mae": 5,
        "confidence": 85,
        "expected_cat": (last_pred and last_pred.get("category")) or "—",
    }
    
    if last_record:
        att = ((last_record.get("lec_pct") or 0) + (last_record.get("prac_pct") or 0)) / 2
        internal_raw = last_record.get("internal") or 0
        internal_marks_pct = internal_raw / 20 * 100
        submission = last_record.get("assign_pct") or 0
        lec = last_record.get("lec_pct") or 0
        prac = last_record.get("prac_pct") or 0
        external_raw = last_record.get("external") or 0
        prac_marks_raw = last_record.get("prac_marks") or 0
    else:
        att = internal_raw = internal_marks_pct = submission = 0
        lec = prac = external_raw = prac_marks_raw = 0
    
    weekly_att = [((r.get("lec_pct") or 0) + (r.get("prac_pct") or 0)) / 2 for r in records]
    trend = feature_service.calculate_attendance_trend(weekly_att) if len(weekly_att) >= 2 else 0
    
    rank_in_batch = None
    for i, p in enumerate(all_preds):
        if str(p["student_id"]) == str(student_id):
            rank_in_batch = i + 1
            break
            
    student_data = {
        "attendance": att,
        "internal_marks": internal_raw,
        "submission_rate": submission,
        "predicted_score": last_pred["score"] if last_pred else 0,
        "attendance_trend": trend,
        "external_marks": external_raw,
        "practical_marks": prac_marks_raw,
        "lecture_pct": lec,
        "practical_pct": prac,
        "assignments_submitted": 0 if submission == 0 else 1,
        "assignments_total": 1,
        "total_external": 75,
        "total_internal": 20,
        "rank_in_batch": rank_in_batch,
    }
    guidance = guidance_service.generate_guidance(student_data)

    weeks = [r["week"] for r in records]
    actual_scores = []
    for r in records:
        lec_val = r.get("lec_pct") or 0
        prac_val = r.get("prac_pct") or 0
        assign_val = r.get("assign_pct") or 0
        int_val = (r.get("internal") or 0) / 20 * 100
        ext_val = (r.get("external") or 0) / 75 * 100
        sc_val = lec_val * 0.2 + prac_val * 0.1 + assign_val * 0.1 + int_val * 0.2 + ext_val * 0.4
        actual_scores.append(round(sc_val, 1))
    
    pred_score = round(last_pred["score"], 1) if last_pred else 0
    if weeks:
        last_w = weeks[-1]
        trend_weeks = [f"W{w}" for w in weeks] + [f"W{last_w + i}(P)" for i in range(1, 5)]
        
        last_actual = actual_scores[-1] if actual_scores else 0
        diff = pred_score - last_actual
        smooth_steps = [0.4, 0.7, 0.9, 1.0]
        future_path = [round(last_actual + diff * step, 1) for step in smooth_steps]
        
        predicted_path = actual_scores + future_path
    else:
        trend_weeks = ["Current", "Predicted"]
        actual_scores = [weighted_score]
        predicted_path = [weighted_score, pred_score]

    return templates.TemplateResponse(
        "faculty_student_view.html",
        {
            "request": request,
            "faculty": faculty,
            "user": {"name": user["name"], "student_id": student_id},
            "performance": performance,
            "prediction": prediction,
            "guidance": guidance,
            "chart_data": {
                "trend_weeks": trend_weeks,
                "actual_scores": actual_scores,
                "predicted_path": predicted_path,
                "metrics": [round(att, 1), round(submission, 1), round(internal_marks_pct, 1)]
            }
        },
    )

# ---------- Faculty operations ----------
@app.get("/faculty/export-credentials")
async def export_credentials(request: Request):
    """Download CSV with name, student_id, password for all students in faculty's subject."""
    uname = request.cookies.get("user_id")
    with db_service.get_conn() as conn:
        faculty = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
    if not faculty:
        return RedirectResponse(url="/", status_code=303)
    subj = faculty["subject_name"]
    students = db_service.get_students_with_credentials_for_subject(subj)
    if not students:
        return JSONResponse(
            {"status": "error", "message": "No students in this batch. Upload data first."},
            status_code=400,
        )
    df = pd.DataFrame(students)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    csv_content = buffer.getvalue()
    safe_subj = "".join(c if c.isalnum() or c in " -_" else "_" for c in subj).strip() or "batch"
    filename = f"student_credentials_{safe_subj}.csv"
    return StreamingResponse(
        iter([csv_content.encode("utf-8")]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/faculty/download-template/{subject_code}")
async def download_template(subject_code: str):
    """Return a template CSV with headers and an example row for faculty upload."""
    headers = [
        "student_id", "name", "week",
        "lecture_present", "lecture_total",
        "practical_present", "practical_total",
        "assignments_submitted", "assignments_total",
        "internal_marks", "external_marks", "practical_marks"
    ]
    # Example data row
    example = [
        "1001", "Student Name", "1",
        "8", "10", "4", "5",
        "1", "1", "15", "60", "25"
    ]
    
    df = pd.DataFrame([example], columns=headers)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    csv_content = buffer.getvalue()
    
    filename = f"template_{subject_code.replace(' ', '_')}.csv"
    return StreamingResponse(
        iter([csv_content.encode("utf-8")]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ---------- Student dashboard ----------
@app.get("/student/dashboard", response_class=HTMLResponse)
@app.get("/admin/student/{student_id}", response_class=HTMLResponse)
async def student_dash(request: Request, subject_idx: int | None = None, student_id: str = None):
    uname = request.cookies.get("user_id")
    if not uname:
        return RedirectResponse(url="/")
        
    with db_service.get_conn() as conn:
        viewer = conn.execute("SELECT * FROM users WHERE username=?", (uname,)).fetchone()
        if not viewer or viewer["role"] not in ["student", "admin"]:
            return RedirectResponse(url="/")
            
        role = viewer["role"]
        is_admin = (role == "admin")
        s_id = student_id if (is_admin and student_id) else uname
        
        user_row = conn.execute("SELECT * FROM users WHERE username=?", (s_id,)).fetchone()
        if not user_row or user_row["role"] != "student":
            return RedirectResponse(url="/")
        user = dict(user_row)

        preds = conn.execute("SELECT * FROM predictions WHERE student_id=?", (s_id,)).fetchall()
        notifs = conn.execute("SELECT * FROM notifications WHERE student_id=?", (s_id,)).fetchall()
        
        # New: Get student-specific events, materials, and messages
        # Map subject names to codes for notification query
        subj_names = [p["subject"] for p in preds]
        with db_service.get_conn() as conn_map:
            # Get unique subject codes for all current subjects
            if subj_names:
                placeholders = ', '.join(['?'] * len(subj_names))
                mapped_codes = conn_map.execute(
                    f"SELECT subject_code FROM users WHERE role='faculty' AND subject_name IN ({placeholders})",
                    subj_names
                ).fetchall()
                current_subj_codes = [r["subject_code"] for r in mapped_codes if r["subject_code"]]
            else:
                current_subj_codes = []
                
        notifications = db_service.get_notifications(student_id=s_id, subject_codes=current_subj_codes)
        events = db_service.get_calendar_events(include_global=True)
        materials = db_service.get_materials() 
        messages = db_service.get_messages(s_id, role='student')
        
        with db_service.get_conn() as conn_map:
            code_map = conn_map.execute("SELECT subject_code, subject_name FROM users WHERE role='faculty'").fetchall()
            code_to_name = {r["subject_code"]: r["subject_name"] for r in code_map if r["subject_code"]}
            
        for m in messages:
            if m["subject_code"] and m["subject_code"] != 'GLOBAL':
                m["subject_code"] = code_to_name.get(m["subject_code"], m["subject_code"])

        records = conn.execute(
            "SELECT * FROM records WHERE student_id=? ORDER BY week",
            (s_id,),
        ).fetchall()
    preds = [dict(p) for p in preds]
    notifs = [dict(n) for n in notifs]
    records = [dict(r) for r in records]

    if not preds:
        empty_performance = {"category": "Average", "weighted_score": 0}
        empty_prediction = {"score": 0, "mae": 0, "confidence": 0, "expected_cat": "—"}
        return templates.TemplateResponse(
            "student_dashboard.html",
            {
                "request": request,
                "is_admin": is_admin,
                "user": {"name": user["name"], "batch": "—", "department": "—"},
                "overall": None,
                "subjects": [],
                "subject_idx": None,
                "notifs": [],
                "performance": empty_performance,
                "prediction": empty_prediction,
                "guidance": [],
                "trend_chart_b64": "",
                "metrics_pie_b64": "",
                "current_vs_target_b64": "",
                "materials": materials,
                "events": events,
                "messages": messages,
                "notifications": notifications,
            },
        )

    subjects = {}
    for r in records:
        key = r.get("subject") or "Overall"
        if key in ("Unknown", "Overall"): continue # Clean architecture: filter out legacy mock subjects
        subjects.setdefault(key, {"records": [], "preds": [], "notifs": []})
        subjects[key]["records"].append(r)
    for p in preds:
        key = p.get("subject") or "Overall"
        if key in ("Unknown", "Overall"): continue
        subjects.setdefault(key, {"records": [], "preds": [], "notifs": []})
        subjects[key]["preds"].append(p)
    for n in notifs:
        key = n.get("subject") or "Overall"
        if key in ("Unknown", "Overall"): continue
        subjects.setdefault(key, {"records": [], "preds": [], "notifs": []})
        subjects[key]["notifs"].append(n)

    subject_cards = []
    overall_scores = []
    all_guidance = []

    for subj, data in subjects.items():
        spreds = data["preds"]
        srecords = data["records"]
        snotifs = data["notifs"]
        last_pred = spreds[0] if spreds else None
        last_record = srecords[-1] if srecords else None
        if last_record:
            lec = last_record.get("lec_pct") or 0
            prac = last_record.get("prac_pct") or 0
            assign = last_record.get("assign_pct") or 0
            internal = last_record.get("internal") or 0
            external = last_record.get("external") or 0
            weighted_score = round(
                (lec * 0.2 + prac * 0.1 + assign * 0.1 + (internal / 20) * 100 * 0.2 + (external / 75) * 100 * 0.4),
                1,
            )
        else:
            weighted_score = round(last_pred["score"], 1) if last_pred else 0
        performance = {
            "category": (last_pred and last_pred.get("category")) or "Average",
            "weighted_score": weighted_score,
        }
        prediction = {
            "score": round(last_pred["score"], 1) if last_pred else 0,
            "mae": 5,
            "confidence": 85,
            "expected_cat": (last_pred and last_pred.get("category")) or "—",
        }
        if last_record:
            att = ((last_record.get("lec_pct") or 0) + (last_record.get("prac_pct") or 0)) / 2
            internal_raw = last_record.get("internal") or 0
            submission = last_record.get("assign_pct") or 0
            lec = last_record.get("lec_pct") or 0
            prac = last_record.get("prac_pct") or 0
            external_raw = last_record.get("external") or 0
            prac_marks_raw = last_record.get("prac_marks") or 0
        else:
            att = internal_raw = submission = 0
            lec = prac = external_raw = prac_marks_raw = 0
        internal_marks_pct = (internal_raw / 20 * 100) if internal_raw else 0
        weekly_att = [((r.get("lec_pct") or 0) + (r.get("prac_pct") or 0)) / 2 for r in srecords]
        trend = feature_service.calculate_attendance_trend(weekly_att) if len(weekly_att) >= 2 else 0
        rank_in_batch = None
        if last_pred and last_pred.get("subject"):
            subj_code = last_pred["subject"]
            with db_service.get_conn() as conn:
                all_preds = conn.execute(
                    "SELECT student_id, score FROM predictions WHERE subject=? ORDER BY score DESC",
                    (subj_code,),
                ).fetchall()
            for i, p in enumerate(all_preds):
                if str(p["student_id"]) == str(s_id):
                    rank_in_batch = i + 1
                    break
        student_data = {
            "attendance": att,
            "internal_marks": internal_raw,
            "submission_rate": submission,
            "predicted_score": last_pred["score"] if last_pred else 0,
            "attendance_trend": trend,
            "external_marks": external_raw,
            "practical_marks": prac_marks_raw,
            "lecture_pct": lec,
            "practical_pct": prac,
            "assignments_submitted": 0 if submission == 0 else 1,
            "assignments_total": 1,
            "total_external": 75,
            "total_internal": 20,
            "rank_in_batch": rank_in_batch,
        }
        guidance = guidance_service.generate_guidance(student_data)
        weeks = [r["week"] for r in srecords]
        actual_scores = []
        for r in srecords:
            lec_val = r.get("lec_pct") or 0
            prac_val = r.get("prac_pct") or 0
            assign_val = r.get("assign_pct") or 0
            int_val = (r.get("internal") or 0) / 20 * 100
            ext_val = (r.get("external") or 0) / 75 * 100
            sc = lec_val * 0.2 + prac_val * 0.1 + assign_val * 0.1 + int_val * 0.2 + ext_val * 0.4
            actual_scores.append(round(sc, 1))
        pred_score = round(last_pred["score"], 1) if last_pred else 0
        if weeks:
            last_w = weeks[-1]
            trend_weeks = [f"W{w}" for w in weeks] + [f"W{last_w + i}(P)" for i in range(1, 5)]
            
            last_actual = actual_scores[-1] if actual_scores else 0
            diff = pred_score - last_actual
            smooth_steps = [0.4, 0.7, 0.9, 1.0]
            future_path = [round(last_actual + diff * step, 1) for step in smooth_steps]
            
            predicted_path = actual_scores + future_path
        else:
            trend_weeks = ["Current", "Predicted"]
            actual_scores = [weighted_score]
            predicted_path = [weighted_score, pred_score]

        subject_cards.append(
            {
                "subject": subj,
                "performance": performance,
                "prediction": prediction,
                "guidance": guidance,
                "notifs": snotifs,
                "chart_data": {
                    "trend_weeks": trend_weeks,
                    "actual_scores": actual_scores,
                    "predicted_path": predicted_path,
                    "metrics": [round(att, 1), round(submission, 1), round(internal_marks_pct, 1)]
                }
            }
        )
        if prediction["score"]:
            overall_scores.append(prediction["score"])
        all_guidance.extend(guidance)

    overall_score = round(sum(overall_scores) / len(overall_scores), 1) if overall_scores else 0

    if not subject_cards:
        empty_performance = {"category": "Average", "weighted_score": 0}
        empty_prediction = {"score": 0, "mae": 0, "confidence": 0, "expected_cat": "—"}
        return templates.TemplateResponse(
            "student_dashboard.html",
            {
                "request": request,
                "user": {"name": user["name"], "batch": "—", "department": "—"},
                "overall": None,
                "subjects": [],
                "subject_idx": None,
                "notifs": [],
                "performance": empty_performance,
                "prediction": empty_prediction,
                "guidance": [],
                "chart_data": {
                    "trend_weeks": [],
                    "actual_scores": [],
                    "predicted_path": [],
                    "metrics": [0,0,0]
                },
                "materials": materials,
                "events": events,
                "messages": messages,
                "notifications": notifications,
            },
        )

    if subject_idx is not None and 0 <= subject_idx < len(subject_cards):
        main_card = subject_cards[subject_idx]
        use_overall = False
    else:
        main_card = subject_cards[0]
        use_overall = True

    if use_overall:
        cats_rank = {"excellent": 0, "good": 1, "average": 2, "at risk": 3, "critical": 4}
        worst_cat = None
        worst_rank = -1
        total_weighted = 0.0
        for c in subject_cards:
            cat = str(c["performance"]["category"] or "Average")
            key = cat.strip().lower()
            rank = cats_rank.get(key, 2)
            if rank > worst_rank:
                worst_rank = rank
                worst_cat = cat
            total_weighted += float(c["performance"]["weighted_score"] or 0)
        avg_weighted = round(total_weighted / len(subject_cards), 1) if subject_cards else 0
        performance = {"category": worst_cat or "Average", "weighted_score": avg_weighted}
        prediction = {
            "score": overall_score,
            "mae": 5,
            "confidence": 85,
            "expected_cat": worst_cat or "—",
        }
        guidance = all_guidance
        notifs_for_view = notifs
    else:
        performance = main_card["performance"]
        prediction = main_card["prediction"]
        guidance = main_card["guidance"]
        notifs_for_view = main_card["notifs"]

    if use_overall:
        # Show all relevant notifications, events, and materials for overall view
        filtered_notifications = notifications
        filtered_events = events
        filtered_materials = materials
        filtered_messages = messages
    else:
        # Filter specifically for the selected subject
        current_subj_name = main_card["subject"]
        with db_service.get_conn() as conn_code:
            f_row = conn_code.execute("SELECT subject_code FROM users WHERE role='faculty' AND subject_name=?", (current_subj_name,)).fetchone()
            current_subj_code = f_row["subject_code"] if f_row else current_subj_name

        filtered_notifications = [n for n in notifications if n["subject_code"] == current_subj_code or n["subject_code"] is None]
        filtered_events = [e for e in events if e["subject_code"] == current_subj_code or e["subject_code"] is None]
        filtered_materials = [m for m in materials if m["subject_code"] == current_subj_code]
        
    filtered_messages = messages

    return templates.TemplateResponse(
        "student_dashboard.html",
        {
            "request": request,
            "is_admin": is_admin,
            "user": {"name": user["name"], "batch": "—", "department": "—"},
            "overall": {"score": overall_score},
            "subjects": subject_cards,
            "subject_idx": subject_idx,
            "notifs": notifs_for_view,
            "performance": performance,
            "prediction": prediction,
            "guidance": guidance,
            "chart_data": main_card["chart_data"],
            "materials": filtered_materials,
            "events": filtered_events,
            "messages": filtered_messages,
            "notifications": filtered_notifications,
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
