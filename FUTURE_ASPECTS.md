# AGMIS Future Aspects & Roadmap

This document outlines the planned future features and operational upgrades for the **Academic Guidance, Motivation & Intelligence System (AGMIS)**.

---

## 🔐 1. Admin Panel Expansion: System Audit Logs

To maintain strict operational security and regulatory compliance, the Institutional Risk Console (Admin Panel) will be expanded with a full **Global Audit Engine**.

### Features to be Developed:
- **Academic History Tracking:** Capture every manual modification made to student records (attendance overrides, marks ingestion) by any faculty member.
- **Action Logs (`action_logs` table):** Record authentication events (logins/logouts), deployment of new faculty, and soft-deletes of personnel/students.
- **Timestamp & IP Logging:** Every system mutation will be strictly tagged with an immutable UNIX timestamp and network identifier.
- **Admin UI Integration:** A dedicated **"Audit & Cal (Phase 3)"** tab inside `admin_dashboard.html` that allows Admins to filter system logs chronologically or by specific Faculty IDs.

---

## 📧 2. Advanced Communication (SMTP Pipeline)
- **Weekly Automated Briefings:** Transition from strictly in-app notifications to automated weekly email digests for students, detailing their current predicted trajectory and actionable guidelines.
- **Faculty Alert Broadcasting:** Immediate SMTP email alerts directly to faculty when a student's risk profile escalates to `CRITICAL`.

---

## ☁️ 3. Cloud Database Migration
- Transition from the local, portable `SQLite3` datastore (`agmis.db`) to a scalable, remote **Supabase (PostgreSQL)** environment.
- This will allow seamless multi-campus deployment and strict Role-Based Access Control (RBAC) defined at the database row-level.

---

## 📈 4. Granular Prediction Validation
- **Performance Evaluation (`prediction_accuracy` table):** Automatically capture end-of-semester actual results and compare them against earlier predictions.
- **Live Model Tuning:** Enable the backend to programmatically calculate Mean Absolute Error (MAE) and R² metrics, allowing admins to trigger predictive model retraining via the dashboard.
