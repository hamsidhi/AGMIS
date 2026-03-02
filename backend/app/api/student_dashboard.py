from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.database import db_service

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/student/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/student/login")
async def do_login(response: Response, username: int = Form(...), password: str = Form(...)):
    conn = db_service.get_connection()
    user = conn.execute("SELECT * FROM students WHERE id = ? AND password = ?", (username, password)).fetchone()
    if user:
        resp = RedirectResponse(url="/student/dashboard", status_code=303)
        resp.set_cookie(key="student_id", value=str(username))
        return resp
    return HTMLResponse("Invalid Credentials. <a href='/student/login'>Try again</a>")

@router.get("/student/dashboard", response_class=HTMLResponse)
async def student_dash(request: Request):
    s_id = request.cookies.get("student_id")
    if not s_id: return RedirectResponse(url="/student/login")
    
    conn = db_service.get_connection()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (s_id,)).fetchone()
    record = conn.execute("SELECT * FROM records WHERE student_id = ?", (s_id,)).fetchone()
    notifs = conn.execute("SELECT * FROM notifications WHERE student_id = ?", (s_id,)).fetchall()
    
    return templates.TemplateResponse("student_dashboard.html", {
        "request": request, "student": student, "record": record, "notifs": notifs
    })