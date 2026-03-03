# AGMIS — Academic Guidance, Motivation & Intelligence System

**Final Year B.Sc Data Science · Atharva College, Malad**

AGMIS is an advanced, intelligence-driven academic platform designed to transform regular student data into predictive, actionable guidance. It allows faculty and administrators to monitor student performance in real-time and predict future exam scores, addressing potential drop-outs or failures 4-6 weeks before critical examinations occur.



## 🌟 Core Features

AGMIS provides three distinct levels of access and functionality:

### 1. Student Dossiers (Student View)
- **Predictive Scoring**: Uses a trained Random Forest and Regression ML models to predict upcoming exam scores based on historical attendance, assignments, and exam performance.
- **Risk Classification**: Classifies students into distinct risk profiles: Critical, High Risk, Moderate, and High Performer.
- **Personalized Actionable Guidance**: Generates rule-based, specific advice tailored to the student (e.g., “Improve attendance to 85%+ to gain ~8 marks”).
- **Direct Faculty Communication**: Students can securely ask questions and seek doubt clarifications from their dedicated subject faculty.

### 2. Faculty Command Center (Faculty View)
- **Batch Analytics & Insights**: A holistic view of the assigned class, dynamically plotting the predictive performance distribution.
- **At-Risk Identification**: Readily identifiable flags pinpoint students classified as "Critical" or "High Risk," focusing intervention efforts where they matter most.
- **Doubt Management System**: Faculty can review and directly answer specific doubts and queries raised by students under their purview, featuring full chat history and summarization.
- **Student Management**: Faculty can directly manage their students, including the ability to reset compromised student passwords securely.
- **Data Integration**: Easy drag-and-drop CSV upload for ingesting new attendance and marks data, automatically updating predictions on the fly.

### 3. Institutional Risk Console (Admin View)
- **Global Surveillance**: Admins oversee the entire institution’s real-time risk distribution across all active subjects and batches.
- **Faculty Deployment & Evaluation**: Admins can safely deploy new faculty, manage their access credentials, and monitor their active caseloads and resolved doubt volumes. (Features Safe Soft-Deletes and UPSERT re-creation).
- **Global Account Management**: Admins possess overarching authority to reset passwords for both Faculty members and Students across the entire system.
- **Communication Visibility**: Broad-scale monitoring of system communications flagged by predictive models (e.g., Burnout Warning badges on highly stressed students who send 5+ queries a week).
- **Secure, Vintage Theming**: Completely overhauled UI/UX design with an immersive "Oldschool Detective Dossier" vibe—featuring high-contrast khaki, beige, and strict monospace typography.

---

## 🏗️ Technical Architecture

AGMIS follows a classic monolithic Model-View-Controller architecture built on a high-performance Python backend.

| Layer        | Technology                                                                 |
|--------------|-----------------------------------------------------------------------------|
| **Frontend** | Pure HTML/CSS styled with a Vintage Light Theme, Jinja2 Templates, Chart.js JS graphs |
| **Backend**  | FastAPI (Python) for asynchronous endpoints and robust validation          |
| **Database** | SQLite3 (Local file-based database for portability)                        |
| **Machine Learning** | `scikit-learn` (Random Forest, Linear Regression, Joblib Serialization) |

### Key Project Structure

```bash
agmis/
├── backend/
│   ├── app/
│   │   ├── ml/                # Scikit-Learn data pipelines & predictors
│   │   ├── services/          # Database connection, CRUD operations, & queries
│   │   ├── static/            # Vintage/Beige CSS files & static assets
│   │   ├── templates/         # HTML Jinja2 Views (Login, Admin, Faculty, Student)
│   │   └── main.py            # FastAPI Application Entrypoint & JSON Routes
│   ├── models/                # Saved serialized ML Models (.joblib)
│   └── agmis.db               # The generated SQLite Database
└── README.md                  # This documentation
```

---

## 🚀 Quickstart & Installation

To run AGMIS locally on your machine, you must have `Python 3.9+` installed.

### 1. Clone the Repository & Enter Directory
```bash
git clone https://github.com/your-username/agmis.git
cd agmis/backend
```

### 2. Set Up the Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```
*If you are generating predictions, make sure the ML stack is installed:*
```bash
pip install fastapi uvicorn multipart jinja2 scikit-learn pandas python-multipart
```

### 4. Boot the Command Center
You can manually start the application using `uvicorn`:
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
*(The `--reload` flag will auto-refresh the server when file changes are detected).*

---

## 🧪 Generating Mock Data

For testing the application, AGMIS includes a robust data generator that creates realistic, synchronized student records across multiple subjects, batches, and weeks.

```bash
python mock_data_generator.py
```

This script will automatically generate a `mock_data/` directory containing CSV files for:
- **Batches**: Year1_A1, Year1_B1
- **Subjects**: Machine Learning, Data Governance, Computer Networks, Software Engineering, Database Systems
- **Timeline**: Week 1, Week 2, Week 3

*Note: The script ensures that student names and IDs remain perfectly consistent across all subjects and weeks for a given batch, making it ideal for testing historical tracking and multi-subject analytics.*

---

## 🔑 Default Authorization Credentials

To access the various dashboards, navigate to `http://127.0.0.1:8000` in your web browser. 
Due to the system's strict architectural separation, you must log in using the correct assigned identifiers.

- **Admin Console:**
  - *Username:* `admin`
  - *Password:* `admin`
- **Faculty View (Machine Learning):**
  - *Username:* `hiral`
  - *Password:* `ml123`
- **Student View:**
  - Login requires a valid `student_id` created via Faculty CSV Upload. 
  - *Default Password:* `1234`

---

## 📊 Standard CSV Data Format 

For the Machine Learning pipelines to process data correctly, Faculty batch-uploads must be formatted as follows:

| student_id | name | week | lecture_present | lecture_total | assignments_submitted | internal_marks |
|------------|------|------|-----------------|---------------|-----------------------|----------------|
| 101        | John | 1    | 8               | 10            | 2                     | 18             |

Upon successful upload via the Faculty Dashboard, AGMIS immediately normalizes the data, runs the active predictive algorithm, saves the new output predictions to the Database, and updates the Global Risk Distribution graphs.

---

## 🔒 Security & License
*AGMIS is a Final Year Academic Capstone Project.*
While safe architectural patterns (such as Soft-Deletes via the `is_active` flag, session cookie limits, and password salting mechanisms) have been built into the database structures to resemble a production application, please DO NOT deploy this publicly with real Student Personally Identifiable Information (PII) without migrating the authentication system to a secure provider (like OAuth2 or Supabase) and enabling strict HTTPS routing protocols.
