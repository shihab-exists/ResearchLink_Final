-- ResearchLink Simplified Database Schema (3NF Normalized)
-- Designed for CSE DBMS Lab Mini Project

USE researchlink;

-- ----------------------------------------------------
-- TABLES (DDL)
-- ----------------------------------------------------

-- 1. Departments Table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(10) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Research Fields Table (e.g. AI, NLP, Robotics)
CREATE TABLE IF NOT EXISTS research_fields (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Skills Table (e.g. Python, SQL, C++)
CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Students Profile Table (One-to-One with auth_user)
CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY,
    dept_id INT,
    roll_no VARCHAR(20) NOT NULL UNIQUE,
    cgpa DECIMAL(3,2) NOT NULL CHECK (cgpa >= 0.00 AND cgpa <= 4.00),
    bio TEXT,
    cv_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES departments(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Teachers Profile Table (One-to-One with auth_user)
CREATE TABLE IF NOT EXISTS teachers (
    id INT PRIMARY KEY,
    dept_id INT,
    designation VARCHAR(100) NOT NULL,
    room_no VARCHAR(50),
    is_approved BOOLEAN DEFAULT FALSE,
    bio TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES departments(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Student Skills Junction Table (Many-to-Many)
CREATE TABLE IF NOT EXISTS student_skills (
    student_id INT NOT NULL,
    skill_id INT NOT NULL,
    PRIMARY KEY (student_id, skill_id),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Teacher Research Interests Junction Table (Many-to-Many)
CREATE TABLE IF NOT EXISTS teacher_interests (
    teacher_id INT NOT NULL,
    researchfield_id INT NOT NULL,
    PRIMARY KEY (teacher_id, researchfield_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (researchfield_id) REFERENCES research_fields(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Projects / Thesis Vacancies posted by Teachers
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT,
    teacher_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'Open' CHECK (status IN ('Open', 'Closed')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Applications (Collaboration & Supervision Proposals)
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NULL,
    student_id INT NOT NULL,
    teacher_id INT NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Accepted', 'Rejected')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. Direct Messages
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    message_text TEXT NOT NULL,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES auth_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ----------------------------------------------------
-- INDEXES
-- ----------------------------------------------------
CREATE INDEX idx_students_roll_no ON students(roll_no);
CREATE INDEX idx_students_cgpa ON students(cgpa);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_applications_status ON applications(status);


-- ----------------------------------------------------
-- VIEWS
-- ----------------------------------------------------

-- View 1: Supervisor workload aggregates
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

-- View 2: Student complete contact details
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


-- ----------------------------------------------------
-- TRIGGERS
-- ----------------------------------------------------
DELIMITER //

-- Enforce Business Constraint: A student can only have ONE assigned supervisor at any time!
-- If an update attempts to set status = 'Accepted' for a student who already has an 'Accepted' application elsewhere, throw a custom database error.
DROP TRIGGER IF EXISTS trig_prevent_multiple_supervisors_insert //
CREATE TRIGGER trig_prevent_multiple_supervisors_insert
BEFORE INSERT ON applications
FOR EACH ROW
BEGIN
    DECLARE accepted_count INT;
    IF NEW.status = 'Accepted' THEN
        SELECT COUNT(*) INTO accepted_count 
        FROM applications 
        WHERE student_id = NEW.student_id AND status = 'Accepted';
        
        IF accepted_count > 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ERROR: This student already has an assigned thesis supervisor.';
        END IF;
    END IF;
END //

DROP TRIGGER IF EXISTS trig_prevent_multiple_supervisors_update //
CREATE TRIGGER trig_prevent_multiple_supervisors_update
BEFORE UPDATE ON applications
FOR EACH ROW
BEGIN
    DECLARE accepted_count INT;
    IF NEW.status = 'Accepted' AND OLD.status <> 'Accepted' THEN
        SELECT COUNT(*) INTO accepted_count 
        FROM applications 
        WHERE student_id = NEW.student_id AND status = 'Accepted';
        
        IF accepted_count > 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ERROR: This student already has an assigned thesis supervisor.';
        END IF;
    END IF;
END //

DELIMITER ;


-- ----------------------------------------------------
-- STORED PROCEDURES
-- ----------------------------------------------------
DELIMITER //

-- Stored Procedure to Approve teacher supervisor profile
DROP PROCEDURE IF EXISTS sp_approve_teacher //
CREATE PROCEDURE sp_approve_teacher(IN t_id INT)
BEGIN
    UPDATE teachers 
    SET is_approved = TRUE 
    WHERE id = t_id;
END //

DELIMITER ;
