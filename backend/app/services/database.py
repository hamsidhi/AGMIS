import sqlite3

class DatabaseService:
    def __init__(self):
        self.db_path = "local.db"
        self.init_db()

    def get_conn(self):
            # We add 'check_same_thread=False' to stop the infinite buffering/hanging
            conn = sqlite3.connect(
                self.db_path, 
                timeout=15, 
                check_same_thread=False
            )
            conn.row_factory = sqlite3.Row
            return conn

    def init_db(self):
        with self.get_conn() as conn:
            # 1. Users
            conn.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY, password TEXT, role TEXT, 
                name TEXT, subject_name TEXT, subject_code TEXT, 
                email TEXT, is_first_login INTEGER DEFAULT 1)''')
            cols = [r["name"] for r in conn.execute("PRAGMA table_info(users)").fetchall()]
            if "email" not in cols:
                conn.execute("ALTER TABLE users ADD COLUMN email TEXT")
            if "subject_code" not in cols:
                conn.execute("ALTER TABLE users ADD COLUMN subject_code TEXT")
            if "is_first_login" not in cols:
                conn.execute("ALTER TABLE users ADD COLUMN is_first_login INTEGER DEFAULT 1")
            
            # 2. Records
            conn.execute('''CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT, subject TEXT, week INTEGER,
                lec_pct REAL, prac_pct REAL, assign_pct REAL,
                internal REAL, external REAL, prac_marks REAL)''')
            
            # 3. Predictions
            conn.execute('''CREATE TABLE IF NOT EXISTS predictions (
                student_id TEXT, subject TEXT, score REAL, 
                category TEXT, risk_level TEXT,
                PRIMARY KEY(student_id, subject))''')
            
            # 4. Notifications (Persistent & Targeted)
            notif_cols = [r["name"] for r in conn.execute("PRAGMA table_info(notifications)").fetchall()]
            if notif_cols and "id" not in notif_cols:
                # Table exists but is the old one. Let's drop and recreate safely.
                conn.execute("DROP TABLE notifications")
                notif_cols = []
                
            conn.execute('''CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT, -- NULL for all students
                subject_code TEXT, -- NULL for global
                message TEXT,
                type TEXT DEFAULT 'announcement', -- announcement, alert, system
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            if notif_cols: # If table existed, it might need individual column migrations
                notif_cols = [r["name"] for r in conn.execute("PRAGMA table_info(notifications)").fetchall()]
                if "subject_code" not in notif_cols:
                    if "subject" in notif_cols:
                        conn.execute("ALTER TABLE notifications RENAME COLUMN subject TO subject_code")
                    else:
                        conn.execute("ALTER TABLE notifications ADD COLUMN subject_code TEXT")
                if "type" not in notif_cols:
                    conn.execute("ALTER TABLE notifications ADD COLUMN type TEXT DEFAULT 'announcement'")
                if "created_at" not in notif_cols:
                    conn.execute("ALTER TABLE notifications ADD COLUMN created_at TIMESTAMP DEFAULT '2024-01-01 00:00:00'")

            # 5. Weights per subject
            conn.execute('''CREATE TABLE IF NOT EXISTS weights (
                subject TEXT PRIMARY KEY,
                w_lec REAL, w_prac REAL, w_assign REAL, w_internal REAL, w_external REAL
            )''')

            # 6. Student profile (year / batch mapping)
            conn.execute(
                '''CREATE TABLE IF NOT EXISTS student_profile (
                    student_id TEXT PRIMARY KEY,
                    year INTEGER,
                    batch TEXT
                )'''
            )

            # 7. Study Materials (PDFs, Videos, Links)
            conn.execute('''CREATE TABLE IF NOT EXISTS materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_code TEXT,
                faculty_id TEXT,
                title TEXT,
                type TEXT, -- pdf, video, link
                url TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

            # 8. Calendar Events (Holidays, Global Deadlines, Subject-specific Deadlines)
            conn.execute('''CREATE TABLE IF NOT EXISTS calendar_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_code TEXT, -- NULL for global/system-wide events
                title TEXT,
                description TEXT,
                event_date DATE,
                event_type TEXT, -- exam, deadline, holiday, event
                created_by TEXT)''')

            # 9. Messaging System (Doubt Sessions and General Messaging)
            conn.execute('''CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id TEXT,
                receiver_id TEXT,
                subject_code TEXT,
                message TEXT,
                parent_id INTEGER DEFAULT NULL, -- For threading/responding to doubts
                is_read INTEGER DEFAULT 0,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            msg_cols = [r["name"] for r in conn.execute("PRAGMA table_info(messages)").fetchall()]
            if "subject_code" not in msg_cols:
                conn.execute("ALTER TABLE messages ADD COLUMN subject_code TEXT")
            if "parent_id" not in msg_cols:
                conn.execute("ALTER TABLE messages ADD COLUMN parent_id INTEGER DEFAULT NULL")
            if "is_read" not in msg_cols:
                conn.execute("ALTER TABLE messages ADD COLUMN is_read INTEGER DEFAULT 0")
            if "sent_at" not in msg_cols:
                conn.execute("ALTER TABLE messages ADD COLUMN sent_at TIMESTAMP DEFAULT '2024-01-01 00:00:00'")

            # 10. Audit Logs
            conn.execute('''CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            audit_cols = [r["name"] for r in conn.execute("PRAGMA table_info(audit_logs)").fetchall()]
            if "timestamp" not in audit_cols and "time" in audit_cols:
                conn.execute("ALTER TABLE audit_logs RENAME COLUMN time TO timestamp")
            elif "timestamp" not in audit_cols:
                conn.execute("ALTER TABLE audit_logs ADD COLUMN timestamp TIMESTAMP DEFAULT '2024-01-01 00:00:00'")

            # Initialize Faculty (username, password, role, display name, subject_name, subject_code, is_first_login)
            faculty_data = [
                ("hiral", "ml123", "faculty", "Hiral Maam", "Machine Learning", "CS-ML-501", 1),
                ("harish", "gov123", "faculty", "Harish Sir", "Data Governance", "CS-DG-502", 1),
                ("jennifer", "iot123", "faculty", "Jennifer Maam", "IoT", "CS-IOT-503", 1),
                ("vivek", "an123", "faculty", "Vivek Sir", "Analysis", "CS-AN-504", 1),
                ("vibha", "eda123", "faculty", "Vibha Maam", "EDA", "CS-EDA-505", 1)
            ]
            for data in faculty_data:
                # Use INSERT OR REPLACE to update existing faculty with subject_code
                conn.execute("""
                    INSERT INTO users (username, password, role, name, subject_name, subject_code, is_first_login)
                    VALUES (?,?,?,?,?,?,?)
                    ON CONFLICT(username) DO UPDATE SET 
                        subject_code=COALESCE(users.subject_code, excluded.subject_code),
                        subject_name=COALESCE(users.subject_name, excluded.subject_name)
                """, data)
            
            # Admin (Admin doesn't need forced change)
            conn.execute("INSERT OR IGNORE INTO users (username,password,role,name,subject_name,subject_code,is_first_login) VALUES (?,?,?,?,?,?,?)",
                         ("admin", "admin123", "admin", "Administrator", None, "SYS-ADM", 0))

    def save_faculty_data(self, s_id, name, subj, week, metrics, pred_result):
        with self.get_conn() as conn:
            sid = str(s_id).strip()
            nm = str(name).strip()
            subj = subj.strip() if subj else None
            # New students are created with is_first_login = 1
            # Only update name on conflict, don't reset password or first login status
            conn.execute(
                """
                INSERT INTO users (username, password, role, name, subject_name, is_first_login)
                VALUES (?, '1234', 'student', ?, NULL, 1)
                ON CONFLICT(username) DO UPDATE SET 
                    name=excluded.name,
                    role=COALESCE(users.role, excluded.role)
                """,
                (sid, nm),
            )
            
            # metrics = [lec_pct, prac_pct, assign_pct, internal, external, practical]
            conn.execute(
                '''INSERT INTO records (student_id, subject, week, lec_pct, prac_pct, assign_pct, internal, external, prac_marks) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (sid, subj, week, *metrics),
            )
            
            risk = "Low"
            if pred_result['score'] < 50: risk = "Critical"
            elif pred_result['score'] < 65: risk = "High"
                
            conn.execute(
                '''REPLACE INTO predictions VALUES (?, ?, ?, ?, ?)''',
                (sid, subj, pred_result['score'], pred_result['cat'], risk),
            )

    def add_notif(self, student_id, message, subject_code=None, n_type='announcement'):
        with self.get_conn() as conn:
            # Check for duplicates within last 1 hour
            existing = conn.execute(
                "SELECT id FROM notifications WHERE student_id IS ? AND message=? AND subject_code IS ? AND created_at > datetime('now', '-1 hour')",
                (student_id, message, subject_code)
            ).fetchone()
            if not existing:
                conn.execute(
                    "INSERT INTO notifications (student_id, message, subject_code, type) VALUES (?, ?, ?, ?)",
                    (student_id, message, subject_code, n_type)
                )

    def get_notifications(self, student_id=None, subject_codes=None):
        """Fetch system-wide, subject-specific, and personal notifications."""
        with self.get_conn() as conn:
            # System-wide: student_id is NULL AND subject_code is NULL
            query = "SELECT * FROM notifications WHERE (student_id IS NULL AND subject_code IS NULL)"
            params = []
            
            # Personal: student_id matches
            if student_id:
                query += " OR student_id = ?"
                params.append(student_id)
            
            # Subject-specific: subject_code matches (and not personal)
            if subject_codes:
                placeholders = ', '.join(['?'] * len(subject_codes))
                query += f" OR subject_code IN ({placeholders})"
                params.extend(subject_codes)
                
            query += " ORDER BY created_at DESC LIMIT 50"
            rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def set_student_profile(self, student_id: str, year: int | None, batch: str | None):
        sid = str(student_id).strip()
        b = batch.strip() if batch else None
        with self.get_conn() as conn:
            conn.execute(
                "REPLACE INTO student_profile(student_id, year, batch) VALUES (?, ?, ?)",
                (sid, year, b),
            )

    def get_student_profile(self, student_id: str):
        sid = str(student_id).strip()
        with self.get_conn() as conn:
            row = conn.execute("SELECT * FROM student_profile WHERE student_id=?", (sid,)).fetchone()
        return dict(row) if row else None

    def get_students_with_credentials_for_subject(self, subject):
        """Returns list of dicts: name, student_id, password for students in this subject."""
        with self.get_conn() as conn:
            rows = conn.execute(
                """SELECT u.name, u.username AS student_id, u.password
                   FROM users u
                   INNER JOIN predictions p ON p.student_id = u.username
                   WHERE u.role = 'student' AND p.subject = ?
                   GROUP BY u.username""",
                (subject,),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_user(self, username: str):
        with self.get_conn() as conn:
            row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        return dict(row) if row else None

    def get_faculty_list(self):
        with self.get_conn() as conn:
            rows = conn.execute("SELECT username, name, subject_name, email FROM users WHERE role='faculty'").fetchall()
        return [dict(r) for r in rows]

    def update_faculty(self, username: str, name: str | None, subject_name: str | None, email: str | None):
        with self.get_conn() as conn:
            current = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
            if not current:
                return False
            nm = name if name is not None else current["name"]
            subj = subject_name if subject_name is not None else current["subject_name"]
            em = email if email is not None else current["email"] if "email" in current.keys() else None
            conn.execute("UPDATE users SET name=?, subject_name=?, email=? WHERE username=?", (nm, subj, em, username))
        return True

    def get_weights_for_subject(self, subject: str):
        with self.get_conn() as conn:
            row = conn.execute("SELECT * FROM weights WHERE subject=?", (subject,)).fetchone()
        return dict(row) if row else None

    def set_weights_for_subject(self, subject: str, w_lec: float, w_prac: float, w_assign: float, w_internal: float, w_external: float):
        total = (w_lec or 0) + (w_prac or 0) + (w_assign or 0) + (w_internal or 0) + (w_external or 0)
        if total == 0:
            w_lec, w_prac, w_assign, w_internal, w_external = 0.20, 0.10, 0.10, 0.20, 0.40
        else:
            # Normalize weights
            w_lec, w_prac, w_assign, w_internal, w_external = [x / total for x in (w_lec, w_prac, w_assign, w_internal, w_external)]
        with self.get_conn() as conn:
            conn.execute(
                "REPLACE INTO weights (subject, w_lec, w_prac, w_assign, w_internal, w_external) VALUES (?,?,?,?,?,?)",
                (subject, w_lec, w_prac, w_assign, w_internal, w_external),
            )
        return True

    def add_audit_log(self, user_id, action, details):
        with self.get_conn() as conn:
            conn.execute("INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
                         (user_id, action, details))

    def get_materials(self, subject_code=None):
        with self.get_conn() as conn:
            if subject_code:
                rows = conn.execute("SELECT * FROM materials WHERE subject_code=? ORDER BY uploaded_at DESC", (subject_code,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM materials ORDER BY uploaded_at DESC").fetchall()
        return [dict(r) for r in rows]

    def add_material(self, subject_code, faculty_id, title, type, url):
        with self.get_conn() as conn:
            conn.execute("INSERT INTO materials (subject_code, faculty_id, title, type, url) VALUES (?, ?, ?, ?, ?)",
                         (subject_code, faculty_id, title, type, url))
        self.add_audit_log(faculty_id, "UPLOAD_MATERIAL", f"Type: {type}, Title: {title}, Subject: {subject_code}")

    def delete_material(self, material_id, user_id):
        with self.get_conn() as conn:
            conn.execute("DELETE FROM materials WHERE id=?", (material_id,))
        self.add_audit_log(user_id, "DELETE_MATERIAL", f"Material ID: {material_id}")

    def get_calendar_events(self, subject_code=None, include_global=True):
        with self.get_conn() as conn:
            if subject_code:
                if include_global:
                    rows = conn.execute("SELECT * FROM calendar_events WHERE subject_code=? OR subject_code IS NULL ORDER BY event_date ASC", (subject_code,)).fetchall()
                else:
                    rows = conn.execute("SELECT * FROM calendar_events WHERE subject_code=? ORDER BY event_date ASC", (subject_code,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM calendar_events WHERE subject_code IS NULL ORDER BY event_date ASC").fetchall()
        return [dict(r) for r in rows]

    def add_calendar_event(self, subject_code, title, description, event_date, event_type, created_by):
        with self.get_conn() as conn:
            conn.execute("INSERT INTO calendar_events (subject_code, title, description, event_date, event_type, created_by) VALUES (?, ?, ?, ?, ?, ?)",
                         (subject_code, title, description, event_date, event_type, created_by))
        self.add_audit_log(created_by, "ADD_EVENT", f"Type: {event_type}, Title: {title}, Subject: {subject_code or 'GLOBAL'}")

    def delete_calendar_event(self, event_id, user_id):
        with self.get_conn() as conn:
            conn.execute("DELETE FROM calendar_events WHERE id=?", (event_id,))
        self.add_audit_log(user_id, "DELETE_EVENT", f"Event ID: {event_id}")

    def get_messages(self, user_id, role=None, other_id=None, subject_code=None):
        with self.get_conn() as conn:
            # Base query: messages involving the user
            query = "SELECT * FROM messages WHERE (sender_id = ? OR receiver_id = ?"
            params = [user_id, user_id]
            
            # If faculty/admin, they can also see GLOBAL inquiries (receiver_id is NULL)
            if role in ['faculty', 'admin']:
                query += " OR (receiver_id IS NULL AND subject_code = 'GLOBAL')"
                
            query += ")"
            
            if other_id:
                query += " AND (sender_id = ? OR receiver_id = ?)"
                params.extend([other_id, other_id])
            
            if subject_code and role != 'admin': # Admins see all, Faculty see their subject
                query += " AND subject_code = ?"
                params.append(subject_code)
                
            query += " ORDER BY sent_at DESC"
            rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def send_message(self, sender_id, receiver_id, subject_code, message, parent_id=None):
        with self.get_conn() as conn:
            conn.execute("INSERT INTO messages (sender_id, receiver_id, subject_code, message, parent_id) VALUES (?, ?, ?, ?, ?)",
                         (sender_id, receiver_id, subject_code, message, parent_id))
        self.add_audit_log(sender_id, "SEND_MESSAGE", f"To: {receiver_id}, Subject: {subject_code}")

    def get_audit_logs(self, limit=100):
        with self.get_conn() as conn:
            rows = conn.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]

db_service = DatabaseService()
