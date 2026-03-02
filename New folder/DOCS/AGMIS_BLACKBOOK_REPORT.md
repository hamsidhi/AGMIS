# ACADEMIC GUIDANCE AND INTELLIGENCE SYSTEM (AGMIS)

## FINAL YEAR B.SC DATA SCIENCE PROJECT REPORT

---

**FORMATTING SPECIFICATIONS (Apply in Word)**

- Font: Times New Roman
- Body size: 12 pt
- Headings: 14 pt Bold
- Chapter titles: 16 pt Bold CAPS
- Line spacing: 1.5
- Alignment: Justified

---

# COVER PAGE

---

**ACADEMIC GUIDANCE AND INTELLIGENCE SYSTEM (AGMIS)**

A Final Year Project Report

Submitted in Partial Fulfillment of the Requirements for the Award of

**BACHELOR OF SCIENCE IN DATA SCIENCE**

---

**By**

**Hamza Siddiqui**

**Under the Guidance of**

**[Faculty Name]**

---

**ATHARVA COLLEGE OF ENGINEERING**

**MALAD (W), MUMBAI**

**UNIVERSITY OF MUMBAI**

**2025–2026**

---

# CERTIFICATE

---

This is to certify that the project entitled **"ACADEMIC GUIDANCE AND INTELLIGENCE SYSTEM (AGMIS)"** submitted by **Hamza Siddiqui** in partial fulfillment of the requirements for the award of **Bachelor of Science in Data Science** to the University of Mumbai is a record of bonafide work carried out by him under my supervision and guidance.

The matter embodied in this project report has not been submitted earlier for the award of any other degree or diploma to the best of my knowledge and belief.

---

**Project Guide**  
[Name]  
[Designation]  
[Department]

---

**Head of Department**  
[Name]  
[Designation]  
[Department]

---

**Principal**  
[Name]  
[Designation]

---

**Place:** Mumbai  
**Date:** [Date]

---

# DECLARATION

---

I, **Hamza Siddiqui**, student of B.Sc. Data Science, hereby declare that the project work entitled **"ACADEMIC GUIDANCE AND INTELLIGENCE SYSTEM (AGMIS)"** submitted to Atharva College of Engineering, Malad, is a record of an original work done by me under the guidance of [Faculty Name]. This work has not been submitted elsewhere for the award of any other degree or diploma. I have followed the guidelines provided by the University of Mumbai in the preparation of this report.

---

**Signature of Student**  
**Name:** Hamza Siddiqui  
**Date:** [Date]

---

# ACKNOWLEDGEMENT

---

The successful completion of this project would not have been possible without the support and guidance of several individuals. I take this opportunity to express my sincere gratitude to all those who contributed to this endeavour.

I extend my heartfelt thanks to the Principal of Atharva College of Engineering for providing the necessary infrastructure and resources to carry out this project. I am deeply grateful to the Head of the Department of Data Science for the academic support and encouragement extended throughout the duration of this work.

I owe a special debt of gratitude to my project guide, [Faculty Name], for his/her invaluable guidance, constructive criticism, and constant encouragement. His/her expertise in the domain and willingness to share knowledge have been instrumental in shaping this project. The technical discussions and feedback provided at every stage helped me refine the system design and implementation.

I would like to thank all the faculty members of the Data Science department for their support and for creating an environment conducive to learning and research. I am also grateful to the faculty members who participated in the requirement gathering phase and provided insights into the real-world challenges faced in academic monitoring and student guidance.

My sincere thanks go to my classmates and friends who supported me during the development phase, provided feedback during testing, and helped in the documentation process. I also thank my family for their unwavering support and encouragement throughout this academic journey.

---

**Hamza Siddiqui**

---

# ABSTRACT

---

The Academic Guidance and Intelligence System (AGMIS) is a data-driven platform designed to address the critical gap between academic data collection and actionable intervention in higher education institutions. In the current Indian college ecosystem, attendance registers, internal assessment marks, assignment records, and examination scores are collected continuously but utilised exclusively for final evaluation. This retroactive usage pattern results in delayed identification of at-risk students, typically in weeks twelve to sixteen of the semester, when meaningful intervention is no longer feasible. The system proposed in this project transforms this paradigm by enabling proactive identification of academic risk four to six weeks before critical evaluation points.

AGMIS comprises three core analytical components: a classification engine, a prediction engine, and a guidance engine. The classification engine employs a Random Forest classifier to categorise students into five performance levels—Excellent, Good, Average, At Risk, and Critical—based on a weighted combination of attendance percentage, internal marks, assignment completion rate, and examination scores. The prediction engine utilises a regression model, implemented as a Random Forest Regressor, to forecast the next examination score (CEM-2 or semester-end) with a confidence interval. The model is trained using a temporal sliding window approach, ensuring that predictions are based only on data available at the time of prediction. The guidance engine implements a rule-based logic system that maps performance patterns to specific, actionable recommendations, with each message traceable to a clear rule and accompanied by an estimated impact on future performance.

The system is built on a five-layer architecture comprising the Presentation Layer (Faculty and Student dashboards), the Application Layer (FastAPI backend), the Analytics Layer (classification, prediction, and guidance engines), the Data Processing Layer (validation, feature engineering, and history management), and the Data Layer (PostgreSQL database via Supabase). Role-based access control ensures that faculty members can upload data, view batch analytics, and receive risk alerts, while students have read-only access to their personal performance summaries, predictions, and guidance messages. The design prioritises explainability over black-box accuracy: every prediction is accompanied by feature importance visualisation, and every guidance message is linked to a specific rule.

The project demonstrates the practical application of data science to real institutional problems, combining classification, regression, and rule-based systems within an ethical framework. The system uses only institutionally collected academic data, excludes behavioural surveillance, and positions itself as a decision-support tool that augments rather than replaces faculty judgment. Success metrics include classification accuracy greater than 75 percent, prediction Mean Absolute Error less than six marks, and the ability of faculty to answer the question: "Which students need intervention this week, and why?"

---

**Keywords:** Academic Analytics, Early Warning System, Random Forest Classification, Regression Prediction, Rule-Based Guidance, Explainable AI, Educational Data Mining, Proactive Intervention

---

# TABLE OF CONTENTS

---

| Chapter | Title | Page |
|--------|-------|------|
| 1 | INTRODUCTION | |
| 1.1 | Background | |
| 1.2 | Problem Statement | |
| 1.3 | Academic Context | |
| 1.4 | Motivation | |
| 1.5 | Objectives | |
| 1.6 | Scope | |
| 1.7 | Applicability | |
| 1.8 | Expected Impact | |
| 2 | LITERATURE SURVEY | |
| 3 | SYSTEM STUDY AND ANALYSIS | |
| 3.1 | Existing System | |
| 3.2 | Limitations of Existing System | |
| 3.3 | Proposed System | |
| 3.4 | Requirement Analysis | |
| 3.5 | Feasibility Study | |
| 3.6 | Stakeholder Analysis | |
| 4 | SYSTEM DESIGN | |
| 4.1 | Overall Architecture | |
| 4.2 | Layered Architecture | |
| 4.3 | Data Flow Diagrams | |
| 4.4 | Use Case Diagram | |
| 4.5 | Sequence Diagrams | |
| 4.6 | Deployment Diagram | |
| 4.7 | Component Diagram | |
| 4.8 | Database Design | |
| 4.9 | ER Diagram | |
| 4.10 | Schema Description | |
| 5 | ALGORITHMIC DESIGN | |
| 5.1 | Feature Engineering | |
| 5.2 | Classification Model | |
| 5.3 | Regression Prediction Model | |
| 5.4 | Guidance Rule Engine | |
| 5.5 | Statistical Analytics | |
| 5.6 | Explainability Strategy | |
| 5.7 | Model Comparison Justification | |
| 6 | IMPLEMENTATION | |
| 7 | RESULTS AND OUTPUTS | |
| 8 | TESTING AND VALIDATION | |
| 9 | DEPLOYMENT | |
| 10 | ETHICS, SECURITY AND PRIVACY | |
| 11 | LIMITATIONS | |
| 12 | FUTURE SCOPE | |
| 13 | CONCLUSION | |
| | REFERENCES | |
| | APPENDICES | |

---

# LIST OF FIGURES

---

| Figure No. | Title | Page |
|------------|-------|------|
| 4.1 | Overall System Architecture | |
| 4.2 | Five-Layer Architecture Diagram | |
| 4.3 | Data Flow Diagram Level 0 | |
| 4.4 | Data Flow Diagram Level 1 | |
| 4.5 | Use Case Diagram | |
| 4.6 | Sequence Diagram – Data Upload | |
| 4.7 | Sequence Diagram – Student Dashboard Load | |
| 4.8 | Deployment Diagram | |
| 4.9 | Component Diagram | |
| 4.10 | Entity-Relationship Diagram | |
| 5.1 | Feature Engineering Pipeline | |
| 5.2 | Classification Model Workflow | |
| 5.3 | Temporal Sliding Window for Prediction | |
| 6.1 | Faculty Dashboard Screenshot | |
| 6.2 | Student Dashboard Screenshot | |
| 7.1 | Performance Distribution Chart | |
| 7.2 | Academic Trajectory Chart | |
| 7.3 | At-Risk Student List | |
| 7.4 | Guidance Messages Display | |

---

# LIST OF TABLES

---

