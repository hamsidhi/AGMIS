from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from app.schemas.academic import APIResponse
from supabase import create_client, Client
from app.core.config import settings
import csv
import io

router = APIRouter()
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

@router.get("/health")
async def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME}

@router.post("/upload/attendance", response_model=APIResponse)
async def upload_attendance(file: UploadFile = File(...)):
    """
    FR-1.1: Faculty uploads attendance via CSV
    Columns: student_id, subject_id, date, status
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload CSV.")

    contents = await file.read()
    decoded = contents.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))
    
    records = []
    for row in reader:
        try:
            records.append({
                "student_id": int(row['student_id']),
                "subject_id": int(row['subject_id']),
                "attendance_theory": float(row['status']),
                "record_date": row['date'],
                "week_number": 1 # Simplified for initial upload
            })
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Missing column: {str(e)}")

    # Bulk insert into Supabase
    data, count = supabase.table("academic_records").insert(records).execute()
    
    return {
        "status": "success", 
        "message": f"Successfully uploaded {len(records)} records"
    }

@router.get("/dashboard/student/{student_id}")
async def get_student_data(student_id: int):
    """
    4.1.2 Student - Data Consumer
    Fetches latest performance and predictions
    """
    # Fetch academic records
    records = supabase.table("academic_records")\
        .select("*")\
        .eq("student_id", student_id)\
        .execute()
    
    # Fetch latest prediction
    prediction = supabase.table("prediction_results")\
        .select("*")\
        .eq("student_id", student_id)\
        .order("prediction_date", desc=True)\
        .limit(1)\
        .execute()

    return {
        "records": records.data,
        "latest_prediction": prediction.data[0] if prediction.data else None
    }