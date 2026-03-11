<div align="center">
  <img src="https://via.placeholder.com/800x200/2A2A2A/FFCC00?text=AGMIS+Command+Center" alt="AGMIS Banner">

  <h1>AGMIS</h1>
  <h3>Academic Guidance, Motivation & Intelligence System</h3>
  <i>An advanced, intelligence-driven academic platform transforming student data into predictive, actionable guidance.</i>

  <p align="center">
    <a href="#-about-agmis"><strong>Explore the Docs</strong></a> ·
    <a href="#-core-features"><strong>View Features</strong></a> ·
    <a href="#-quickstart--installation"><strong>Get Started</strong></a>
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.9+-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
    <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn">
    <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
    <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" alt="Status">
  </p>
</div>

<br />

## 📖 About AGMIS

**Final Year B.Sc Data Science Capstone Project · Atharva College, Malad**

AGMIS is engineered to combat academic stagnation by predicting student performance **4-6 weeks before critical examinations occur**. By monitoring real-time data inputs—such as attendance drops, assignment submission rates, and internal marks—AGMIS intelligently classifies students into risk profiles. It gives **faculty** a bird's-eye view to deploy early interventions and empowers **students** with ultra-personalized, rule-based course corrections to stay ahead.

---

## 🌟 Core Features

### 🎓 1. Student Dossiers (Student Command Center)
Empowering the scholar with actionable clarity.
- **🔮 Predictive Scoring:** Harnesses a trained Random Forest model to forecast future final exam scores based on historical data.
- **🚦 Risk Classification System:** Students are instantly triaged into dynamic profiles: *Critical, High Risk, Moderate, or High Performer*.
- **🎯 Actionable Guidance Engine:** Generates real-time, mathematically-backed advice (e.g., *"Improve attendance to 85%+ to secure ~8 extra marks"*).
- **✉️ Direct Faculty Communication:** Secure, continuous two-way communication channel to resolve doubts directly with subject professors.

### 👨‍🏫 2. Faculty Command Center (Intervention Dashboard)
Giving educators the ultimate analytical upper hand.
- **📊 Omni-Batch Analytics:** Visualize predictive performance distributions of the entire class dynamically.
- **🚩 Target At-Risk Identification:** Immediately red-flags highly critical student profiles to deploy priority academic interventions.
- **💬 Doubt Management System:** Features a centralized inbox for faculty to review, answer, and manage student queries with full historic chat persistence.
- **📁 Frictionless Data Ingestion:** Drag-and-drop CSV upload for rapid attendance and internal marks syncing—triggering immediate, on-the-fly model re-predictions.

### 🛡️ 3. Institutional Risk Console (Admin View)
Overarching surveillance of academic health across all systems.
- **🌍 Global Surveillance Network:** Aggregate view of real-time risk distribution mapping across all assigned courses and faculty branches.
- **👥 Seamless Personnel Deployment:** Admins control faculty credentialing, user access thresholds, and manage operations like Safe Soft-Deletes.
- **🎨 Immersive, Vintage UI/UX:** Complete visual overhaul featuring an "Oldschool Detective Dossier" aesthetic—with high-contrast khaki/beige styling and strict monospace typography.

---

## 🏗️ Technical Architecture

AGMIS enforces a classic monolithic **Model-View-Controller (MVC)** architectural blueprint built to scale around a high-performance Python ASYNC core.

<div align="center">

| System Layer | Core Technology Stack | Functionality |
| :--- | :--- | :--- |
| **Frontend/UI** | `HTML5`, `CSS3` (Vanilla), `Jinja2`, `Chart.js` | Vintage "Light" Theme, Dynamic UI Generation, Graphical Data Plotting |
| **Backend API** | `FastAPI` (Python) | High-speed async routing, concurrent request handling, validation |
| **Database** | `SQLite3` (Local DB) | Ephemeral, ultra-portable persistence using normalized schemas |
| **ML Engine** | `scikit-learn`, `Pandas`, `NumPy` | Machine learning pipelines, Random Forest Classification, joblib |

</div>

### 📂 Directory Structure