| Table No. | Title | Page |
|-----------|-------|------|
| 3.1 | Functional Requirements Summary | |
| 3.2 | Non-Functional Requirements Summary | |
| 4.1 | Access Control Matrix | |
| 4.2 | Database Schema – Core Tables | |
| 4.3 | Database Schema – Prediction Tables | |
| 4.4 | Database Schema – History and Audit Tables | |
| 5.1 | Classification Feature Description | |
| 5.2 | Prediction Feature Description | |
| 5.3 | Guidance Rule Examples | |
| 7.1 | Classification Accuracy Results | |
| 7.2 | Prediction Accuracy Metrics | |
| 8.1 | Test Cases | |

---

# CHAPTER 1 – INTRODUCTION

---

## 1.1 Background

The Indian higher education system generates substantial volumes of academic data throughout each semester. Attendance registers capture theory and practical attendance on a subject-wise and date-wise basis. Internal assessment marks, including CEM-1 (Continuous Evaluation Method 1) and CEM-2, mid-term examinations, and assignment scores, are recorded periodically. Practical and laboratory work completion is documented. Final examination scores are compiled at the end of the semester. This data represents a rich source of information about student engagement, comprehension, and trajectory.

However, the prevailing usage pattern in most institutions is characterised by a critical disconnect: data is collected continuously but utilised retroactively. The primary application of this data occurs at the end of the semester, when it is aggregated for final grade computation. Between the point of data collection and the point of utilisation lies a temporal void of ten to twelve weeks. During this period, problems compound silently. A student whose attendance declines from seventy percent to sixty percent between weeks five and eight, who misses two assignments, and who scores fifty-five in the internal examination in week nine, may not be identified as at-risk until week ten or later. By week twelve, the opportunity for meaningful intervention has often passed. By week sixteen, the semester concludes with a failure that could have been prevented.

Faculty members possess intuitive knowledge of patterns: they recognise that attendance does not equate to understanding, that trajectory matters more than snapshot performance, and that behavioural patterns differ from academic outcomes. Yet they lack the tools to quantify these patterns, to identify at-risk students early, and to allocate limited time across sixty or more students effectively. Students, for their part, receive generic guidance such as "study more" or "improve your performance," delivered often after failure has occurred, without specificity or actionable direction.

The Academic Guidance and Intelligence System (AGMIS) is conceived to bridge this gap. It transforms routine academic data collection into an intelligent, predictive, and actionable guidance system that enables students and faculty to identify, understand, and address academic challenges four to six weeks before critical evaluation points.

---

## 1.2 Problem Statement

The core problem can be stated as follows:

**Academic data is collected continuously but utilised retroactively, resulting in delayed identification of at-risk students and missed opportunities for timely intervention.**

This problem manifests in several specific dimensions:

**Late Detection:** Students are identified as at-risk only after they have failed or are on the verge of failure. Identification occurs typically in weeks twelve to sixteen of the semester. The desired state is identification in weeks four to six, when intervention can still alter outcomes.

**Fragmented Data:** No holistic view of student performance exists. Data resides in Excel spreadsheets, physical registers, and possibly a student portal, but these sources are not unified. There is no single analytics platform that aggregates and visualises performance across dimensions.

**Absence of Prediction:** The system cannot project future trajectory. Faculty and students react to outcomes after they occur. There is no capability to answer the question: "If this student continues their current pattern, what will happen in the next examination?"

**Generic Guidance:** Advice provided to students is one-size-fits-all. "Study more" and "Improve your performance" lack specificity. The desired state is guidance such as: "Improve attendance by fifteen percent to gain approximately eight marks in the next examination."

**Faculty Overload:** Faculty cannot monitor sixty or more students individually. They rely on manual, intuitive tracking. The desired state is automated, data-driven alerts that prioritise students requiring intervention.

---

## 1.3 Academic Context

This project is undertaken as a Final Year B.Sc. Data Science project at Atharva College of Engineering, Malad, under the University of Mumbai. The project demonstrates the practical application of data science methodologies to a real institutional problem. It combines multiple technical domains: classification (Random Forest), regression (Random Forest Regressor and Linear Regression), rule-based systems (guidance engine), database design and management, web application development, and ethical considerations in artificial intelligence.

The project aligns with the learning outcomes of a data science programme: the ability to collect, process, and analyse data; to build and evaluate machine learning models; to deploy models in a production-like environment; and to communicate findings effectively. It also addresses the institutional need for tools that support academic quality and student success.

---

## 1.4 Motivation

The motivation for this project stems from three sources.

**Faculty Feedback:** Direct engagement with faculty members revealed a clear demand for batch-level analytics, student notifications, a prediction model to forecast future performance, and explainable logic rather than opaque "AI magic." The critical requirement articulated was: "If a student continues their current pattern, what will happen in the next exam?"

**Observed Institutional Gap:** The gap between data collection and actionable intervention is observable across many institutions. The consequences—delayed identification, generic guidance, and faculty overload—are well documented in educational research. Early intervention has been shown to be significantly more effective than late intervention.

**Technical Opportunity:** The availability of institutional data, the maturity of machine learning libraries such as scikit-learn, and the accessibility of modern web frameworks and cloud databases create a favourable technical environment for building such a system. The project represents an opportunity to apply data science to a problem with measurable impact.

---

## 1.5 Objectives

The project has the following primary objectives:

**OBJ-1: Current Performance Classification**  
Categorise students based on present academic standing using a Random Forest classifier with five categories: Excellent, Good, Average, At Risk, and Critical. Success metric: classification accuracy greater than 75 percent, F1-score greater than 0.70 per category.

**OBJ-2: Future Performance Prediction**  
Forecast the next examination score (CEM-2 or semester-end) using a regression model trained on historical patterns. Output includes predicted score (0–100 scale) with confidence range. Success metric: Mean Absolute Error less than six marks, RMSE less than eight marks, R² greater than 0.70.

**OBJ-3: Explainable Guidance Generation**  
Translate performance patterns into specific, actionable advice using rule-based mapping. Every message must be traceable to a clear rule. Success metric: student comprehension and faculty validation of guidance quality.

**OBJ-4: Early Academic Risk Detection**  
Identify at-risk students in weeks four to six, not weeks fourteen to sixteen. Success metric: seventy percent or more of actual failures predicted with six or more weeks of lead time.

**OBJ-5: Role-Based Dashboard System**  
Provide appropriate interfaces for faculty (data upload, batch analytics, risk alerts) and students (personal insights, predictions, guidance). Success metric: load time less than three seconds, usability score greater than 90 percent.

Secondary objectives include batch-level analytics (performance distribution, percentile rankings, trend analysis), historical tracking of performance evolution, and a notification system for students and faculty.

---

## 1.6 Scope

**In Scope:** Data management (CSV upload, manual entry, validation, archiving); analytics engine (feature engineering, Random Forest classification, regression prediction, statistical aggregation); guidance system (rule-based logic, personalised messages, priority ranking); faculty dashboard (upload interface, batch distribution charts, at-risk student list, prediction accuracy metrics); student dashboard (performance summary, predicted score visualisation, percentile ranking, trend graphs, guidance messages); notification system (in-app alerts, optional email); database schema (students, subjects, enrollment, academic records, predictions, users, history, audit logs); authentication and role-based access control.

**Out of Scope:** Mobile application (web-responsive design sufficient); real-time streaming (weekly batch processing sufficient); integration with existing LMS (manual CSV upload alternative); SMS notifications (email and in-app sufficient); mental health assessment (ethical boundary); behavioural surveillance (privacy concern); long-term career prediction (focused on semester outcomes); automated grading (faculty judgment retained); cross-institution benchmarking (data access limitation).

---

## 1.7 Applicability

AGMIS is applicable to higher education institutions that collect attendance, internal assessment marks, assignment records, and examination scores. It is designed for a typical batch size of 60 to 150 students per subject, with support for multiple batches and subjects. The system is institution-agnostic in its core logic but requires configuration of evaluation weightages and rules to align with institutional policies. It is suitable for undergraduate programmes in any discipline where continuous evaluation is practised.

---

## 1.8 Expected Impact

The expected impact of AGMIS includes:

**For Faculty:** Ability to answer "Which students need intervention this week, and why?"; batch-level visibility into performance distribution; prioritised list of at-risk students; decision-support for scheduling counselling and tutorials.

**For Students:** Clear understanding of current standing; knowledge of predicted future trajectory; specific, actionable improvement steps; progress visibility over time.

**For the Institution:** Reduction in failure rates through early intervention; improved student engagement through transparency; data-driven academic support; demonstration of practical application of data science.

**For the Academic Community:** A reference implementation of an explainable, ethical academic analytics system; contribution to the discourse on early warning systems in education.

---

# CHAPTER 2 – LITERATURE SURVEY

---

This chapter presents a comparative analysis of existing approaches to academic monitoring and early warning systems, and establishes the rationale for the design choices adopted in AGMIS.

## 2.1 Traditional Attendance Systems

Traditional attendance systems in Indian colleges typically consist of physical registers maintained by faculty. Attendance is marked manually for each lecture and practical session. At the end of the semester, percentages are calculated and submitted for grade computation. These systems suffer from several limitations: data is not digitised in a structured format until the final submission; there is no intermediate analysis or trend detection; and the data is not integrated with other academic metrics such as internal marks or assignment completion. The primary function is record-keeping, not analytics. AGMIS differs by treating attendance as one input in a multi-dimensional feature set, enabling correlation with other metrics and trend analysis over time.

## 2.2 Learning Management Systems (LMS)

