from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import io, random
from app.services.database import db_service
from app.services.prediction import prediction_service
from app.services.features import feature_service

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/faculty/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    # Provide empty stats so the page doesn't crash on first load
    return templates.TemplateResponse("faculty_dashboard.html", {
        "request": request, 
        "students": [], 
        "stats": {"total": 0, "avg": 0, "at_risk": 0, "critical": 0},
        "banner": None
    })

@router.post("/faculty/upload", response_class=HTMLResponse)
async def upload_csv(request: Request, file: UploadFile = File(...)):
    df = pd.read_csv(io.BytesIO(await file.read()))
    
    processed_students = []
    total_score = 0
    at_risk_count = 0
    critical_count = 0
    
    for _, row in df.iterrows():
        # 1. Feature Engineering & Prediction
        feats = feature_service.build_features(row)
        pred = prediction_service.predict(feats)
        score = pred['predicted_score']
        cat = pred['predicted_category']
        
        # 2. Generate Random 4-digit PIN for Student
        pin = str(random.randint(1000, 9999))
        print(f"🔑 Student: {row['name']} | ID: {row['student_id']} | PIN: {pin}")

        # 3. Persistent Save to SQLite
        db_service.save_student_data(
            row['student_id'], row['name'], pin,
            feats[0], feats[2], feats[3], feats[1], feats[4], score, cat
        )
        
        # 4. Notification & Stats Logic
        s_id = row['student_id']
        row_class = ""
        if score < 50:
            db_service.add_notification(s_id, "Immediate intervention needed! Critical risk.", "red")
            critical_count += 1
            row_class = "row-critical"
        elif score < 60:
            db_service.add_notification(s_id, "Thoda focus karo yaar, you can do better!", "orange")
            at_risk_count += 1
            row_class = "row-risk"

        processed_students.append({
            "id": row['student_id'], "name": row['name'], "score": score,
            "cat": cat, "risk": "High" if score < 60 else "Low", "class": row_class
        })
        total_score += score

    # 5. Build the Stats box that the HTML is asking for
    stats = {
        "total": len(processed_students),
        "avg": round(total_score / len(processed_students), 1) if processed_students else 0,
        "at_risk": at_risk_count,
        "critical": critical_count
    }

    # 6. Banner logic
    banner_msg = "✅ Success: All records saved to local.db"
    banner_class = "alert-green"
    if critical_count > 0:
        banner_msg = "🚨 Warning: Critical students detected!"
        banner_class = "alert-red"

    return templates.TemplateResponse("faculty_dashboard.html", {
        "request": request, 
        "students": processed_students, 
        "stats": stats, 
        "banner": {"msg": banner_msg, "css": banner_class}
    })