```text
📦 AGMIS Core
 ┣ 📂 backend/
 ┃ ┣ 📂 app/
 ┃ ┃ ┣ 📂 ml/           # Scikit-Learn data pipelines & predictors
 ┃ ┃ ┣ 📂 services/     # Database singletons, CRUD ops, analytics integration
 ┃ ┃ ┣ 📂 static/       # Vintage CSS/JS assets
 ┃ ┃ ┣ 📂 templates/    # UI Views (Login, Admin, Faculty, Student)
 ┃ ┃ ┗ 📜 main.py       # FastAPI Application Entrypoint & Endpoints
 ┃ ┣ 📂 models/         # Multi-layered .joblib serialized neural/forest models
 ┃ ┗ 📜 agmis.db        # Mission-Critical SQLite Datastore
 ┣ 📂 mock_data/        # Simulated large-scale dataset generation 
 ┣ 📂 Docs/             # Institutional Project Reports & Blackbook
 ┣ 📜 PROJECT_STATUS.md # Current Project Checklist against initial PRD
 ┣ 📜 FUTURE_ASPECTS.md # Future Roadmap & Admin Audit Log capabilities
 ┗ 📜 README.md         # Documentation Reference (You are here)
```

---

## 🚀 Quickstart & Installation

Get the command center up and running globally or locally in **3 minutes flat**. Requires `Python 3.9+`.

### Step 1. Clone & Enter
```bash
git clone https://github.com/hamsidhi/AGMIS.git
cd AGMIS
```

### Step 2. Isolate the Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux OS
python3 -m venv venv
source venv/bin/activate
```

### Step 3. Initialize Operational Modules
```bash
# Inside the top level / AGMIS directory:
pip install -r backend/requirements.txt
```
*(Dependencies include: FastAPI, Uvicorn, Jinja2, Scikit-Learn, Pandas, Python-Multipart)*

### Step 4. Ignite the Core
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
*System Live Feedback: Visit [`http://127.0.0.1:8000`](http://127.0.0.1:8000) to access the central gateway.*

---

## 🧪 Simulation / Mock Data Pipeline

AGMIS boasts a fully functioning algorithmic data generator designed to rigorously stress-test the classification engine over massive arrays of data spanning multi-week simulations.

```bash
# From the root directory:
python mock_data_generator.py
```

**What it does:**
Instantly synchronizes arrays of realistic CSVs encompassing:
- **Multiple Batches** *(e.g. Year1_A1, Year1_B1)*
- **Diverse Subjects** *(Machine Learning, Data Governance, OS, Software Engineering)*
- **Timeline Extrapolations** *(Auto-scaling across Weeks 1, 2, and 3)*

*This pipeline guarantees persistent `student_id` validation constraints across historical bounds—perfect for ML stress testing.*

---

## 🔑 Default Global Access Credentials

AGMIS requires highly strict horizontal segregation of roles. To test operations, authenticate through the main portal using these designated access hashes:

<div align="center">

| Operational Tier | Default Username | Standard Password | Scope of Access |
| :--- | :--- | :--- | :--- |
| **Global Admin Console** | `admin` | `admin` | Level 5 System wide control, all subjects, all analytics. |
| **Faculty Dashboard** | `hiral` | `ml123` | Control over Machine Learning batch arrays. |
| **Student Profiles** | *(Valid Target ID)* | `1234` | Highly restricted singular dossier access. |

</div>

> **Note:** A valid `student_id` must either be uploaded through the Faculty CSV Intake Portal or found inside the native Database generation files prior to initial student login.

---

## 📊 CSV Standard Integrity Protocol

To push raw academic metrics into the Machine Learning ingestion engine, Faculty uploads MUST conform exactly to the AGMIS dimensional standard:

| student_id | name | week | lecture_present | lecture_total | assignments_submitted | internal_marks |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1042X | John Doe | 1 | 8 | 10 | 2 | 18 |

> **Process Flow:** The moment CSV arrays are synchronized via the Dashboard, AGMIS immediately cleanses data anomalies, pushes matrices to predictive instances, locks target classification, caches to Local DB, and completely rewires global dynamic distribution charts—*in milliseconds*.

---

## 🔒 Security & License
*AGMIS is a Final Year Academic Capstone Project.*

While safe architectural patterns (such as Soft-Deletes via the `is_active` flag, session cookie limits, and password salting mechanisms) have been built into the database structures to resemble a production application, please DO NOT deploy this publicly with real Student Personally Identifiable Information (PII) without migrating the authentication system to a secure provider (like OAuth2 or Supabase) and enabling strict HTTPS routing protocols.

<div align="center">
  <br>
  <b>Built with Intelligence, Engineered for Guidance</b><br>
  <i>— AGMIS —</i>
</div>