Learning Management Systems such as Moodle, Google Classroom, and institutional portals provide digital platforms for course delivery, assignment submission, and grade recording. They offer dashboards for students and faculty. However, LMS platforms are primarily designed for content delivery and assessment management. They do not typically include predictive analytics, early warning algorithms, or personalised guidance generation. Analytics, when present, are often descriptive (e.g., completion rates) rather than predictive. AGMIS complements rather than replaces an LMS: it consumes data that can be exported from an LMS (or entered manually) and adds the analytical and predictive layer that LMS platforms lack.

## 2.3 Manual Excel Tracking

Many institutions use Excel spreadsheets to maintain attendance, internal marks, and assignment scores. Faculty export data from registers or LMS, consolidate it in spreadsheets, and perform ad-hoc calculations. This approach is flexible but labour-intensive. It does not scale to multiple batches or subjects. There is no automated classification, prediction, or guidance. Version control is poor, and audit trails are absent. AGMIS provides a structured database, automated pipelines, and reproducible analytics, eliminating the manual consolidation and calculation burden while adding predictive capability.

## 2.4 Early Warning Systems in Education

Early warning systems (EWS) in education have been studied extensively. Research indicates that early identification of at-risk students, combined with timely intervention, significantly improves outcomes. EWS typically use indicators such as attendance, grades, and engagement metrics. Methods range from rule-based thresholds (e.g., attendance below 75 percent flags a student) to machine learning models. AGMIS aligns with this body of work by combining multiple indicators, using machine learning for classification and prediction, and generating actionable guidance. The key differentiator is the emphasis on explainability: every prediction and every guidance message is traceable to features and rules, supporting faculty trust and ethical deployment.

## 2.5 Academic Analytics Platforms

Commercial and research academic analytics platforms exist in the market. Some focus on institutional dashboards for administrators; others target student success and retention. Many rely on proprietary algorithms and do not expose the logic behind predictions. AGMIS adopts an open, explainable approach. It uses well-documented algorithms (Random Forest) with published hyperparameters and evaluation metrics. The rule-based guidance engine is transparent and modifiable by faculty. This design choice prioritises trust and academic defensibility over proprietary optimisation.

## 2.6 Superiority of AGMIS

AGMIS is superior to the alternatives discussed above in the following respects:

**Unified Analytics:** It integrates attendance, internal marks, assignments, and examination scores into a single platform with a consistent schema and automated pipelines.

**Predictive Capability:** It forecasts future performance (next examination score) with confidence intervals, enabling proactive rather than reactive intervention.

**Explainability:** Every classification, prediction, and guidance output is traceable to features and rules. There is no black-box behaviour.

**Actionable Guidance:** Guidance messages are specific (e.g., "Improve attendance to 85 percent to gain approximately eight marks") rather than generic.

**Ethical Design:** It uses only academic data, excludes behavioural surveillance, and positions itself as decision-support rather than decision-maker.

**Scalability:** It is designed for 150 to 300 students with support for 10,000 or more historical records, with cloud deployment handling scaling.

**Accessibility:** Role-based dashboards provide faculty and students with appropriate interfaces without requiring technical expertise.

---

# CHAPTER 3 – SYSTEM STUDY AND ANALYSIS

---

## 3.1 Existing System

The existing system in most Indian colleges comprises the following components:

**Attendance Registers:** Physical or digital registers recording presence in theory and practical classes. Data is typically aggregated at semester end for grade computation.

**Internal Assessment Records:** Marks for CEM-1, CEM-2, assignments, and practicals are recorded in spreadsheets or institutional systems. Submission is often batch-based at the end of the semester.

**Student Portals:** Some institutions provide portals where students can view attendance percentage and internal marks. These are typically read-only and do not include analytics or predictions.

**Excel-Based Tracking:** Faculty may maintain personal spreadsheets to track student performance across the semester. This is informal and not standardised.

The existing system is characterised by fragmentation, retroactive usage, and absence of predictive or guidance capabilities.

---

## 3.2 Limitations of Existing System

The limitations of the existing system are summarised as follows:

1. **Temporal Lag:** Data is used for final evaluation only. There is no intermediate analysis during the semester.

2. **No Predictive Insight:** The system cannot answer "What will happen if the student continues this pattern?"

3. **Generic Guidance:** Advice to students is non-specific and often delivered after failure.

4. **Faculty Overload:** Manual monitoring of large batches is infeasible. Faculty rely on intuition rather than data-driven prioritisation.

5. **Fragmented Data:** Multiple sources (registers, spreadsheets, portals) are not unified.

6. **No Early Warning:** At-risk students are identified too late for effective intervention.

7. **Lack of Explainability:** Where analytics exist, the logic is often opaque.

---

## 3.3 Proposed System

The proposed system, AGMIS, addresses these limitations through:

1. **Unified Data Platform:** A single database storing students, subjects, enrollment, academic records, predictions, and audit logs.

2. **Classification Engine:** Random Forest classifier categorising students into five performance levels based on weighted features.

3. **Prediction Engine:** Regression model forecasting next examination score with confidence interval.

4. **Guidance Engine:** Rule-based system generating personalised, actionable recommendations with impact estimates.

5. **Faculty Dashboard:** Data upload, batch analytics, at-risk student list, prediction accuracy metrics, individual student view.

6. **Student Dashboard:** Performance summary, predicted score, trend graphs, guidance messages.

7. **Notification System:** In-app and optional email alerts for students and faculty.

8. **Role-Based Access:** Faculty and students have appropriate permissions; audit trails record all actions.

---

## 3.4 Requirement Analysis

### 3.4.1 Functional Requirements

The functional requirements are derived from the PRD and presented in Table 3.1.

**Table 3.1: Functional Requirements Summary**

| ID | Requirement | Category | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-1.1 | Faculty shall upload attendance via CSV | Data Management | CSV validated; invalid rows rejected; duplicates prevented |
| FR-1.2 | Faculty shall upload internal marks manually | Data Management | Form with validation; save triggers recalculation |
| FR-1.3 | System shall archive previous data before updates | Data Management | Old record to history table; no deletion |
| FR-2.1 | System shall validate attendance range (0–100) | Data Validation | Values outside range rejected |
| FR-2.2 | System shall validate marks range | Data Validation | Internal 0–50; Exam 0–100; negatives rejected |
| FR-2.3 | System shall handle missing values | Data Validation | Missing flagged; incomplete excluded from classification |
| FR-3.1 | System shall classify into 5 categories | Classification | Random Forest; accuracy >75%; F1 >0.70 per category |
| FR-3.2 | System shall compute weighted score | Classification | Formula: 0.2×Att + 0.3×Internal + 0.2×Assign + 0.3×Exam |
| FR-3.3 | System shall display feature importance | Classification | Horizontal bar chart on faculty dashboard |
| FR-4.1 | System shall predict next exam score | Prediction | MAE <6; RMSE <8; R² >0.70; confidence interval |
| FR-4.2 | System shall store prediction history | Prediction | All predictions timestamped; no deletion |
| FR-4.3 | System shall visualise prediction confidence | Prediction | Student dashboard shows score ± MAE |
| FR-5.1 | System shall measure prediction vs actual | Prediction | MAE, RMSE per batch; retrain if MAE >8 |
| FR-6.1 | System shall generate personalised guidance | Guidance | Rule-based; priority assigned; top 3 displayed |
| FR-6.2 | Guidance shall include impact estimates | Guidance | Marks gain displayed per recommendation |
| FR-7.1 | Faculty dashboard: batch distribution | Dashboard | Bar chart; pie chart; filter; export PDF |
| FR-7.2 | Faculty dashboard: at-risk list | Dashboard | Sortable table; click for profile; export CSV |
| FR-7.3 | Faculty dashboard: prediction accuracy | Dashboard | MAE, RMSE, R²; comparison; trend |
| FR-8.1 | Student dashboard: performance summary | Dashboard | Category, score, percentile; color-coded |
| FR-8.2 | Student dashboard: predicted performance | Dashboard | Score ± MAE; expected category; confidence |
| FR-8.3 | Student dashboard: guidance messages | Dashboard | 3–5 messages; priority order; action, impact, deadline |
| FR-8.4 | Student dashboard: performance trend | Dashboard | Line graph; weeks vs score |
| FR-9.1 | Weekly summary email to students | Notification | Monday 8 AM; category, score, top 3 guidance |
| FR-9.2 | Faculty alert for critical-risk students | Notification | When predicted <50; student list |
| FR-9.3 | Notify students of category changes | Notification | Old/new category; reason |
| FR-10.1 | Complete audit trail | History | All updates to history table; no deletion |
| FR-10.2 | Track prediction accuracy over time | History | Actual vs predicted; store; display trends |

### 3.4.2 Non-Functional Requirements

**Table 3.2: Non-Functional Requirements Summary**

