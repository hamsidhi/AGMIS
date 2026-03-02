# AGMIS System Diagrams

All diagrams for the AGMIS Blackbook Report (Chapter 4). These use Mermaid syntax and can be rendered in GitHub, GitLab, VS Code (with Mermaid extension), or exported to PNG/SVG using [Mermaid Live Editor](https://mermaid.live) or `mermaid-cli`.

---

## Figure 4.1: Overall System Architecture

```mermaid
flowchart TB
    subgraph Users
        Faculty[Faculty]
        Student[Student]
    end

    subgraph Presentation["Presentation Layer"]
        FD[Faculty Dashboard]
        SD[Student Dashboard]
    end

    subgraph Application["Application Layer"]
        API[FastAPI REST API]
        Auth[Authentication & RBAC]
    end

    subgraph Analytics["Analytics Layer"]
        CE[Classification Engine]
        PE[Prediction Engine]
        GE[Guidance Engine]
    end

    subgraph DataProcessing["Data Processing Layer"]
        Val[Validation]
        FE[Feature Engineering]
        Hist[History Management]
    end

    subgraph Data["Data Layer"]
        DB[(PostgreSQL/SQLite)]
    end

    Faculty -->|HTTPS/JSON| FD
    Student -->|HTTPS/JSON| SD
    FD --> API
    SD --> API
    API --> Auth
    Auth --> Val
    Val --> FE
    FE --> Hist
    Hist --> CE
    CE --> PE
    PE --> GE
    GE --> DB
    Val --> DB
    Hist --> DB
    API --> DB
```

---

## Figure 4.2: Five-Layer Architecture (Component Interaction)

```mermaid
flowchart TB
    subgraph Layer1["Presentation Layer"]
        FD[Faculty Dashboard<br/>Upload, Charts, At-Risk List, Metrics]
        SD[Student Dashboard<br/>Summary, Predictions, Trends, Guidance]
    end

    subgraph Layer2["Application Layer"]
        FastAPI[FastAPI]
        Auth[Supabase Auth / Session]
        RBAC[Role-Based Access Control]
    end

    subgraph Layer3["Analytics Layer"]
        ClassEng[Classification Engine<br/>Random Forest]
        PredEng[Prediction Engine<br/>Random Forest Regressor]
        GuidEng[Guidance Engine<br/>Rule-Based]
    end

    subgraph Layer4["Data Processing Layer"]
        Val[Validation<br/>Range, Missing, Duplicates]
        FeatEng[Feature Engineering<br/>Aggregation, Trends, Normalisation]
        HistMgmt[History Management<br/>Archive, Audit Trail]
    end

    subgraph Layer5["Data Layer"]
        DB[(PostgreSQL/Supabase)]
    end

    Layer1 -->|HTTPS JSON| Layer2
    Layer2 --> Layer3
    Layer3 --> Layer4
    Layer4 --> Layer5
```

---

## Figure 4.3: Context Diagram (DFD Level 0)

```mermaid
flowchart LR
    Faculty((Faculty))
    Student((Student))
    AGMIS([AGMIS System])

    Faculty -->|CSV Data, Marks| AGMIS
    AGMIS -->|Batch Analytics, Risk Alerts| Faculty
    Student -->|Login, Requests| AGMIS
    AGMIS -->|Performance Summary, Predictions, Guidance| Student
```

---

## Figure 4.4: Data Flow Diagram Level 1

```mermaid
flowchart TB
    Faculty((Faculty))
    Student((Student))

    P1[1. Receive CSV Upload]
    P2[2. Validate & Transform Data]
    P3[3. Archive to History]
    P4[4. Insert/Update Records]
    P5[5. Compute Features]
    P6[6. Run Classification]
    P7[7. Run Prediction]
    P8[8. Generate Guidance]
    P9[9. Update Dashboards]
    P10[10. Send Notifications]

    DB[(Database)]

    Faculty -->|CSV| P1
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    P5 --> P6
    P6 --> P7
    P7 --> P8
    P8 --> P9
    P9 --> P10

    P2 --> DB
    P3 --> DB
    P4 --> DB
    P8 --> DB

    P9 -->|Dashboard Data| Faculty
    P9 -->|Dashboard Data| Student
    P10 --> Faculty
    P10 --> Student

    Student -->|Request| P9
```

---

## Figure 4.5: Use Case Diagram

```mermaid
flowchart TB
    subgraph Actors
        Faculty((Faculty))
        Student((Student))
        Admin((Admin))
    end

    subgraph FacultyUC["Faculty Use Cases"]
        UC1[Upload Attendance]
        UC2[Upload Marks]
        UC3[View Batch Analytics]
        UC4[View At-Risk Students]
        UC5[View Individual Student Profile]
        UC6[Export Credentials CSV]
        UC7[Receive Critical Alerts]
    end

    subgraph StudentUC["Student Use Cases"]
        UC8[View Performance Summary]
        UC9[View Predicted Score]
        UC10[View Guidance]
        UC11[View Trend Graph]
    end

    subgraph AdminUC["Admin Use Cases"]
        UC12[Manage Faculty Accounts]
        UC13[Configure Rules]
        UC14[View Audit Logs]
    end

    Faculty --> UC1 & UC2 & UC3 & UC4 & UC5 & UC6 & UC7
    Student --> UC8 & UC9 & UC10 & UC11
    Admin --> UC12 & UC13 & UC14
```

---

## Figure 4.6: Sequence Diagram – Data Upload Flow

```mermaid
sequenceDiagram
    participant Faculty
    participant Browser
    participant FastAPI
    participant Validate
    participant Archive
    participant DB
    participant Features
    participant Classification
    participant Prediction
    participant Guidance

    Faculty->>Browser: Upload CSV
    Browser->>FastAPI: POST /upload (CSV file)
    FastAPI->>Validate: Validate data
    Validate-->>FastAPI: Valid/Invalid
    FastAPI->>Archive: Archive previous records
    Archive->>DB: Insert into academic_history
    FastAPI->>DB: Insert/Update academic_records
    FastAPI->>Features: Compute features
    Features->>DB: Read records
    Features-->>FastAPI: Feature matrix
    FastAPI->>Classification: Run classifier
    Classification-->>FastAPI: Categories
    FastAPI->>Prediction: Run regressor
    Prediction-->>FastAPI: Predicted scores
    FastAPI->>Guidance: Generate recommendations
    Guidance-->>FastAPI: Guidance messages
    FastAPI->>DB: Store predictions, guidance
    FastAPI-->>Browser: Success response
    Browser-->>Faculty: Confirmation
```

---

## Figure 4.7: Sequence Diagram – Student Dashboard Load

```mermaid
sequenceDiagram
    participant Student
    participant Browser
    participant FastAPI
    participant Auth
    participant DB
    participant Features
    participant Guidance

    Student->>Browser: Request dashboard
    Browser->>FastAPI: GET /student/dashboard
    FastAPI->>Auth: Verify session/token
    Auth-->>FastAPI: User identity
    FastAPI->>DB: Query academic_records
    FastAPI->>DB: Query prediction_results
    DB-->>FastAPI: Records, predictions
    FastAPI->>Features: Compute trend
    Features-->>FastAPI: Trend data
    FastAPI->>Guidance: Get guidance for student
    Guidance->>DB: Fetch rules, student data
    Guidance-->>FastAPI: Guidance messages
    FastAPI->>FastAPI: Format response (JSON)
    FastAPI-->>Browser: Dashboard data
    Browser->>Browser: Render dashboard
    Browser-->>Student: Display summary, predictions, guidance, trends
```

---

## Figure 4.8: Deployment Diagram

```mermaid
flowchart TB
    subgraph Client["Client Node"]
        Browser[Web Browser]
    end

    subgraph Repo["Source Control"]
        GitHub[GitHub Repository]
    end

    subgraph Hosting["Application Hosting"]
        Railway[Railway / Vercel]
        Backend[FastAPI Backend]
        Frontend[Static Frontend]
    end

    subgraph Database["Database & Auth"]
        Supabase[Supabase]
        PG[(PostgreSQL)]
        AuthSvc[Supabase Auth]
    end

    GitHub -->|Deploy| Railway
    Railway --> Backend
    Railway --> Frontend
    Browser <-->|HTTPS| Railway
    Backend <-->|Connection Pool| Supabase
    Supabase --> PG
    Supabase --> AuthSvc
```

---

## Figure 4.9: Component Diagram

```mermaid
flowchart TB
    subgraph App["AGMIS Application"]
        Main[main.py<br/>FastAPI App]

        subgraph API["api/"]
            Routes[Routes]
            FacultyEP[faculty_dashboard]
            StudentEP[student_dashboard]
            Endpoints[endpoints]
        end

        subgraph Services["services/"]
            DB[database]
            Features[features]
            Classification[classification]
            Prediction[prediction]
            Guidance[guidance]
            Charts[charts]
        end

        subgraph Other["Other"]
            Schemas[schemas/]
            Templates[templates/]
            Static[static/]
        end
    end

    Main --> API
    Main --> Services
    Main --> Other
    API --> Services
    Services --> DB
    Services --> Schemas
    Templates --> Static
```

---

## Figure 4.10: Entity-Relationship Diagram

```mermaid
erDiagram
    users ||--o| students : "has"
    users {
        int user_id PK
        string email
        string role
        string password_hash
    }

    students ||--o{ enrollment : "enrolled in"
    students {
        int student_id PK
        string name
        string email
        string batch
        string department
    }

    subjects ||--o{ enrollment : "has"
    subjects {
        int subject_id PK
        string subject_name
        string subject_code
        int semester
    }

    enrollment ||--o{ academic_records : "has"
    enrollment {
        int enrollment_id PK
        int student_id FK
        int subject_id FK
        string academic_year
    }

    academic_records ||--o{ academic_history : "archived in"
    academic_records {
        int record_id PK
        int enrollment_id FK
        int week_number
        decimal attendance_theory
        decimal attendance_practical
        decimal internal_marks
        decimal assignment_score
        decimal exam_score
        string performance_category
    }

    students ||--o{ prediction_results : "has"
    prediction_results {
        int prediction_id PK
        int student_id FK
        date prediction_date
        decimal predicted_score
        decimal confidence_lower
        decimal confidence_upper
        string predicted_category
    }

    prediction_results ||--o| prediction_accuracy : "validated by"
    prediction_accuracy {
        int accuracy_id PK
        int prediction_id FK
        decimal actual_score
        decimal error
    }

    academic_history {
        int history_id PK
        int record_id FK
        decimal old_attendance_theory
        decimal old_internal_marks
        int modified_by FK
        timestamp modified_on
    }

    users ||--o{ action_logs : "performs"
    action_logs {
        int log_id PK
        int user_id FK
        string action_type
        string entity_type
        int entity_id
        timestamp timestamp
    }
```

---

## Exporting to Images

To export these diagrams to PNG or SVG:

1. **Mermaid Live Editor**: Copy each diagram block to [mermaid.live](https://mermaid.live) and export.
2. **mermaid-cli** (if installed): `mmdc -i AGMIS_DIAGRAMS.md -o output/`
3. **VS Code**: Install "Mermaid Preview" or "Markdown Preview Mermaid Support" extension and use export from preview.
