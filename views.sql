-- ResearchLink Simplified Database Views
-- DBMS Lab Mini Project

USE researchlink;

-- ----------------------------------------------------
-- VIEW 1: view_teacher_workload
-- Enforces: JOIN, LEFT JOIN, GROUP BY, aggregates (COUNT)
-- Purpose: Real-time query listing supervisor workload. Used directly by Admin Dashboard.
-- ----------------------------------------------------
CREATE OR REPLACE VIEW view_teacher_workload AS
SELECT 
    t.id AS teacher_id,
    u.first_name,
    u.last_name,
    d.name AS dept_name,
    t.designation,
    COUNT(a.id) AS accepted_supervisions
FROM teachers t
JOIN auth_user u ON t.id = u.id
LEFT JOIN departments d ON t.dept_id = d.id
LEFT JOIN applications a ON t.id = a.teacher_id AND a.status = 'Accepted'
GROUP BY t.id, u.first_name, u.last_name, d.name, t.designation;


-- ----------------------------------------------------
-- VIEW 2: view_student_details
-- Enforces: JOIN, LEFT JOIN
-- Purpose: Integrates base login details with student bio-statistics.
-- ----------------------------------------------------
CREATE OR REPLACE VIEW view_student_details AS
SELECT 
    s.id AS student_id,
    u.username,
    u.first_name,
    u.last_name,
    u.email,
    s.roll_no,
    s.cgpa,
    d.name AS dept_name,
    s.bio,
    s.cv_url
FROM students s
JOIN auth_user u ON s.id = u.id
LEFT JOIN departments d ON s.dept_id = d.id;