| ID | Category | Requirement | Target |
|----|----------|-------------|--------|
| NFR-1 | Performance | Dashboard load time | Student <3 s; Faculty <5 s |
| NFR-2 | Performance | Batch processing | <10 min for 150 students |
| NFR-3 | Performance | Scalability | 300 users; 10,000+ records |
| NFR-4 | Accuracy | Classification | Accuracy >75%; F1 >0.70 per category |
| NFR-5 | Accuracy | Prediction | MAE <6; RMSE <8; R² >0.70 |
| NFR-6 | Accuracy | Data quality | <5% missing; outliers flagged |
| NFR-7 | Security | Authentication | Email + password; min 8 chars |
| NFR-8 | Security | Authorization | RBAC; role separation |
| NFR-9 | Security | Data privacy | Encrypted at rest; HTTPS |
| NFR-10 | Security | Audit logging | All actions logged; 2 semesters |
| NFR-11 | Usability | UI | Responsive; <3 clicks to feature |
| NFR-12 | Usability | Accessibility | WCAG AA; keyboard nav |
| NFR-13 | Reliability | Availability | 99% uptime (academic hours) |
| NFR-14 | Reliability | Data integrity | ACID; foreign keys; daily backup |
| NFR-15 | Maintainability | Code quality | Modular; documented |
| NFR-16 | Maintainability | Deployment | Single-command; env vars |
| NFR-17 | Explainability | Model | Feature importance; prediction explanation |
| NFR-18 | Explainability | Guidance | Every message linked to rule |

---

## 3.5 Feasibility Study

### 3.5.1 Technical Feasibility

The proposed technology stack—FastAPI (Python), PostgreSQL (Supabase), scikit-learn, HTML/CSS/JavaScript—is mature and well-documented. All components are open-source or available on free tiers. The algorithms (Random Forest) are standard and have been validated in similar contexts. The development team has access to the necessary tools and infrastructure. Technical feasibility is high.

### 3.5.2 Operational Feasibility

Faculty are already accustomed to exporting attendance and marks from registers or LMS. CSV upload is a minimal change to their workflow. Students are familiar with web-based portals. The system does not require extensive training. Operational feasibility is high.

### 3.5.3 Economic Feasibility

Supabase, Railway, and Vercel offer free tiers sufficient for a pilot deployment. No licensing costs are incurred for open-source components. The primary cost is development effort. Economic feasibility is high for an academic project.

---

## 3.6 Stakeholder Analysis

**Faculty:** Primary data owners. They upload data, view analytics, receive alerts, and act on interventions. They require an intuitive interface, explainable outputs, and the ability to export reports.

**Students:** Data consumers. They view their performance, predictions, and guidance. They require clarity, specificity in guidance, and assurance that the system supports rather than punishes.

**Administration:** May oversee system deployment, user management, and audit trails. They require security, compliance, and maintainability.

**Institution:** Benefits from improved student outcomes, reduced failure rates, and demonstration of data-driven decision-making.

---

---

# CHAPTER 4 – SYSTEM DESIGN

---

## 4.1 Overall Architecture

AGMIS follows a five-layer architecture that separates concerns across Presentation, Application, Analytics, Data Processing, and Data layers. The overall architecture ensures that user interactions flow through authenticated endpoints, business logic is encapsulated in services, and data integrity is maintained through validation and audit trails.

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

*Figure 4.1: High-level system architecture showing the flow from user interaction through to database persistence.*

---

## 4.2 Layered Architecture

**Presentation Layer:** Comprises the Faculty Dashboard and Student Dashboard. The Faculty Dashboard provides data upload interface, batch performance distribution charts, at-risk student list, prediction accuracy metrics, and individual student view. The Student Dashboard provides performance summary card, predicted score visualisation, percentile ranking, trend graphs, and personalised guidance messages. Communication with the Application Layer occurs over HTTPS using JSON payloads.

**Application Layer:** Implemented using FastAPI (Python). Handles authentication (Supabase Auth or session-based), authorization (role-based access control), API routes for upload, prediction, and dashboard data, and business logic orchestration. Exposes RESTful endpoints.

**Analytics Layer:** Contains three engines. The Classification Engine uses a Random Forest classifier to assign performance categories. The Prediction Engine uses a regression model (Random Forest Regressor) to forecast next examination scores. The Guidance Engine implements rule-based logic to generate personalised recommendations. All engines are invoked by the Application Layer after data validation and feature computation.

**Data Processing Layer:** Comprises validation (range checks, missing value handling, duplicate prevention), feature engineering (aggregation, trend computation, normalisation), and history management (archiving previous records, maintaining audit trail). Ensures data quality before analytics and preserves lineage for compliance.

**Data Layer:** Implemented using PostgreSQL (Supabase) or SQLite for local deployment. Stores students, subjects, enrollment, academic records, prediction results, prediction accuracy, academic history, action logs, and user management tables. Supports ACID transactions, foreign key constraints, and indexing for query performance.

```mermaid
flowchart TB
    subgraph Layer1["Presentation Layer"]
        FD[Faculty Dashboard]
        SD[Student Dashboard]
    end
    subgraph Layer2["Application Layer"]
        FastAPI[FastAPI]
        Auth[Supabase Auth / Session]
        RBAC[Role-Based Access Control]
    end
    subgraph Layer3["Analytics Layer"]
        ClassEng[Classification Engine - Random Forest]
        PredEng[Prediction Engine - Random Forest Regressor]
        GuidEng[Guidance Engine - Rule-Based]
    end
    subgraph Layer4["Data Processing Layer"]
        Val[Validation]
        FeatEng[Feature Engineering]
        HistMgmt[History Management]
    end
    subgraph Layer5["Data Layer"]
        DB[(PostgreSQL/Supabase)]
    end
    Layer1 -->|HTTPS JSON| Layer2
    Layer2 --> Layer3
    Layer3 --> Layer4
    Layer4 --> Layer5
```

*Figure 4.2: Detailed layered architecture showing component interaction.*

---

## 4.3 Data Flow Diagrams

### 4.3.1 Level 0 (Context Diagram)

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

*Figure 4.3: Context diagram showing external entities (Faculty, Student) and the AGMIS system as a single process.*

The Level 0 diagram depicts Faculty and Student as external entities. Faculty provides CSV data and receives batch analytics and risk alerts. Student receives performance summary, predictions, and guidance. The system is the central process.

### 4.3.2 Level 1 (Decomposition)

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

*Figure 4.4: Level 1 DFD showing internal processes: Data Upload, Validation, Feature Engineering, Classification, Prediction, Guidance Generation, Dashboard Rendering.*

Processes include: (1) Receive CSV Upload; (2) Validate and Transform Data; (3) Archive to History; (4) Insert/Update Records; (5) Compute Features; (6) Run Classification; (7) Run Prediction; (8) Generate Guidance; (9) Update Dashboards; (10) Send Notifications.

---

## 4.4 Use Case Diagram

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

*Figure 4.5: Use case diagram showing actors (Faculty, Student, Admin) and use cases (Upload Data, View Batch Analytics, View At-Risk List, View Individual Student, View Personal Dashboard, Receive Notifications, Export Reports, Manage Users).*

Faculty use cases: Upload Attendance, Upload Marks, View Batch Analytics, View At-Risk Students, View Individual Student Profile, Export Credentials CSV, Receive Critical Alerts. Student use cases: View Performance Summary, View Predicted Score, View Guidance, View Trend Graph. Admin use cases (optional): Manage Faculty Accounts, Configure Rules, View Audit Logs.

---

## 4.5 Sequence Diagrams

### 4.5.1 Data Upload Flow

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

*Figure 4.6: Sequence diagram for faculty CSV upload: Faculty → Upload → FastAPI → Validate → Archive → Insert → Feature Engineering → Classification → Prediction → Guidance → Update DB → Response.*

### 4.5.2 Student Dashboard Load

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

*Figure 4.7: Sequence diagram for student dashboard: Student → Request → FastAPI → Auth → Query Records, Predictions, Guidance → Compute Trend → Format Response → Render Dashboard.*

---

## 4.6 Deployment Diagram

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

*Figure 4.8: Deployment diagram showing GitHub repository, Railway/Vercel for application hosting, Supabase for database, and client browsers.*

Components: GitHub (source code), Railway or Vercel (backend and frontend hosting), Supabase (PostgreSQL, authentication), Client (web browser). Communication: HTTPS between client and application; application connects to Supabase via connection pool.

---

## 4.7 Component Diagram

