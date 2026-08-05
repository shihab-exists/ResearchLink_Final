# ResearchLink 
### A Research Collaboration & Faculty Supervision Management System
**Final DBMS Lab Mini Project (Strictly Normalized to 3NF)**

ResearchLink is a clean, student-built web application designed to match senior Computer Science & Engineering students with faculty supervisors for thesis, design projects, and collaborative research tracks.

The system is designed with **quality over quantity**, focusing on high-integrity database principles, robust triggers, transactional stored procedures, and custom database views integrated directly with a **Python Django** backend and a **Vanilla CSS / Bootstrap** frontend.

---

## 🚀 Tech Stack
*   **Backend:** Python Django (v4.2)
*   **Database:** MySQL / MariaDB (ACID-compliant)
*   **Frontend:** HTML5, CSS3, ES6 Vanilla JS, Bootstrap
*   **CSS Sheets:** Clean, organized per-page stylesheets (`styles.css`, `login.css`, `dashboard.css`, `profile.css`)

---

## 🔑 Seeded Demo Accounts (For Viva & Evaluation)
You can log in and instantly demo the workflow using these seeded credentials:

| Role | Username | Password | Notes / Status |
| :--- | :--- | :--- | :--- |
| **System Admin** | `admin` | `admin123` | Can view overall system statistics, track recent registrations, and approve faculty supervisors via stored procedures. |
| **Student** | `student1` | `student123` | Active student in EEE dept. Has skills checklist uploaded, looking for supervisors. |
| **Student (High GPA)**| `student2` | `student123` | High CGPA (3.85) in EEE. Eligible to submit collaboration proposals. |
| **Supervisor (Approved)**| `teacher1` | `teacher123` | Faculty Professor in CSE dept. Can post project vacancies and review student applications. |
| **Supervisor (Pending)** | `teacher18` | `teacher123` | Faculty Assistant Prof in MAT dept. Currently pending admin review. |

---

## 📂 Streamlined Folder Structure
```text
ResearchLink/
│
├── venv/                 # Virtual environment (ignored in git)
├── researchlink/         # Django project base settings and router apps
│   ├── accounts/         # User registrations, secure logins, and session handling
│   ├── students/         # Student bios, skills checklists, and search directory
│   ├── teachers/         # Faculty supervisors catalog and interests mappings
│   ├── projects/         # Thesis vacancies posting and supervisor applications
│   ├── messaging/        # Simple direct peer-to-peer message exchanges
│   └── dashboard/        # Dashboard stats router & administrative command center
│
├── requirements.txt      # Python library dependencies
├── schema.sql            # Master MySQL DDL (CREATE, VIEWS, TRIGGERS, PROCEDURES)
├── populate_db.py        # Database seeding script (20+ realistic records per table)
├── README.md             # Project documentation and manual guide
├── .env                  # Environment configurations and database keys
└── .gitignore            # Git exclusions
```

---

## 📊 Database Entities (3NF Normalized Schema)
To maintain strict database integrity, our model mapping is designed around 9 primary entities and junction relationships:
1.  **`departments`** (`id` PK, `name`, `code`)
2.  **`research_fields`** (`id` PK, `name`)
3.  **`skills`** (`id` PK, `name`)
4.  **`students`** (`id` PK references `auth_user`, `dept_id` FK, `roll_no` [Unique], `cgpa`, `bio`, `cv_url`)
5.  **`teachers`** (`id` PK references `auth_user`, `dept_id` FK, `designation`, `room_no`, `is_approved` [Boolean], `bio`)
6.  **`student_skills`** (`student_id` FK, `skill_id` FK) [Junction table for skills checklists]
7.  **`teacher_interests`** (`teacher_id` FK, `researchfield_id` FK) [Junction table for research areas]
8.  **`projects`** (`id` PK, `title`, `description`, `requirements`, `teacher_id` FK, `status`)
9.  **`applications`** (`id` PK, `project_id` FK, `student_id` FK, `teacher_id` FK, `message`, `status`)
10. **`messages`** (`id` PK, `sender_id` FK, `receiver_id` FK, `message_text`, `sent_at`)

---

## ⚡ Advanced Database-Level Logic (Evaluator Highlights)

### 1. Database Views
*   `view_teacher_workload`: Aggregates the count of currently accepted student supervisions for each faculty member. Used directly in the Admin Dashboard stats page.
*   `view_student_details`: Flattens student user accounts, departments, and GPAs into a single virtual log for standard directory searches.

### 2. Database Triggers (Advanced Integrity Constraint)
*   `trig_prevent_multiple_supervisors_insert` / `trig_prevent_multiple_supervisors_update`: 
    *   **Enforces the safety rule:** *A student can only have one assigned thesis supervisor at any given time.*
    *   If a student is accepted by a supervisor, any other concurrent application or status change to "Accepted" is automatically blocked by the database with a `SIGNAL SQLSTATE '45000'` database-level error.
    *   Our Django views catch this trigger error natively and print a user-friendly flash alert to the user.

### 3. Stored Procedures
*   `sp_approve_teacher(t_id)`: Approves a pending supervisor account at the database level. Called dynamically by the administrator with a single button click.

---

## 🛠️ Local Server Setup & Running Guide

Follow these steps to run the project locally on your machine:

1.  **Start MySQL Server:** Ensure MySQL/MariaDB server is active and listening on port `3306`.
2.  **Create the Database:** Create a blank database schema inside your SQL client:
    ```sql
    CREATE DATABASE researchlink CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```
3.  **Import Database Schema:** Import the DDL script to create the normalized tables, views, stored procedures, and triggers:
    ```bash
    mysql -u root researchlink < schema.sql
    ```
4.  **Set Up Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On Linux / Mac:
    source venv/bin/activate
    ```
5.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
6.  **Apply Django migrations:**
    ```bash
    python manage.py migrate
    ```
7.  **Seed Database Data:** Populate the database with 20+ records of realistic mock university records:
    ```bash
    python populate_db.py
    ```
8.  **Run Development Server:**
    ```bash
    python manage.py runserver
    ```
    Navigate to `http://127.0.0.1:8000/` inside your web browser.
