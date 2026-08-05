-- ResearchLink Database Transactions & Stored Procedures
-- DBMS Lab Mini Project

USE researchlink;

DELIMITER //

-- --------------------------------------------------------------------------------
-- STORED PROCEDURE 1: sp_approve_teacher
-- Purpose: Safely sets a teacher profile status to approved. Runs when the Admin
--          clicks "Approve" on the admin control panel.
-- --------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_approve_teacher //
CREATE PROCEDURE sp_approve_teacher(IN t_id INT)
BEGIN
    UPDATE teachers 
    SET is_approved = TRUE 
    WHERE id = t_id;
END //

DELIMITER ;


-- --------------------------------------------------------------------------------
-- DEMONSTRATION WORKFLOW: Explicit Transaction with Rollback
-- Use this manual block during your lab presentation to demonstrate ACID attributes!
-- --------------------------------------------------------------------------------

/*
-- STEP A: Start the Transaction
START TRANSACTION;

-- STEP B: Add a mock project opportunity
INSERT INTO projects (title, description, requirements, teacher_id, status)
VALUES ('Quantum Photonics', 'Simulating photonic circuit paths in CMOS.', 1, 'Open');

-- STEP C: Query to verify existence inside this isolation session
SELECT * FROM projects WHERE title = 'Quantum Photonics';

-- STEP D: Perform Rollback (Cancel the actions)
ROLLBACK;

-- STEP E: Query again (Table returns empty, verifying rollback consistency!)
SELECT * FROM projects WHERE title = 'Quantum Photonics';
*/