```mermaid
flowchart TB
    subgraph App["AGMIS Application"]
        Main[main.py - FastAPI App]
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

*Figure 4.9: Component diagram showing FastAPI app, services (database, features, classification, prediction, guidance, charts), API routes, and templates.*

Components: main.py (FastAPI app), api/ (routes), services/ (database, features, classification, prediction, guidance, charts), schemas/, templates/, static/.

---

## 4.8 Database Design

The database is designed for normalisation, referential integrity, and auditability. Core tables support the academic domain; prediction tables store model outputs; history and audit tables support compliance and traceability.

---

## 4.9 ER Diagram

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

*Figure 4.10: ER diagram showing entities (users, students, subjects, enrollment, academic_records, prediction_results, prediction_accuracy, academic_history, action_logs) and relationships.*

Key relationships: users (faculty/student/admin); students linked to users; enrollment links students to subjects; academic_records link to enrollment; prediction_results link to students; academic_history links to academic_records; action_logs link to users.

---

## 4.10 Schema Description

### 4.10.1 Core Tables

**Table 4.2: Core Database Schema**

| Table | Column | Type | Constraint | Description |
|-------|--------|------|------------|-------------|
| students | student_id | INTEGER | PRIMARY KEY | Unique identifier |
| students | name | VARCHAR(100) | NOT NULL | Full name |
| students | email | VARCHAR(100) | UNIQUE | Login credential |
| students | batch | VARCHAR(20) | NOT NULL | e.g., 2024-DS-A |
| students | department | VARCHAR(50) | NOT NULL | e.g., Data Science |
| subjects | subject_id | INTEGER | PRIMARY KEY | Unique identifier |
| subjects | subject_name | VARCHAR(100) | NOT NULL | e.g., Machine Learning |
| subjects | subject_code | VARCHAR(20) | UNIQUE | e.g., DS301 |
| subjects | semester | INTEGER | NOT NULL | 1–8 |
| enrollment | enrollment_id | INTEGER | PRIMARY KEY | Unique identifier |
| enrollment | student_id | INTEGER | FOREIGN KEY | References students |
| enrollment | subject_id | INTEGER | FOREIGN KEY | References subjects |
| enrollment | academic_year | VARCHAR(10) | NOT NULL | e.g., 2024-25 |
| academic_records | record_id | INTEGER | PRIMARY KEY | Unique identifier |
| academic_records | enrollment_id | INTEGER | FOREIGN KEY | References enrollment |
| academic_records | week_number | INTEGER | NOT NULL | Week 1–16 |
| academic_records | attendance_theory | DECIMAL(5,2) | CHECK 0–100 | Theory attendance % |
| academic_records | attendance_practical | DECIMAL(5,2) | CHECK 0–100 | Practical attendance % |
| academic_records | internal_marks | DECIMAL(5,2) | CHECK 0–100 | Internal assessment |
| academic_records | assignment_score | DECIMAL(5,2) | CHECK 0–100 | Assignment score |
| academic_records | exam_score | DECIMAL(5,2) | CHECK 0–100 | Exam score |
| academic_records | weighted_score | DECIMAL(5,2) | COMPUTED | Auto-calculated |
| academic_records | performance_category | VARCHAR(20) | NOT NULL | Excellent/Good/Average/At Risk/Critical |

### 4.10.2 Prediction Tables

**Table 4.3: Prediction Schema**

| Table | Column | Type | Constraint | Description |
|-------|--------|------|------------|-------------|
| prediction_results | prediction_id | INTEGER | PRIMARY KEY | Unique identifier |
| prediction_results | student_id | INTEGER | FOREIGN KEY | References students |
| prediction_results | prediction_date | DATE | NOT NULL | When prediction made |
| prediction_results | prediction_horizon | INTEGER | NOT NULL | Weeks ahead (4, 6, 8) |
| prediction_results | predicted_score | DECIMAL(5,2) | NOT NULL | Predicted exam score |
| prediction_results | confidence_lower | DECIMAL(5,2) | NOT NULL | Lower bound (95% CI) |
| prediction_results | confidence_upper | DECIMAL(5,2) | NOT NULL | Upper bound (95% CI) |
| prediction_results | predicted_category | VARCHAR(20) | NOT NULL | Expected class |
| prediction_results | model_version | VARCHAR(10) | NOT NULL | e.g., rf_v1.0 |
| prediction_results | features_used | JSONB | NOT NULL | Snapshot of input features |
| prediction_accuracy | accuracy_id | INTEGER | PRIMARY KEY | Unique identifier |
| prediction_accuracy | prediction_id | INTEGER | FOREIGN KEY | References prediction_results |
| prediction_accuracy | actual_score | DECIMAL(5,2) | NOT NULL | Actual exam score |
| prediction_accuracy | error | DECIMAL(5,2) | COMPUTED | predicted − actual |
| prediction_accuracy | absolute_error | DECIMAL(5,2) | COMPUTED | ABS(error) |

### 4.10.3 History and Audit Tables

**Table 4.4: History and Audit Schema**

| Table | Column | Type | Constraint | Description |
|-------|--------|------|------------|-------------|
| academic_history | history_id | INTEGER | PRIMARY KEY | Unique identifier |
| academic_history | record_id | INTEGER | FOREIGN KEY | References academic_records |
| academic_history | old_attendance_theory | DECIMAL(5,2) | | Previous value |
| academic_history | old_internal_marks | DECIMAL(5,2) | | Previous value |
| academic_history | old_weighted_score | DECIMAL(5,2) | | Previous value |
| academic_history | modified_by | INTEGER | FOREIGN KEY | Faculty user_id |
| academic_history | modified_on | TIMESTAMP | NOT NULL | Change timestamp |
| action_logs | log_id | INTEGER | PRIMARY KEY | Unique identifier |
| action_logs | user_id | INTEGER | FOREIGN KEY | Who performed action |
| action_logs | action_type | VARCHAR(50) | NOT NULL | upload/update/delete |
| action_logs | entity_type | VARCHAR(50) | NOT NULL | student/record/prediction |
| action_logs | entity_id | INTEGER | NOT NULL | Which record affected |
| action_logs | details | TEXT | | JSON details |
| action_logs | timestamp | TIMESTAMP | DEFAULT NOW | When action occurred |

---

# CHAPTER 5 – ALGORITHMIC DESIGN

---

## 5.1 Feature Engineering

Feature engineering transforms raw academic data into numerical and categorical inputs suitable for machine learning models. The pipeline computes the following features.

### 5.1.1 Classification Features (7 features)

**Table 5.1: Classification Feature Description**

| Feature | Description | Scale | Computation |
|---------|-------------|-------|-------------|
| Overall Attendance % | Combined theory and practical, weighted by class hours | 0–100 | (theory_att × hours_theory + prac_att × hours_prac) / total_hours |
| Internal Marks Average | Average across CEM-1, CEM-2, assignments | 0–100 | Mean of available internal scores, normalised to 100 |
| Assignment Completion Rate | Proportion of assignments submitted | 0–100 | (Submitted / Total) × 100 |
| Practical Performance Score | Lab work and practical exam scores | 0–100 | Normalised to 100 scale |
| Attendance Trend | Direction of change over recent weeks | −1, 0, 1 | Slope of attendance over last 4 weeks: <−2% → −1; −2% to +2% → 0; >+2% → 1 |
| Previous Exam Score | Last available exam (e.g., CEM-1) | 0–100 | Direct value; default 50 if first semester |
| Submission Consistency | Regularity of submission | 0–1 | Inverse of standard deviation of submission gaps; low σ = consistent |

### 5.1.2 Prediction Features (5 features)

**Table 5.2: Prediction Feature Description**

| Feature | Description | Scale |
|---------|-------------|-------|
| Current Attendance % | Most recent weekly attendance | 0–100 |
| Previous Exam Score | CEM-1 or most recent assessment | 0–100 |
| Internal Marks Average | Current semester internal assessments | 0–100 |
| Assignment Submission Rate | Proxy for engagement | 0–100 |
| Attendance Trend | −1 (declining), 0 (stable), 1 (improving) | −1, 0, 1 |

**[Insert Feature Engineering Pipeline Diagram Here]**

*Figure 5.1: Feature engineering pipeline showing raw data inputs and computed feature outputs.*

---

## 5.2 Classification Model – Random Forest

### 5.2.1 Rationale

Random Forest is selected for classification because: (1) academic performance exhibits non-linear relationships—attendance alone does not determine success; (2) Random Forest captures interaction effects (e.g., high attendance with low marks suggests comprehension issues); (3) it provides feature importance for explainability; (4) it is robust to noise and handles class imbalance via class_weight='balanced'.

### 5.2.2 Target Variable

Five classes: Excellent (≥85% weighted score), Good (75–84%), Average (60–74%), At Risk (50–59%), Critical (<50%).

### 5.2.3 Hyperparameters

```
RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    max_features='sqrt',
    class_weight='balanced',
    random_state=42
)
```

### 5.2.4 Training Strategy

1. Load historical data (previous 2 semesters).
2. Compute 7 features per student-record.
3. Train-test split (80/20), stratified by class.
4. Train Random Forest.
5. Evaluate: accuracy, precision, recall, F1 per class; confusion matrix; feature importance.
6. Save model (joblib).
7. Deploy for real-time classification.

### 5.2.5 Evaluation Metrics

Target: Overall accuracy >75%; per-class F1 >0.70; top 3 features explain >60% variance.

**[Insert Classification Model Workflow Diagram Here]**

*Figure 5.2: Classification model workflow from feature input to category output.*

---

## 5.3 Regression Prediction Model

### 5.3.1 Temporal Sliding Window

Predictions must not use future data. For each student at week t, the training sample is constructed as: Features (X) = data from weeks 1 to t; Target (y) = exam score at week t+k (k = 4, 6, or 8 weeks). Example: At week 4, features from weeks 1–4 predict score at week 8.

**[Insert Temporal Sliding Window Diagram Here]**

*Figure 5.3: Temporal sliding window showing feature window and prediction horizon.*

### 5.3.2 Algorithm

Production model: Random Forest Regressor. Baseline: Linear Regression. Hyperparameters for RF Regressor: n_estimators=100, max_depth=10, min_samples_split=10, random_state=42.

### 5.3.3 Evaluation Metrics

MAE <6 marks; RMSE <8 marks; R² >0.70; MAPE <10%.

### 5.3.4 Confidence Intervals

After training, estimate MAE on test set. For new prediction: confidence_margin = 1.5 × MAE; lower_bound = max(0, predicted − margin); upper_bound = min(100, predicted + margin). Display: "Predicted Score: 68 ± 5 marks (95% confidence: 63–73)."

---

## 5.4 Guidance Rule Engine

### 5.4.1 Rule Structure

```
IF (condition_1 AND condition_2):
    guidance_message = "Specific action with expected impact"
    priority = "HIGH" | "MEDIUM" | "LOW" | "CRITICAL"
    deadline = "Week X" or "Before next exam"
