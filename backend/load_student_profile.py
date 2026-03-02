import csv
import os

from app.services.database import db_service


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "student_profile_v1.csv")
    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}")
        return

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = (row.get("student_id") or "").strip()
            if not sid:
                continue
            year_raw = (row.get("year") or "").strip()
            batch_raw = (row.get("batch") or "").strip()
            year_val = int(year_raw) if year_raw else None
            batch_val = batch_raw or None
            db_service.set_student_profile(sid, year_val, batch_val)

    print("student_profile_v1.csv loaded into student_profile table.")


if __name__ == "__main__":
    main()

