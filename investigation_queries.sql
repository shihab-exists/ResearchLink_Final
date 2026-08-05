-- ResearchLink DBMS Lab Mini Project
-- EP4: Analytical Investigation Queries
-- These queries are designed for report-ready output and project evaluation / viva!

USE researchlink;

-- --------------------------------------------------------------------------------
-- Query 1: Top Supervisor
-- Identifies the supervisor who has accepted the highest number of collaboration requests.
-- --------------------------------------------------------------------------------
SELECT 
    t.id AS supervisor_id,
    u.first_name,
    u.last_name,
    d.code AS department,
    COUNT(a.id) AS accepted_count
FROM teachers t
JOIN auth_user u ON t.id = u.id
JOIN departments d ON t.dept_id = d.id
JOIN applications a ON t.id = a.teacher_id
WHERE a.status = 'Accepted'
GROUP BY t.id, u.first_name, u.last_name, d.code
ORDER BY accepted_count DESC
LIMIT 1;


-- --------------------------------------------------------------------------------
-- Query 2: Most Active Department
-- Finds departments ranked by the count of active research project listings.
-- --------------------------------------------------------------------------------
SELECT 
    d.id AS dept_id,
    d.name AS department_name,
    d.code AS department_code,
    COUNT(p.id) AS total_projects
FROM departments d
LEFT JOIN teachers t ON d.id = t.dept_id
LEFT JOIN projects p ON t.id = p.teacher_id
GROUP BY d.id, d.name, d.code
HAVING total_projects > 0
ORDER BY total_projects DESC;


-- --------------------------------------------------------------------------------
-- Query 3: Most Requested Research Field
-- Determines which research fields are most sought after by combining teacher interests 
-- with a count of applications linked to projects.
-- --------------------------------------------------------------------------------
SELECT 
    rf.id AS field_id,
    rf.name AS field_name,
    COUNT(ti.teacher_id) AS supervisor_interests,
    (
        SELECT COUNT(a.id) 
        FROM applications a 
        JOIN projects p ON a.project_id = p.id
        WHERE p.title LIKE CONCAT('%', rf.name, '%') OR p.description LIKE CONCAT('%', rf.name, '%')
    ) AS application_keyword_matches
FROM research_fields rf
LEFT JOIN teacher_interests ti ON rf.id = ti.researchfield_id
GROUP BY rf.id, rf.name
ORDER BY supervisor_interests DESC, application_keyword_matches DESC
LIMIT 5;


-- --------------------------------------------------------------------------------
-- Query 4: Average Accepted Applications
-- Calculates the average number of accepted supervision requests per teacher profile.
-- Uses a subquery to aggregate accepted applications.
-- --------------------------------------------------------------------------------
SELECT 
    ROUND(AVG(accepted_count), 2) AS average_accepted_supervisions
FROM (
    SELECT 
        t.id,
        COUNT(a.id) AS accepted_count
    FROM teachers t
    LEFT JOIN applications a ON t.id = a.teacher_id AND a.status = 'Accepted'
    GROUP BY t.id
) AS teacher_acceptances;


-- --------------------------------------------------------------------------------
-- Query 5: Teacher Workload Breakdown
-- Lists teachers, their departments, their active projects, and accepted supervision requests.
-- Uses complex outer joins and Group By.
-- --------------------------------------------------------------------------------
SELECT 
    u.first_name,
    u.last_name,
    d.code AS dept_code,
    t.designation,
    COUNT(DISTINCT p.id) AS active_projects_posted,
    COUNT(DISTINCT CASE WHEN a.status = 'Accepted' THEN a.id END) AS supervised_students_count
FROM teachers t
JOIN auth_user u ON t.id = u.id
LEFT JOIN departments d ON t.dept_id = d.id
LEFT JOIN projects p ON t.id = p.teacher_id AND p.status = 'Open'
LEFT JOIN applications a ON t.id = a.teacher_id
GROUP BY t.id, u.first_name, u.last_name, d.code, t.designation
ORDER BY supervised_students_count DESC, active_projects_posted DESC;


-- --------------------------------------------------------------------------------
-- Query 6: Student Participation & Engagement
-- Displays students alongside their CGPA, department, skills count, and submitted applications count.
-- Demonstrates nested queries and aggregate functions.
-- --------------------------------------------------------------------------------
SELECT 
    s.roll_no,
    u.first_name,
    u.last_name,
    d.code AS dept_code,
    s.cgpa,
    (SELECT COUNT(*) FROM student_skills ss WHERE ss.student_id = s.id) AS skills_uploaded,
    COUNT(a.id) AS supervision_requests_sent
FROM students s
JOIN auth_user u ON s.id = u.id
LEFT JOIN departments d ON s.dept_id = d.id
LEFT JOIN applications a ON s.id = a.student_id
GROUP BY s.id, s.roll_no, u.first_name, u.last_name, d.code, s.cgpa
ORDER BY s.cgpa DESC, supervision_requests_sent DESC;


-- --------------------------------------------------------------------------------
-- Query 7: Monthly Project Creation Rate
-- Tracks the frequency of research opportunity postings by month.
-- --------------------------------------------------------------------------------
SELECT 
    DATE_FORMAT(created_at, '%Y-%m') AS creation_month,
    COUNT(id) AS projects_created
FROM projects
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY creation_month DESC;


-- --------------------------------------------------------------------------------
-- Query 8: High CGPA Students without a Supervisor
-- Displays students with CGPA >= 3.50 who have no 'Accepted' supervision applications.
-- --------------------------------------------------------------------------------
SELECT 
    s.roll_no,
    u.first_name,
    u.last_name,
    s.cgpa,
    d.code AS dept_code
FROM students s
JOIN auth_user u ON s.id = u.id
LEFT JOIN departments d ON s.dept_id = d.id
WHERE s.cgpa >= 3.50 
  AND s.id NOT IN (
      SELECT student_id 
      FROM applications 
      WHERE status = 'Accepted'
  )
ORDER BY s.cgpa DESC;


-- --------------------------------------------------------------------------------
-- Query 9: Department Skill Density
-- Find which department has the highest count of registered student skills.
-- Shows deep nesting and GROUP BY ... HAVING.
-- --------------------------------------------------------------------------------
SELECT 
    d.code AS dept_code,
    COUNT(ss.skill_id) AS total_skills_held,
    ROUND(AVG(s.cgpa), 2) AS avg_student_cgpa
FROM departments d
JOIN students s ON d.id = s.dept_id
JOIN student_skills ss ON s.id = ss.student_id
GROUP BY d.id, d.code
HAVING total_skills_held > 5
ORDER BY total_skills_held DESC;
