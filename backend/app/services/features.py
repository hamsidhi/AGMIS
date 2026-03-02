import pandas as pd
import numpy as np
from typing import List, Dict, Any

REQUIRED_CSV_COLUMNS = [
    "student_id", "name", "week",
    "lecture_present", "lecture_total",
    "practical_present", "practical_total",
    "assignments_submitted", "assignments_total",
    "internal_marks", "external_marks", "practical_marks",
]


def validate_csv_columns(df: pd.DataFrame) -> str | None:
    """Returns None if valid, else error message. Uses schema: student_id, name, week, lecture_*, practical_*, assignments_*, internal_marks, external_marks, practical_marks."""
    cols = set(c.strip().lower() for c in df.columns)
    required = set(c.lower() for c in REQUIRED_CSV_COLUMNS)
    missing = required - cols
    if missing:
        return (
            f"Missing required columns: {', '.join(sorted(missing))}. "
            f"This backend expects: student_id, name, week, lecture_present, lecture_total, practical_present, practical_total, "
            f"assignments_submitted, assignments_total, internal_marks, external_marks, practical_marks."
        )
    return None


class FeatureService:
    @staticmethod
    def calculate_weighted_score(
        attendance: float,
        internal_marks: float,
        assignments: float,
        exam: float = 0,
    ) -> float:
        score = (attendance * 0.20) + (internal_marks * 0.30) + (assignments * 0.20) + (exam * 0.30)
        return round(score, 2)

    @staticmethod
    def calculate_attendance_trend(weekly_attendance: List[float]) -> int:
        if len(weekly_attendance) < 2:
            return 0
        recent = weekly_attendance[-4:]
        x = np.arange(len(recent))
        y = np.array(recent)
        slope, _ = np.polyfit(x, y, 1)
        if slope < -2:
            return -1
        if slope > 2:
            return 1
        return 0

    @staticmethod
    def get_performance_category(score: float) -> str:
        if score >= 85:
            return "Excellent"
        if score >= 75:
            return "Good"
        if score >= 60:
            return "Average"
        if score >= 50:
            return "At Risk"
        return "Critical"

    def build_features(self, row: Any) -> List[float]:
        """
        Converts raw counts from CSV into percentages.
        Expects: lecture_present, lecture_total, practical_present, practical_total,
                 assignments_submitted, assignments_total, internal_marks, external_marks, practical_marks.
        """
        lec_total = float(row.get("lecture_total") or 0)
        prac_total = float(row.get("practical_total") or 0)
        assign_total = float(row.get("assignments_total") or 0)
        lec_pct = (float(row["lecture_present"]) / lec_total * 100) if lec_total > 0 else 0
        prac_pct = (float(row["practical_present"]) / prac_total * 100) if prac_total > 0 else 0
        assign_pct = (float(row["assignments_submitted"]) / assign_total * 100) if assign_total > 0 else 0
        return [
            round(lec_pct, 2),
            round(prac_pct, 2),
            round(assign_pct, 2),
            float(row.get("internal_marks", 0)),
            float(row.get("external_marks", 0)),
            float(row.get("practical_marks", 0)),
        ]

    def engineer_student_features(self, df_records: pd.DataFrame) -> Dict:
        if "attendance_theory" in df_records.columns and "attendance_practical" in df_records.columns:
            avg_attendance = df_records[["attendance_theory", "attendance_practical"]].mean().mean()
        else:
            avg_attendance = 0
        avg_internals = df_records["internal_marks"].mean() if "internal_marks" in df_records.columns else 0
        assignment_rate = df_records["assignment_score"].mean() if "assignment_score" in df_records.columns else 0
        trend = 0
        if "attendance_theory" in df_records.columns and len(df_records) >= 2:
            trend = self.calculate_attendance_trend(df_records["attendance_theory"].tolist())
        current_score = self.calculate_weighted_score(avg_attendance, avg_internals, assignment_rate)
        return {
            "attendance_pct": round(avg_attendance, 2),
            "internal_avg": round(avg_internals, 2),
            "assignment_rate": round(assignment_rate, 2),
            "attendance_trend": trend,
            "weighted_score": current_score,
            "performance_category": self.get_performance_category(current_score),
        }


feature_service = FeatureService()
