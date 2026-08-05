-- ResearchLink Database Sample Seed Data
-- Enforces: 20+ realistic records for all static lookup tables
-- Mini Project Lab Deliverable

USE researchlink;

-- ----------------------------------------------------
-- 1. SEED DEPARTMENTS (21 Records)
-- ----------------------------------------------------
INSERT INTO departments (id, name, code) VALUES
(1, 'Computer Science & Engineering', 'CSE'),
(2, 'Electrical & Electronic Engineering', 'EEE'),
(3, 'Mechanical Engineering', 'ME'),
(4, 'Civil Engineering', 'CE'),
(5, 'Industrial & Production Engineering', 'IPE'),
(6, 'Software Engineering', 'SWE'),
(7, 'Information Technology', 'IT'),
(8, 'Biomedical Engineering', 'BME'),
(9, 'Textile Engineering', 'TE'),
(10, 'Chemical Engineering', 'ChE'),
(11, 'Pharmacy', 'PHR'),
(12, 'Mathematics', 'MAT'),
(13, 'Physics', 'PHY'),
(14, 'Chemistry', 'CHM'),
(15, 'Architecture', 'ARC'),
(16, 'Business Administration', 'BBA'),
(17, 'Economics', 'ECO'),
(18, 'English', 'ENG'),
(19, 'Environmental Science', 'EVS'),
(20, 'Law & Justice', 'LAW'),
(21, 'Statistics', 'STA')
ON DUPLICATE KEY UPDATE name=VALUES(name), code=VALUES(code);


-- ----------------------------------------------------
-- 2. SEED RESEARCH INTEREST FIELDS (21 Records)
-- ----------------------------------------------------
INSERT INTO research_fields (id, name) VALUES
(1, 'Artificial Intelligence'),
(2, 'Natural Language Processing'),
(3, 'Machine Learning'),
(4, 'Computer Vision'),
(5, 'Cyber Security'),
(6, 'Blockchain Technology'),
(7, 'Cloud Computing'),
(8, 'Internet of Things (IoT)'),
(9, 'Bioinformatics'),
(10, 'Data Science & Analytics'),
(11, 'Quantum Computing'),
(12, 'Software Engineering'),
(13, 'Robotics & Control'),
(14, 'Nanotechnology'),
(15, 'Renewable Energy'),
(16, 'VLSI & Embedded Systems'),
(17, 'Digital Signal Processing'),
(18, 'Smart Grid Systems'),
(19, 'Wireless Communication'),
(20, 'Material Science'),
(21, 'Human-Computer Interaction')
ON DUPLICATE KEY UPDATE name=VALUES(name);


-- ----------------------------------------------------
-- 3. SEED SKILLS (21 Records)
-- ----------------------------------------------------
INSERT INTO skills (id, name) VALUES
(1, 'Python'),
(2, 'SQL'),
(3, 'C++'),
(4, 'Java'),
(5, 'PyTorch'),
(6, 'TensorFlow'),
(7, 'Git & GitHub'),
(8, 'R Programming'),
(9, 'MATLAB'),
(10, 'HTML5 & CSS3'),
(11, 'Vanilla JavaScript'),
(12, 'Linux/Bash'),
(13, 'AWS Cloud'),
(14, 'Docker Containers'),
(15, 'Node.js'),
(16, 'Spring Boot'),
(17, 'Unity 3D Engine'),
(18, 'LaTeX Document Prep'),
(19, 'AutoCAD Design'),
(20, 'Tableau Data Viz'),
(21, 'Microsoft Excel Advanced')
ON DUPLICATE KEY UPDATE name=VALUES(name);


-- --------------------------------------------------------------------------------
-- LAB REPORT NOTE: 
-- For users (auth_user), student profiles (students), and teacher profiles (teachers),
-- we seed them dynamically via the Django `populate_db.py` script. 
-- This guarantees that password hashes (e.g. PBKDF2 algorithm) conform to Django's 
-- security middleware, allowing you to log in with active test users (like `student1` or `teacher1`).
-- --------------------------------------------------------------------------------
SELECT 'Seeding lookup tables completed!' AS status;
