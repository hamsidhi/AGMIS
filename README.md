# AGMIS — Academic Guidance & Intelligence System

**Final Year B.Sc Data Science · Atharva College, Malad**

AGMIS turns routine academic data into an **intelligent, predictive, and actionable** guidance system so faculty and students can spot problems 4–6 weeks before critical exams.

## What It Does

- **Classify** current performance into 5 levels: Excellent / Good / Average / At Risk / Critical (Random Forest).
- **Predict** next exam score (e.g. CEM-2) with a confidence range (regression model).
- **Guide** with rule-based, specific advice (e.g. “Improve attendance to 85%+ to gain ~8 marks”).
- **Dashboards** for faculty (batch analytics, at-risk list, upload) and students (performance, prediction, guidance).

## Product Definition (from PRD)

> *"AGMIS analyzes academic data to classify where a student stands today, predict where they are heading in future exams, and guide them on what specific actions will improve outcomes — transparently and ethically."*

## Tech Stack

| Layer        | Technology                          |
|-------------|--------------------------------------|
| Frontend    | HTML, CSS, Jinja2 templates, Chart.js |
| Backend     | FastAPI (Python)                     |
| Database    | SQLite (local) / Supabase (optional) |
| ML          | scikit-learn (Random Forest, regression) |
| Auth        | Session/cookie (username + password) |

## Project Structure

```
agmis/
├── backend/
│   ├── app/
│   │   ├── api/           # API route modules (Supabase/optional)
│   │   ├── core/          # Config
│   │   ├── schemas/       # Pydantic models
│   │   ├── services/     # DB, features, classification, prediction, guidance
│   │   ├── static/       # CSS
│   │   ├── templates/    # Faculty & student dashboards, login
│   │   └── main.py       # App entry, routes, login, upload
│   ├── models/           # Saved ML models (.joblib)
│   ├── local.db          # SQLite DB (created on first run)
│   └── requirements.txt
├── DOCS/                 # PRD and other docs
├── README.md             # This file
└── PROJECT_STATUS.md     # PRD vs implementation status
```

## How to Run

1. **Clone and enter backend**
   ```bash
   cd agmis/backend
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```
   Add ML/data deps if needed:
   ```bash
   pip install pandas numpy scikit-learn joblib
   ```

3. **Run the app**
   ```bash
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
   Or:
   ```bash
   python -m app.main
   ```

4. **Open in browser**
   - Login: http://127.0.0.1:8000/
   - **Faculty**: e.g. `hiral` / `ml123` (subject: Machine Learning)
   - **Students**: After a faculty CSV upload, each student can log in with:
     - **Username** = `student_id` from the CSV (e.g. `101`, `202`)
     - **Password** = `1234` (set in `backend/app/services/database.py` in `save_faculty_data`)

## CSV Upload Format (Faculty)

Expected columns (names may vary; ensure mapping in code):

- `student_id`, `name`, `week`
- `lecture_present`, `lecture_total`, `practical_present`, `practical_total`
- `assignments_submitted`, `assignments_total`
- `internal_marks`, `external_marks`, `practical_marks`

The app computes percentages and runs the prediction pipeline on upload.

## Reference

- **PRD**: `New folder/DOCS/📘 ACADEMIC GUIDANCE & INTELLIGENCE SYSTEM (AGMIS) PRD.pdf`
- **Status vs PRD**: see [PROJECT_STATUS.md](PROJECT_STATUS.md).

## License & Use

Academic project. Do not use production credentials or real student PII in open repos.


one click start
1-cd E:\Projects\agmis\backend
.\venv\Scripts\Activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

2-cd E:\Projects\agmis\backend
.\venv\Scripts\Activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001