```

### 5.4.2 Example Rules

**Table 5.3: Guidance Rule Examples**

| Condition | Guidance Message | Priority |
|-----------|------------------|----------|
| Attendance <75% AND predicted_score <60 | Improve attendance to 85%+ to gain ~8 marks in next exam | HIGH |
| Attendance ≥85% AND internal_avg <70 AND predicted_score <75 | Focus on internal exam preparation and assignment quality | MEDIUM |
| Assignment rate <60% | Complete pending assignments before deadline to gain ~5 marks | HIGH |
| Predicted score 45–55 | Immediate intervention needed—meet faculty this week | CRITICAL |
| Predicted score ≥85 AND attendance ≥90 | Maintain consistency and support peers | LOW |

### 5.4.3 Impact Estimation

Impact is estimated using feature importance from the prediction model. Formula: impact_marks ≈ (improvement_in_feature / 100) × 100 × feature_importance. Example: Improving attendance by 15% with importance 0.30 yields approximately 4.5 marks (rounded to ~5).

---

## 5.5 Statistical Analytics

Batch-level analytics include: mean, median, standard deviation of weighted scores; percentile rankings; performance distribution (count per category); trend analysis (slope of score over weeks). All computed using standard statistical functions (pandas, numpy).

---

## 5.6 Explainability Strategy

1. **Feature Importance:** Random Forest provides feature_importances_; displayed as horizontal bar chart on faculty dashboard.
2. **Prediction Explanation:** "Predicted score 68 because: attendance 80% (contribution: +16), internal marks 65 (contribution: +13)..."
3. **Guidance Traceability:** Every message linked to specific rule; rule logic visible to faculty.

---

## 5.7 Model Comparison Justification

**Random Forest vs Logistic Regression:** RF captures non-linearity; Logistic Regression assumes linear decision boundaries. For academic data with interactions, RF is superior.

**Random Forest vs Neural Networks:** RF requires less data, trains faster, provides feature importance. For ~150 students × 16 weeks, RF is optimal. Neural networks would risk overfitting and lack interpretability.

**Rule-Based Guidance vs Learned Guidance:** Rules ensure transparency and faculty control. Learned guidance (e.g., from NLP) would be less interpretable and harder to audit.

---

# CHAPTER 6 – IMPLEMENTATION

---

## 6.1 Technology Stack

**Backend:** Python 3.10+, FastAPI 0.100+, Uvicorn ASGI server. FastAPI provides automatic OpenAPI documentation, async support, and Pydantic validation.

**Database:** Supabase (PostgreSQL) for production; SQLite for local development. Supabase provides authentication, real-time subscriptions, and REST API; SQLite enables offline testing.

**Frontend:** Jinja2 templates with server-side rendering. HTML5, CSS3, JavaScript for interactivity. Matplotlib for chart generation (base64-encoded PNG).

**Authentication:** Supabase Auth (JWT) or session-based login with role verification (faculty/student).

**Deployment:** Railway or Vercel for application hosting; GitHub for version control; Supabase Cloud for database.

---

## 6.2 Backend Architecture

### 6.2.1 Project Structure

```
agmis/
├── main.py                 # FastAPI app entry, route mounting
├── api/
│   ├── endpoints.py        # API route definitions
│   ├── faculty_dashboard.py
│   └── student_dashboard.py
├── services/
│   ├── database.py         # DB operations, CRUD
│   ├── features.py         # Feature engineering
│   ├── classification.py  # Random Forest classifier
│   ├── prediction.py       # Regression model
│   ├── guidance.py         # Rule engine
│   └── charts.py           # Matplotlib chart generation
├── schemas/                # Pydantic models
├── templates/              # Jinja2 HTML
├── static/                 # CSS, JS
├── models/                 # Saved ML models (joblib)
└── requirements.txt
```

### 6.2.2 Module-Wise Explanation

**main.py:** Instantiates FastAPI app, configures Jinja2 with `tojson` filter, mounts routes, defines login and redirect logic. Middleware: CORS, session handling.

**database.py:** Connection management (SQLite/PostgreSQL), CRUD for students, subjects, enrollment, academic_records, prediction_results. Functions: get_student_by_id, get_records_for_student, save_student_data, get_students_for_subject, get_students_with_credentials_for_subject.

**features.py:** compute_classification_features(records) → dict; compute_prediction_features(records) → dict. Handles missing values, normalisation, trend computation.

**classification.py:** load_model(), predict_category(features) → str. Uses joblib-serialised RandomForestClassifier.

**prediction.py:** load_model(), predict_score(features, horizon) → (score, lower, upper). Uses RandomForestRegressor with temporal validation.

**guidance.py:** generate_guidance(performance, prediction, features) → list of {message, priority, deadline}. Implements rule matching and impact estimation.

**charts.py:** generate_line_chart(), generate_bar_chart(), generate_pie_chart(). Returns base64 PNG strings. Uses asyncio.to_thread() for non-blocking execution.

---

## 6.3 API Endpoints

**Table 6.1: API Endpoint Summary**

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | / | Redirect to login or dashboard | Session |
| GET | /login | Render login page | None |
| POST | /login | Authenticate user, set session | None |
| GET | /logout | Clear session, redirect to login | Session |
| GET | /faculty/dashboard | Faculty dashboard with batch analytics | Faculty |
| GET | /faculty/student/{id} | Individual student view | Faculty |
| POST | /faculty/upload | Upload CSV, process, save | Faculty |
| GET | /faculty/export-credentials | Download student credentials CSV | Faculty |
| GET | /student/dashboard | Student dashboard with performance, prediction, guidance | Student |
| GET | /health | Health check (no chart logic) | None |

---

## 6.4 Authentication Flow

1. User submits credentials at /login.
2. Backend validates against users table (or Supabase Auth).
3. On success: create session with user_id, role; redirect to /faculty/dashboard or /student/dashboard.
4. On failure: redirect to /login?error=1; template displays "Invalid credentials."
5. Protected routes check session; if missing or role mismatch, redirect to /login.

---

## 6.5 Data Upload Workflow

1. Faculty selects CSV file and subject on upload form.
2. POST /faculty/upload receives file.
3. Parse CSV: validate headers (student_id, name, attendance_theory, attendance_practical, internal_marks, assignment_score, etc.).
4. Validation: range checks (0–100), duplicate detection; reject invalid rows.
5. Archive previous records to academic_history.
6. Insert/update academic_records; compute enrollment if new.
7. Compute features for each student.
8. Run classification; run prediction.
9. Generate guidance.
10. Save prediction_results; update academic_records.performance_category.
11. Generate student_credentials CSV in output/.
12. Redirect to /faculty/dashboard with success message.

---

## 6.6 Dashboard Data Flow

**Faculty Dashboard:** Query students for subject, get records, compute 5-category distribution, average prediction, at-risk count, sorted at-risk list. Generate charts (pie, bar, line). Render template with data.

**Student Dashboard:** Query records for student, compute performance summary, run prediction, generate guidance, compute trend_history. Generate charts (bar, line). Render template with data.

---

## 6.7 Notification System

**Implementation:** In-dashboard alerts only. No email/SMS in current scope. Critical alerts (predicted <50) displayed prominently on faculty dashboard. Student sees guidance messages on dashboard.

**Future:** Webhook or cron for batch email; optional push notifications.

---

## 6.8 Weekly Cron Job (Optional)

For automated weekly processing: cron triggers script that (1) fetches latest records from DB; (2) runs feature engineering, classification, prediction; (3) updates prediction_results; (4) generates guidance; (5) logs. Not implemented in current deployment; manual upload triggers processing.

---

## 6.9 Data Pipelines

**Ingestion:** CSV → validation → parsing → DB insert. **Processing:** DB records → feature engineering → ML models → output. **Output:** prediction_results, guidance messages, charts. No external ETL; all within application.

---

# CHAPTER 7 – RESULTS & OUTPUTS

---

## 7.1 Faculty Dashboard Outputs

**Batch Performance Distribution:** Pie chart showing count of students in each category (Excellent, Good, Average, At Risk, Critical). Colour-coded: green for Excellent/Good, yellow for Average, red for At Risk/Critical.

**[Insert Screenshot Here – Faculty Batch Distribution Chart]**

*Figure 7.1: Faculty dashboard batch performance distribution pie chart.*

**At-Risk Student List:** Table with student name, ID, predicted score, category, guidance summary. Sorted by predicted score ascending. "View" link opens individual student view.

**[Insert Screenshot Here – Faculty At-Risk Student List]**

*Figure 7.2: Faculty dashboard at-risk student list with view links.*

**Prediction Accuracy Metrics:** Average MAE, RMSE, R² for the batch. Displayed when actual exam scores are available.

**[Insert Screenshot Here – Faculty Prediction Accuracy]**

*Figure 7.3: Faculty dashboard prediction accuracy metrics.*

**Individual Student View:** Faculty can drill down to see student's performance card, prediction chart, trend graph, and guidance messages.

**[Insert Screenshot Here – Faculty Individual Student View]**

*Figure 7.4: Faculty individual student view with performance summary and guidance.*

---

## 7.2 Student Dashboard Outputs

**Performance Summary Card:** Current attendance %, internal marks average, assignment score, weighted score, category badge.

**[Insert Screenshot Here – Student Performance Summary]**

*Figure 7.5: Student dashboard performance summary card.*

**Predicted Score Visualisation:** Bar or line chart showing predicted score with confidence interval (e.g., 68 ± 5).

**[Insert Screenshot Here – Student Predicted Score Chart]**

*Figure 7.6: Student dashboard predicted score with confidence bounds.*

**Percentile Ranking:** "You are in the top X% of your batch."

**[Insert Screenshot Here – Student Percentile]**

*Figure 7.7: Student dashboard percentile ranking.*

**Trend Graph:** Line chart showing historical scores vs predicted future trajectory.

**[Insert Screenshot Here – Student Trend Graph]**

*Figure 7.8: Student dashboard academic trajectory trend graph.*

**Guidance Messages:** List of personalised recommendations with priority and deadline.

**[Insert Screenshot Here – Student Guidance Messages]**

*Figure 7.9: Student dashboard guidance messages.*

---

## 7.3 Classification Results

**Table 7.1: Sample Classification Results**

| Student ID | Predicted Category | Confidence |
|------------|-------------------|------------|
| S001 | Excellent | 0.92 |
| S002 | Good | 0.85 |
| S003 | Average | 0.78 |
| S004 | At Risk | 0.81 |
| S005 | Critical | 0.88 |

---

## 7.4 Prediction Results

**Table 7.2: Sample Prediction Results**

| Student ID | Predicted Score | 95% CI Lower | 95% CI Upper | Actual (Later) |
|------------|-----------------|--------------|--------------|----------------|
| S001 | 85 | 80 | 90 | 87 |
| S002 | 72 | 66 | 78 | 70 |
| S003 | 58 | 52 | 64 | 55 |
| S004 | 48 | 42 | 54 | 45 |

---

## 7.5 Risk Alerts

**Table 7.3: Sample Risk Alert Output**

| Student | Priority | Message |
|---------|----------|---------|
| S003 | HIGH | Improve attendance to 85%+ to gain ~8 marks in next exam |
| S004 | CRITICAL | Immediate intervention needed—meet faculty this week |
| S005 | HIGH | Complete pending assignments before deadline to gain ~5 marks |

---

## 7.6 Guidance Messages

**Table 7.4: Sample Guidance Messages**

| Condition | Message | Priority |
|-----------|---------|----------|
| Attendance <75% | Improve attendance to 85%+ to gain ~8 marks | HIGH |
| Internal marks low | Focus on internal exam preparation | MEDIUM |
| Assignment rate <60% | Complete pending assignments before deadline | HIGH |
| Predicted 45–55 | Meet faculty this week | CRITICAL |

---

# CHAPTER 8 – TESTING & VALIDATION

---

## 8.1 Unit Testing

**Scope:** Individual functions in services (features, classification, prediction, guidance). Framework: pytest.

**Test Cases:** compute_classification_features returns 7 keys; compute_prediction_features returns 5 keys; predict_category returns valid category; predict_score returns 0–100; generate_guidance returns list with message, priority, deadline.

**Table 8.1: Unit Test Cases**

| Test ID | Function | Input | Expected Output |
|---------|----------|-------|-----------------|
| UT-1 | compute_classification_features | Valid records | Dict with 7 keys |
| UT-2 | compute_prediction_features | Valid records | Dict with 5 keys |
| UT-3 | predict_category | Valid features | One of 5 categories |
| UT-4 | predict_score | Valid features, horizon=4 | Float in [0, 100] |
| UT-5 | generate_guidance | Performance, prediction | List of dicts |

---

## 8.2 Integration Testing

**Scope:** API endpoints with mocked database. Test: POST /faculty/upload with valid CSV returns 200; GET /student/dashboard with valid session returns 200; GET /faculty/dashboard returns batch data.

**Table 8.2: Integration Test Cases**

| Test ID | Endpoint | Method | Expected |
|---------|----------|--------|----------|
| IT-1 | /login | POST | 302 redirect on success |
| IT-2 | /faculty/dashboard | GET | 200, HTML with batch data |
| IT-3 | /student/dashboard | GET | 200, HTML with performance |
| IT-4 | /faculty/upload | POST | 200, success message |

---

## 8.3 Model Accuracy Tests

**Classification:** Confusion matrix, precision, recall, F1 per class. Target: accuracy >75%.

**Table 8.3: Classification Confusion Matrix (Sample)**

|  | Predicted Excellent | Predicted Good | Predicted Average | Predicted At Risk | Predicted Critical |
|--|---------------------|----------------|-------------------|-------------------|---------------------|
| Actual Excellent | 12 | 2 | 0 | 0 | 0 |
| Actual Good | 1 | 15 | 2 | 0 | 0 |
| Actual Average | 0 | 1 | 8 | 2 | 0 |
| Actual At Risk | 0 | 0 | 1 | 5 | 1 |
| Actual Critical | 0 | 0 | 0 | 1 | 4 |

**Regression:** MAE, RMSE, R² for prediction model. Target: MAE <6, RMSE <8, R² >0.70.

**Table 8.4: Regression Metrics (Sample)**

| Metric | Target | Achieved |
|--------|--------|----------|
| MAE | <6 | 5.2 |
| RMSE | <8 | 7.1 |
| R² | >0.70 | 0.74 |
| MAPE | <10% | 8.3% |

---

## 8.4 Test Cases Table

**Table 8.5: Comprehensive Test Cases**

| ID | Category | Description | Input | Expected |
|----|----------|-------------|-------|----------|
| TC-1 | Functional | CSV upload valid | Valid CSV | Records saved, dashboard updated |
| TC-2 | Functional | CSV upload invalid | Missing columns | Error message, no save |
| TC-3 | Functional | Student login | Valid credentials | Dashboard access |
| TC-4 | Functional | Faculty login | Valid credentials | Faculty dashboard |
| TC-5 | Functional | Invalid login | Wrong password | Error message |
| TC-6 | Non-functional | Dashboard load time | N/A | <3 seconds |
| TC-7 | Non-functional | Chart render | Valid data | Chart displays |
| TC-8 | Security | Unauthorised access | No session | Redirect to login |

---

# CHAPTER 9 – DEPLOYMENT

---

## 9.1 Version Control

**GitHub:** Repository hosting. Branch strategy: main (production), develop (staging). Commit messages follow conventional commits (feat, fix, docs, refactor).

---

## 9.2 Hosting

**Railway:** Deploy FastAPI app via GitHub integration. Environment variables: DATABASE_URL, SUPABASE_URL, SUPABASE_KEY, SECRET_KEY. Build command: pip install -r requirements.txt && uvicorn main:app.

**Vercel:** Alternative for serverless deployment. Requires adapter for FastAPI (e.g., mangum).

**Supabase:** Cloud PostgreSQL. Database created via Supabase dashboard. Connection string from project settings. Migrations via SQL scripts or Supabase CLI.

---

## 9.3 CI/CD

**GitHub Actions:** Workflow on push to main: (1) run pytest; (2) deploy to Railway. Secrets: RAILWAY_TOKEN, DATABASE_URL.

**Example workflow:**

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pip install -r requirements.txt && pytest
      - name: Deploy to Railway
        run: railway up
```

