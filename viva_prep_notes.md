# DBMS Lab Viva Preparation Notes
## Project: ResearchLink (Simplified & Streamlined)

These preparation notes are customized for a CSE student defending their final lab project in front of an external evaluator or course instructor.

---

### Part 1: Core Database & SQL Questions

#### Q1: What is the primary difference between a View and a Table? How did you use Views in ResearchLink?
*   **Answer:** A table stores records physically on disk. A view is a virtual table—it does not store data itself; rather, it is a saved, compiled SQL query. Whenever a view is queried, the database executes its underlying query on-the-fly.
*   **Our Project Usage:** We created two views:
    1.  `view_teacher_workload`: Aggregates the number of accepted student applications per faculty.
    2.  `view_student_details`: Combines the `students` profile and Django's core `auth_user` credentials into one query.
    *   We query `view_teacher_workload` directly in our Django Admin Dashboard using a raw SQL command to show real-time workload stats.

#### Q2: What are Triggers, and why did you use them instead of doing everything in Django?
*   **Answer:** A trigger is a set of SQL statements that automatically execute (or "fire") in response to a specific event (INSERT, UPDATE, or DELETE) on a table. 
*   We used triggers to guarantee data integrity at the database level. Even if someone bypasses the Django web portal and inserts records directly into MySQL, the triggers enforce our rules:
    *   `trig_prevent_multiple_supervisors_insert` / `trig_prevent_multiple_supervisors_update`: BEFORE INSERT or BEFORE UPDATE on `applications`. If a student has an existing application with status = 'Accepted', the trigger throws a custom database error using `SIGNAL SQLSTATE '45000'`.
    *   This guarantees that a student can only ever have **ONE** active accepted supervisor across the entire database!

#### Q3: Explain what Stored Procedures are, and detail how you called them inside Django.
*   **Answer:** A stored procedure is a precompiled collection of SQL statements stored in the database. It can accept input parameters and execute database actions. It improves performance because the database doesn't need to recompile the query, and it keeps logic secure.
*   **Our Project Usage:** We created the stored procedure `sp_approve_teacher(t_id)` to approve a pending supervisor profile:
    ```sql
    CREATE PROCEDURE sp_approve_teacher(IN t_id INT)
    BEGIN
        UPDATE teachers SET is_approved = TRUE WHERE id = t_id;
    END
    ```
    *   We integrated it in Django views using `connection.cursor()`:
        ```python
        with connection.cursor() as cursor:
            cursor.callproc('sp_approve_teacher', [teacher_id])
        ```

#### Q4: Why are Indexes important? Which columns did you index and why?
*   **Answer:** Indexes are lookup trees (B-Trees in InnoDB) that speed up search queries on specific columns, transforming a linear $O(N)$ full-table scan into a logarithmic $O(\log N)$ search. 
*   **Our Project Usage:** We created indexes on columns frequently used in WHERE, JOIN, and ORDER BY clauses:
    *   `idx_students_roll_no` (speeds up student searches)
    *   `idx_students_cgpa` (speeds up CGPA filtering/rankings)
    *   `idx_projects_status` (speeds up open vacancy checks)
    *   `idx_applications_status` (speeds up pending proposal filtering)

---

### Part 2: Django & Tech Stack Questions

#### Q5: How did you bridge your raw MySQL tables with Django's ORM?
*   **Answer:** We wrote standard Django models but customized their table mappings using the `db_table` option inside the `class Meta` subclass. By setting `db_table = 'students'`, `db_table = 'projects'`, etc., we forced Django's ORM to read and write directly to our hand-crafted, normalized SQL tables instead of generating default hashed table names.

#### Q6: Why did you use Django Session variables to track user roles?
*   **Answer:** Standard Django auth handles logins, but since we have multiple distinct user profiles (Student and Teacher) linking to the same `User` table, we needed an efficient way to check roles during views and template renders.
*   During login, we query which profile table the user exists in, and save `'student'` or `'teacher'` in `request.session['user_role']`. In templates, we can simply write `{% if request.session.user_role == 'student' %}` to hide or show matching elements dynamically.

#### Q7: How does your application capture database trigger error signals?
*   **Answer:** In our Django view, when an insertion or update is made (such as accepting an application or applying to a project), we wrap the save action inside a standard `try-except` block:
    ```python
    try:
        app.save()
    except (utils.InternalError, utils.OperationalError, IntegrityError) as e:
        # Catch and display the database trigger's SIGNAL error message
    ```
    *   This beautifully shows the division of labor between application-tier logic and database-tier constraints!
