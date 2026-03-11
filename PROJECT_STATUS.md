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
| **4.1.3** | Admin role & dashboard | ✅ | Complete Admin view with global risk monitoring, chat intelligence, and student/faculty management. |
| **FR-8** | Student dashboard | ✅ | Fully polished with modern graphs, Doubt Sessions chat, hover analytics, and personalized guidelines. |

---

## 🔶 Partially Done

| PRD Section | Requirement | Gap |
|-------------|-------------|-----|
| **FR-3.2** | Configurable weightages | Weights are hardcoded in feature/prediction logic. |
| **FR-4.1** | MAE/RMSE/R² targets | Prediction is formula-based; no stored metrics or confidence interval in DB. |
| **6.6** | Notifications (weekly email, faculty alerts) | In-app push notifications and announcements are done, but no email yet. |
| **8.2** | Full Supabase schema | `api/endpoints.py` targets Supabase; app currently uses SQLite. |

---

## ❌ Not Done (per PRD)

| PRD Section | Requirement | Notes |
|-------------|-------------|--------|
| **FR-1.2** | Manual marks entry form | Only CSV upload available. |
| **FR-2** | Strict validation (range, missing, duplicates) | Basic only. |
| **FR-5.1** | Prediction vs actual tracking (MAE/RMSE post-exam) | No `prediction_accuracy` flow. |
| **FR-9** | Weekly email to students; faculty alert email | Not implemented. |
| **FR-10** | Full audit trail (academic_history, action_logs) | Tracked for future aspect; see FUTURE_ASPECTS.md. |
| **7.x** | NFRs (load time, scalability, RBAC per subject) | Not measured or enforced. |
| **11** | 16-week sprint plan | Used as a roadmap. |

---

## Suggested Next Steps (priority order)

1. **Optional**: Develop Full Audit Trail for Admin Panel (System logs, Academic History mapping). See `FUTURE_ASPECTS.md`.
2. **Optional**: Store confidence intervals (e.g., ±MAE) formally in the Data Layer.
3. **Optional**: Email notifications / SMTP integration.
4. **Later**: Supabase remote cloud migration.

---

*Last updated to match current `backend` and PRD.*
