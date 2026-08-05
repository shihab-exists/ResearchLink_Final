-- ResearchLink Simplified Database Triggers
-- DBMS Lab Mini Project

USE researchlink;

DELIMITER //

-- --------------------------------------------------------------------------------
-- TRIGGER 1: trig_prevent_multiple_supervisors_insert
-- Timing: BEFORE INSERT
-- Table: applications
-- Purpose: Enforces the rule that a student cannot be assigned to more than 
--          one supervisor at any time. Throws a database-level error if violated.
-- --------------------------------------------------------------------------------
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


-- --------------------------------------------------------------------------------
-- TRIGGER 2: trig_prevent_multiple_supervisors_update
-- Timing: BEFORE UPDATE
-- Table: applications
-- Purpose: Monitors changes during faculty review decisions. If a supervisor attempts
--          to accept a student who was already locked in with another teacher,
--          the database aborts the update transaction immediately.
-- --------------------------------------------------------------------------------
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