---

## 9.4 Environment Setup

**Environment Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://user:pass@host:5432/db |
| SUPABASE_URL | Supabase project URL | https://xxx.supabase.co |
| SUPABASE_KEY | Supabase anon key | eyJ... |
| SECRET_KEY | Session encryption | random_string_32_chars |
| MPLBACKEND | Matplotlib backend | Agg |

---

## 9.5 Production Architecture

**[Insert Production Deployment Diagram Here]**

*Figure 9.1: Production architecture with GitHub, Railway, Supabase, and client browsers.*

Components: GitHub (source) → Railway (build, run) → Supabase (DB, Auth). Client → HTTPS → Railway. Railway → PostgreSQL connection pool → Supabase.

---

# CHAPTER 10 – ETHICS, SECURITY & PRIVACY

---

## 10.1 Role-Based Access Control

**Faculty:** Upload data, view batch analytics, view at-risk list, view individual student, export credentials. Cannot access other faculty's subjects without permission.

**Student:** View own performance, prediction, guidance, trend. Cannot access other students' data.

**Admin (optional):** Manage faculty accounts, configure rules, view audit logs. No direct access to student data for surveillance.

---

## 10.2 Audit Trails

**action_logs table:** Records user_id, action_type (upload/update/delete), entity_type (student/record/prediction), entity_id, details (JSON), timestamp. Enables: who changed what, when; compliance with data governance; dispute resolution.

---

## 10.3 Data Privacy

**Principles:** (1) Data minimisation—only required fields stored; (2) Purpose limitation—data used only for academic guidance; (3) No third-party sharing—data stays within institution; (4) Retention—records archived per policy; (5) Right to access—students can view their data.

---

## 10.4 No Surveillance

**Design:** No continuous monitoring; no keystroke tracking; no screen recording. Data collected only from faculty-uploaded assessments and attendance. Predictions are advisory, not punitive.

---

## 10.5 Explainable AI

**Measures:** Feature importance displayed; prediction explanation with contribution breakdown; guidance traceability to rules. Faculty and students can understand why a recommendation was given.

---

## 10.6 Ethical Safeguards

**Transparency:** Students informed of system purpose and data collection. **Consent:** Implicit via enrollment; explicit opt-out for non-essential features. **Bias mitigation:** Class weights for imbalanced data; regular model review. **Human-in-the-loop:** Faculty makes final decisions; system supports, does not replace.

---

# CHAPTER 11 – LIMITATIONS

---

## 11.1 Data Limitations

**Small sample size:** With ~150 students per batch, model may not generalise to larger or different institutions. **Data quality:** Predictions depend on accurate, timely attendance and marks; errors in input propagate. **Missing data:** Gaps in records (e.g., no CEM-1) reduce prediction accuracy; feature defaults (e.g., 50 for previous exam) may bias.

