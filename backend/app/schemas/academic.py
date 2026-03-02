from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class AttendanceUpload(BaseModel):
    student_id: int
    subject_id: int
    date: date
    status: float = Field(..., ge=0, le=100, description="Attendance percentage 0-100")

class MarksUpload(BaseModel):
    student_id: int
    subject_id: int
    marks: float = Field(..., ge=0, le=100)
    category: str # 'internal' or 'exam'

class APIResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None