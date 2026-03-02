# AGMIS — Project Status vs PRD

This file maps the [AGMIS PRD](New%20folder/DOCS/📘%20ACADEMIC%20GUIDANCE%20%26%20INTELLIGENCE%20SYSTEM%20(AGMIS)%20PRD.pdf) to what is implemented and what is left.

---

## ✅ Done

| PRD Section | Requirement | Status | Notes |
|-------------|-------------|--------|--------|
| **1–2** | Context, vision, product definition | ✅ | Documented in PRD; README summarizes. |
| **5.1.1** | Data management (upload, validation) | ✅ | Faculty CSV upload in `main.py`; feature_service builds metrics. |
| **5.1.1** | Analytics engine (feature eng, classification, prediction) | ✅ | `features.py`, `classification.py`, `prediction.py`; models in `models/`. |
| **5.1.1** | Guidance system (rule-based) | ✅ | `guidance.py` with PRD-style rules and priorities. |
| **5.1.1** | Faculty dashboard | ✅ | Batch stats, distribution chart, at-risk list, upload. |
| **5.1.1** | Student dashboard | ✅ | Performance summary, prediction, guidance, trend (template present). |
| **5.1.1** | Database schema | ✅ | SQLite: `users`, `records`, `predictions`, `notifications`. |
| **5.1.2** | Auth (role-based) | ✅ | Login by role; faculty vs student redirect. |
| **9.2** | Random Forest classification (5 categories) | ✅ | `classification.py` + `student_classifier.joblib`. |
| **9.3** | Prediction (score + category) | ✅ | `prediction.py` (weighted formula); optional RF regressor in `predictor.joblib`. |
| **9.4** | Guidance rules (attendance, trend, assignments, etc.) | ✅ | `guidance.py`. |
| **10** | Architecture (presentation, app, analytics, data) | ✅ | FastAPI + services + SQLite. |

---

## 🔶 Partially Done

| PRD Section | Requirement | Gap |
|-------------|-------------|-----|
| **FR-3.2** | Configurable weightages | Weights are hardcoded in feature/prediction logic. |
| **FR-4.1** | MAE/RMSE/R² targets | Prediction is formula-based; no stored metrics or confidence interval in DB. |
| **FR-4.3** | Confidence interval on student view | Template supports it; backend may not pass `mae`/confidence. |
| **FR-7.2** | At-risk list sortable by predicted score | List exists; ensure sorted by score ascending. |
| **FR-8** | Student dashboard (percentile, trend graph) | Template has placeholders; need data from `records` for trend. |
| **6.6** | Notifications (weekly email, faculty alerts) | In-app notifications only; no email. |
| **8.2** | Full Supabase schema | `api/endpoints.py` targets Supabase; app currently uses SQLite in `main.py`. |

---

## ❌ Not Done (per PRD)

| PRD Section | Requirement | Notes |
|-------------|-------------|--------|
| **FR-1.2** | Manual marks entry form | Only CSV upload. |
| **FR-2** | Strict validation (range, missing, duplicates) | Basic only. |
| **FR-5.1** | Prediction vs actual tracking (MAE/RMSE post-exam) | No `prediction_accuracy` flow. |
| **FR-9** | Weekly email to students; faculty alert email | Not implemented. |
| **FR-10** | Full audit trail (academic_history, action_logs) | No history tables in SQLite. |
| **4.1.3** | Admin role & dashboard | Only faculty + student. |
| **7.x** | NFRs (load time, scalability, RBAC per subject) | Not measured or enforced. |
| **11** | 16-week sprint plan | Use as roadmap; not all sprints completed. |

---

## Suggested Next Steps (priority order)

1. **Single faculty dashboard route** in `main.py` that computes PRD 5-category **distribution** and **at_risk_students** so the existing faculty template works without errors.
2. **Student dashboard** in `main.py` that passes **performance**, **prediction** (with optional confidence), **guidance**, and **trend_history** from DB + services so the PRD-style student template renders.
3. **Upload response**: return JSON for the faculty upload fetch so the “Upload CSV” button can `location.reload()` on success.
4. **Optional**: Store confidence interval (e.g. ±MAE) in DB and show on student view.
5. **Optional**: Add `academic_history` / `action_logs` and basic audit.
6. **Later**: Email notifications, admin role, Supabase migration if required.

---

*Last updated to match current `backend` and PRD.*