---

## 11.2 Model Limitations

**Temporal validity:** Model trained on historical data; curriculum or assessment changes may affect validity. **Causality:** Correlations (e.g., attendance–score) do not imply causation; guidance assumes actionable improvement. **Regime shift:** COVID-19 or policy changes may alter student behaviour; model may need retraining.

---

## 11.3 Operational Limitations

**Manual upload:** Faculty must upload CSV; no automated sync with LMS. **Single-institution:** Designed for one institution; multi-institution requires schema and auth changes. **No real-time:** Processing on upload; no live streaming of attendance.

---

## 11.4 Technical Limitations

**Chart rendering:** Matplotlib server-side; may add latency for large batches. **Scalability:** SQLite not suitable for high concurrency; PostgreSQL recommended for production. **Offline:** Web-based; requires internet for access.

---

# CHAPTER 12 – FUTURE SCOPE

---

## 12.1 LMS Integration

**Moodle/Canvas API:** Direct sync of attendance, assignments, grades. Eliminates manual CSV upload; reduces faculty workload.

---

## 12.2 Multi-Institution Support

**Tenant model:** Multi-tenant schema with institution_id; role hierarchy (super admin, institution admin, faculty, student). Separate data per institution.

---

## 12.3 Advanced Analytics

**Cohort comparison:** Compare batches across semesters. **Trend forecasting:** Predict beyond semester end. **Anomaly detection:** Flag unusual patterns (e.g., sudden drop).

---

## 12.4 Enhanced Notifications

**Email:** Weekly digest for faculty; critical alerts for at-risk students. **SMS/Push:** Optional mobile notifications. **In-app:** Real-time alerts on dashboard.

---

## 12.5 Model Improvements

**Ensemble:** Combine Random Forest with XGBoost; stacking. **Deep learning:** LSTM for temporal sequences if data volume increases. **AutoML:** Hyperparameter tuning; automated retraining.

---

## 12.6 Mobile Application

**Responsive web:** Progressive Web App (PWA) for mobile access. **Native app:** React Native or Flutter for student dashboard; push notifications.

---

# CHAPTER 13 – CONCLUSION

---

The Academic Guidance and Intelligence System (AGMIS) addresses the critical need for data-driven, proactive academic support in educational institutions. By combining traditional attendance and grade tracking with machine learning classification and regression, the system provides faculty with actionable insights and students with personalised guidance.

**Key Achievements:** AGMIS implements a five-layer architecture that separates presentation, application, analytics, data processing, and data storage. The Random Forest classifier and regressor deliver interpretable predictions with confidence intervals. The rule-based guidance engine ensures transparency and faculty control. Role-based access, audit trails, and explainability features uphold ethical and privacy standards.

**Impact:** Faculty can identify at-risk students early and allocate resources efficiently. Students receive targeted recommendations to improve performance. The system is designed for deployment in engineering colleges and universities with minimal changes to existing workflows.

**Limitations:** The system depends on data quality and manual upload; model generalisation and temporal validity require ongoing validation. Future work includes LMS integration, multi-institution support, and enhanced notification mechanisms.

In conclusion, AGMIS demonstrates that a pragmatic, interpretable AI system can augment human decision-making in academic support without compromising transparency or student autonomy. The project provides a foundation for scalable, ethical academic analytics in higher education.

---

# REFERENCES

---

1. Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32.

2. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction* (2nd ed.). Springer.

3. Supabase. (2024). *Supabase Documentation*. https://supabase.com/docs

4. FastAPI. (2024). *FastAPI Documentation*. https://fastapi.tiangolo.com

5. Scikit-learn. (2024). *User Guide: Random Forest*. https://scikit-learn.org/stable/modules/ensemble.html#forest

6. Pandas Development Team. (2024). *pandas: Powerful data structures for data analysis*. https://pandas.pydata.org

7. Matplotlib Development Team. (2024). *Matplotlib: Visualization with Python*. https://matplotlib.org

8. GDPR. (2016). Regulation (EU) 2016/679. General Data Protection Regulation.

9. Doshi-Velez, F., & Kim, B. (2017). Towards A Rigorous Science of Interpretable Machine Learning. *arXiv preprint arXiv:1702.08608*.

10. Baker, R. S., & Inventado, P. S. (2014). Educational Data Mining and Learning Analytics. In *Learning Analytics* (pp. 61–75). Springer.

---

# APPENDICES

---

## Appendix A: Sample CSV Formats

### A.1 Attendance and Marks Upload Format

```csv
student_id,name,attendance_theory,attendance_practical,internal_marks,assignment_score,week_number
S001,Rahul Sharma,85.5,90.0,72.0,78.0,1
S002,Priya Patel,78.0,82.0,68.0,70.0,1
S003,Amit Kumar,65.0,70.0,55.0,60.0,1
```

### A.2 Student Credentials Export Format

```csv
name,student_id,password
Rahul Sharma,S001,1234
Priya Patel,S002,1234
Amit Kumar,S003,1234
```

---

## Appendix B: API Documentation

### B.1 GET /faculty/dashboard

**Response:** HTML page with batch data, charts, at-risk list.

**Query Parameters:** None.

**Authentication:** Required (Faculty role).

---

### B.2 POST /faculty/upload

**Request:** multipart/form-data; file: CSV; subject_id: integer.

**Response:** 302 redirect to /faculty/dashboard with success message.

**Authentication:** Required (Faculty role).

---

### B.3 GET /student/dashboard

**Response:** HTML page with performance, prediction, guidance, trend.

**Authentication:** Required (Student role).

---

### B.4 GET /health

**Response:** {"status": "ok"}

**Authentication:** None.

---

## Appendix C: Database Schema Tables

**Table C.1: students**

| Column | Type | Constraints |
|--------|------|-------------|
| student_id | INTEGER | PRIMARY KEY |
| name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(100) | UNIQUE |
| batch | VARCHAR(20) | NOT NULL |
| department | VARCHAR(50) | NOT NULL |

**Table C.2: academic_records**

| Column | Type | Constraints |
|--------|------|-------------|
| record_id | INTEGER | PRIMARY KEY |
| enrollment_id | INTEGER | FOREIGN KEY |
| week_number | INTEGER | NOT NULL |
| attendance_theory | DECIMAL(5,2) | CHECK 0–100 |
| attendance_practical | DECIMAL(5,2) | CHECK 0–100 |
| internal_marks | DECIMAL(5,2) | CHECK 0–100 |
| assignment_score | DECIMAL(5,2) | CHECK 0–100 |
| exam_score | DECIMAL(5,2) | CHECK 0–100 |
| weighted_score | DECIMAL(5,2) | COMPUTED |
| performance_category | VARCHAR(20) | NOT NULL |

**Table C.3: prediction_results**

| Column | Type | Constraints |
|--------|------|-------------|
| prediction_id | INTEGER | PRIMARY KEY |
| student_id | INTEGER | FOREIGN KEY |
| prediction_date | DATE | NOT NULL |
| prediction_horizon | INTEGER | NOT NULL |
| predicted_score | DECIMAL(5,2) | NOT NULL |
| confidence_lower | DECIMAL(5,2) | NOT NULL |
| confidence_upper | DECIMAL(5,2) | NOT NULL |
| predicted_category | VARCHAR(20) | NOT NULL |
| model_version | VARCHAR(10) | NOT NULL |

---

## Appendix D: Algorithm Pseudocode

### D.1 Classification Algorithm

```
FUNCTION classify_student(records):
    features = compute_classification_features(records)
    model = load_model("classification_model.joblib")
    category = model.predict(features)
    return category
```

### D.2 Prediction Algorithm

```
FUNCTION predict_score(records, horizon):
    features = compute_prediction_features(records)
    model = load_model("prediction_model.joblib")
    score = model.predict(features)
    margin = 1.5 * MAE_from_test
    lower = max(0, score - margin)
    upper = min(100, score + margin)
    return (score, lower, upper)
```

### D.3 Guidance Rule Engine

```
FUNCTION generate_guidance(performance, prediction, features):
    rules = load_rules()
    guidance_list = []
    FOR each rule IN rules:
        IF rule.condition_matches(performance, prediction, features):
            message = rule.message
            impact = estimate_impact(rule, features)
            guidance_list.append({message, rule.priority, rule.deadline})
    RETURN guidance_list
```

---

# END OF DOCUMENT

---

**Document Statistics:** Approximately 85–95 pages when formatted per specifications (Times New Roman 12pt, 1.5 line spacing, justified).

**Screenshot Placement Guide:** For maximum impact, add screenshots at the following locations:

1. **Figure 7.1** – Faculty batch distribution pie chart (after faculty logs in)
2. **Figure 7.2** – Faculty at-risk student list table
3. **Figure 7.3** – Faculty prediction accuracy metrics (if available)
4. **Figure 7.4** – Faculty individual student view (click "View" on any student)
5. **Figure 7.5** – Student performance summary card
6. **Figure 7.6** – Student predicted score chart
7. **Figure 7.7** – Student percentile ranking
8. **Figure 7.8** – Student trend graph (academic trajectory)
9. **Figure 7.9** – Student guidance messages section

**How to capture:** Run the application locally, log in as faculty and student, navigate to each dashboard/view, and use Print Screen or a screenshot tool (e.g., Snipping Tool, Windows+Shift+S) to capture each view. Insert images at the marked [Insert Screenshot Here] locations.
