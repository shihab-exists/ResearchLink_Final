# DBMS Lab Normalization Report (Streamlined)
## Mini Project: ResearchLink Database Layout

This document details the database normalization process (from 1NF to 3NF) applied to the **ResearchLink** schema to ensure relational efficiency, remove redundant records, and prevent update/deletion anomalies.

---

### 1. First Normal Form (1NF)
**Requirement:** All column values must be atomic (no multi-valued attributes or repeating groups), and each table must have a unique identifier (Primary Key).

*   **Problem resolved:** Originally, a student might want to store a list of technical skills or a teacher might list multiple research interests as comma-separated strings inside a single column (e.g., `"Python, SQL, PyTorch"`). This violates 1NF because values are not atomic, making structured SQL queries or search indexes on individual skills impossible.
*   **1NF Solution:** We created separate lookup tables for `skills` and `research_fields`. Because a student can have multiple skills and a skill can belong to multiple students, we resolved this Many-to-Many relationship by creating junction tables: `student_skills` and `teacher_interests`.
*   All columns in our schema now contain only single-valued atomic values.

---

### 2. Second Normal Form (2NF)
**Requirement:** The database must be in 1NF, and all non-key columns must be fully functionally dependent on the entire primary key (no partial dependencies on composite keys).

*   **Problem resolved:** In composite primary key tables, such as the junction table `student_skills(student_id, skill_id)`, if we added any attribute like `student_cgpa` directly to that table, that attribute would only depend on *part* of the primary key (`student_id`), which violates 2NF and leads to duplicated records.
*   **2NF Solution:** In our junction tables (`student_skills` and `teacher_interests`), the only fields present are the composite key columns themselves (`student_id`, `skill_id`) and (`teacher_id`, `researchfield_id`). All non-key attributes of the student (such as `cgpa`, `bio`, `roll_no`) are kept strictly inside the `students` table, depending fully on the single primary key `id`.
*   All single-key tables are automatically in 2NF, and our composite key tables have no partial dependencies, meaning our schema satisfies 2NF.

---

### 3. Third Normal Form (3NF)
**Requirement:** The database must be in 2NF, and there must be no transitive dependencies (non-key columns must depend only on the primary key, and not on other non-key columns).

*   **Problem resolved:** If we had placed department attributes (e.g., `dept_name` and `dept_code`) directly inside the `students` or `teachers` tables, we would have a transitive dependency:
    `student_id -> dept_id -> dept_name`.
    If a department name changed, we would have to run update queries on multiple student records. If a department currently had no students, we would lose its metadata entirely (deletion anomaly).
*   **3NF Solution:** We factored out the departments into their own independent lookup table `departments` with a unique key `id`. The `students` and `teachers` tables only store a foreign key reference (`dept_id`).
    *   `student_id -> dept_id` (in `students` table)
    *   `dept_id -> dept_name, dept_code` (in `departments` table)
*   This fully eliminates transitive dependencies, satisfying the strict requirements of 3NF!

---

### 4. Normalized Schema Entities Mapping

| Table Name | Primary Key | Foreign Keys | Constraints | Normalized Level |
| :--- | :--- | :--- | :--- | :--- |
| **departments** | `id` | None | `name` (Unique), `code` (Unique) | 3NF |
| **skills** | `id` | None | `name` (Unique) | 3NF |
| **research_fields**| `id` | None | `name` (Unique) | 3NF |
| **students** | `id` | `id` -> `auth_user(id)`, `dept_id` -> `departments(id)` | `roll_no` (Unique), `cgpa` (CHECK 0.00 to 4.00) | 3NF |
| **teachers** | `id` | `id` -> `auth_user(id)`, `dept_id` -> `departments(id)` | `is_approved` (Boolean) | 3NF |
| **student_skills** | `(student_id, skill_id)` | Refs `students(id)`, `skills(id)` | Cascade Deletes | 3NF |
| **teacher_interests**| `(teacher_id, researchfield_id)` | Refs `teachers(id)`, `research_fields(id)` | Cascade Deletes | 3NF |
| **projects** | `id` | `teacher_id` -> `teachers(id)` | `status` (CHECK 'Open', 'Closed') | 3NF |
| **applications** | `id` | `project_id`, `student_id`, `teacher_id` | `status` (CHECK 'Pending', 'Accepted', 'Rejected') | 3NF |
| **messages** | `id` | `sender_id`, `receiver_id` -> `auth_user` | None | 3NF |
