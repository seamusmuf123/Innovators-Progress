DROP DATABASE IF EXISTS progress;
CREATE DATABASE progress;
USE progress;


DROP TABLE IF EXISTS User;
CREATE TABLE User (
   user_ID INT AUTO_INCREMENT NOT NULL,
   name VARCHAR(50),
   email VARCHAR(75) UNIQUE,
   passwordHash VARCHAR(128) NOT NULL,
   address VARCHAR(128),
   gym_location VARCHAR(50) NOT NULL,
   PRIMARY KEY (user_ID)
);


DROP TABLE IF EXISTS Goal;
CREATE TABLE Goal (
   user_ID INT,
   goal_name VARCHAR(50),
   task VARCHAR(75),
   tracking VARCHAR(100),
   records TEXT,
   reminders VARCHAR(100),
   PRIMARY KEY (user_ID, goal_name),
   FOREIGN KEY (user_ID) REFERENCES User (user_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


DROP TABLE IF EXISTS Membership;
CREATE TABLE Membership (
 membership_ID INT AUTO_INCREMENT NOT NULL,
 status VARCHAR(50),
 start_date DATETIME NOT NULL,
 end_date DATETIME NOT NULL,
 billing INT,
 PRIMARY KEY (membership_ID)
);


DROP TABLE IF EXISTS All_Memberships;


DROP TABLE IF EXISTS Report;
CREATE TABLE Report (
   report_ID INT AUTO_INCREMENT NOT NULL,
   title VARCHAR(75),
   checklist TEXT,
   completed_goals TEXT,
   uncompleted_goals TEXT,
   work_efficiency BLOB,
   time_based_summary TEXT NOT NULL,
   PRIMARY KEY (report_ID)
);


DROP TABLE IF EXISTS Plan;
CREATE TABLE Plan (
   plan_ID INT AUTO_INCREMENT NOT NULL,
   title VARCHAR(75),
   workout_rec TEXT,
   diet TEXT,
   PRIMARY KEY (plan_ID)
);


DROP TABLE IF EXISTS Analysis_Team;
CREATE TABLE Analysis_Team (
   team_ID INT AUTO_INCREMENT NOT NULL,
   maintenance_task TEXT,
   requests TEXT,
   PRIMARY KEY (team_ID)
);


DROP TABLE IF EXISTS `system`;
CREATE TABLE `system` (
   system_ID INT AUTO_INCREMENT NOT NULL,
   logs TEXT NOT NULL,
   updates VARCHAR(100),
   alerts VARCHAR(100),
   PRIMARY KEY (system_ID)
);




DROP TABLE IF EXISTS System_Admin;
CREATE TABLE System_Admin (
   admin_ID INT AUTO_INCREMENT NOT NULL,
   name VARCHAR(50),
   email VARCHAR(75),
   shift INT,
   assignedSys_ID INT NOT NULL,
   team_ID INT,
   PRIMARY KEY (admin_ID),
   FOREIGN KEY (assignedSys_ID) REFERENCES `system` (system_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (team_ID) REFERENCES Analysis_Team (team_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);




DROP TABLE IF EXISTS User_Device;
CREATE TABLE User_Device (
   device_ID INT AUTO_INCREMENT NOT NULL,
   transfer VARCHAR(75),
   PRIMARY KEY (device_ID)
);


DROP TABLE IF EXISTS Analyst;
CREATE TABLE Analyst (
   analyst_ID INT AUTO_INCREMENT NOT NULL,
   name VARCHAR(50),
   email VARCHAR(75) UNIQUE,
   report_ID INT NOT NULL,
   plan_ID INT NOT NULL,
   admin_ID INT NOT NULL,
   transfer_ID INT,
   PRIMARY KEY (analyst_ID),
   FOREIGN KEY (report_ID) REFERENCES Report (report_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (plan_ID) REFERENCES Plan (plan_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (admin_ID) REFERENCES System_Admin (admin_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (transfer_ID) REFERENCES User_Device (device_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


DROP TABLE IF EXISTS Desk_Attendant;
CREATE TABLE Desk_Attendant (
   emp_ID INT AUTO_INCREMENT NOT NULL,
   name VARCHAR(50),
   email VARCHAR(75),
   assigned_Area VARCHAR(75),
   shift INT,
   assignedUser_ID INT,
   analyst_ID INT NOT NULL,
   PRIMARY KEY (emp_ID),
   FOREIGN KEY (assignedUser_ID) REFERENCES User (user_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (analyst_ID) REFERENCES Analyst (analyst_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


CREATE TABLE All_Memberships (
   emp_ID INT,
   membership_ID INT,
   active TINYINT(1) NOT NULL DEFAULT 1,
   PRIMARY KEY (emp_ID, membership_ID),
   FOREIGN KEY (emp_ID) REFERENCES Desk_Attendant (emp_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (membership_ID) REFERENCES Membership (membership_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);




DROP TABLE IF EXISTS Policy;
CREATE TABLE Policy (
   policy_ID INT AUTO_INCREMENT NOT NULL,
   title VARCHAR(100) NOT NULL,
   description TEXT NOT NULL,
   PRIMARY KEY (policy_ID)
);


DROP TABLE IF EXISTS Video_Footage;
CREATE TABLE Video_Footage (
   footage_ID INT AUTO_INCREMENT NOT NULL,
   camera_ID INT NOT NULL,
   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                          ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (footage_ID)
);




DROP TABLE IF EXISTS Equipment_Maintenance;
CREATE TABLE Equipment_Maintenance (
   equip_ID INT AUTO_INCREMENT NOT NULL,
   `condition` VARCHAR(128),
   requestForm VARCHAR(128),
   PRIMARY KEY (equip_ID)
);


DROP TABLE IF EXISTS Emp_Only;
CREATE TABLE Emp_Only (
   emp_ID INT,
   policy_ID INT,
   footage_ID INT,
   equip_ID INT,
   FOREIGN KEY (emp_ID) REFERENCES Desk_Attendant (emp_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (policy_ID) REFERENCES Policy (policy_ID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   FOREIGN KEY (footage_ID) REFERENCES Video_Footage (footage_ID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT,
   FOREIGN KEY (equip_ID) REFERENCES Equipment_Maintenance (equip_ID)
       ON UPDATE CASCADE
       ON DELETE RESTRICT
);


SHOW Tables;
-- Sample Data for All Tables


-- USER
-- INSERT INTO User (user_ID, name, email, address, gym_location, passwordHash)
-- VALUES
--   (1, 'Alex Johnson', 'alex.j@gmail.com', '123 Main St', 'Downtown Gym', 'hash123'),
--  (2, 'Brenda Lee', 'brenda.lee@example.com', '456 Oak Rd', 'Westside Gym', 'hash456'),
--  (3, 'Carlos Torres', 'carlos.t@domain.com', '789 Pine Ln', 'Eastside Gym', 'hash789');


-- GOAL
-- INSERT INTO Goal (user_ID, goal_name, task, tracking, records, reminders)
-- VALUES
--   (1, 'Lose Weight', 'Cardio & Diet', 'Daily', 'Progress Weekly', 'Email'),
--  (2, 'Build Muscle', 'Strength Training', 'Bi-weekly', 'Photos Monthly', 'SMS'),
--  (3, 'Improve Stamina', 'HIIT Routines', 'Weekly', 'Pulse Tracker', 'Push Notification');


-- PLAN
-- INSERT INTO Plan (plan_ID, title, workout_rec, diet)
-- VALUES
--  (201, 'Lean Plan', '30 min cardio + weights', 'Low Carb'),
-- (202, 'Bulk Plan', 'Heavy lifting routine', 'High Protein'),
--  (203, 'Endurance Plan', 'Running & cycling', 'Balanced Diet');


-- ALL_MEMBERSHIPS
-- INSERT INTO All_Memberships (emp_ID, membership_ID, active)
-- VALUES
--  (1, 501, 1),
--  (2, 502, 0),
--  (3, 503, 1);


-- MEMBERSHIP
-- INSERT INTO Membership (membership_ID, status, start_date, end_date, billing)
-- VALUES
-- (501, 'Active', '2025-01-01', '2025-12-31', 100),
-- (502, 'Expired', '2024-01-01', '2024-12-31', 1200),
 -- (503, 'Active', '2025-06-01', '2026-05-31', 300);


-- DESK_ATTENDANT
-- INSERT INTO Desk_Attendant (emp_ID, name, email, assigned_Area, shift, assignedUser_ID, analyst_ID)
-- VALUES
-- (101, 'Jamie Adams', 'jadams@gym.com', 'Front Desk', '1', 1, 301),
--  (102, 'Taylor Brown', 'tbrown@gym.com', 'Check-in', '2', 2, 302),
 -- (103, 'Drew Kim', 'dkim@gym.com', 'Lobby', '3', 3, 303);


-- ANALYST
-- INSERT INTO Analyst (analyst_ID, name, email, report_ID, plan_ID, admin_ID, device_ID)
-- VALUES
-- (301, 'Maya Green', 'maya@gym.com', 601, 201, 901, 701),
-- (302, 'Ravi Singh', 'ravi@gym.com', 602, 202, 902, 702),
 -- (303, 'Nina Park', 'nina@gym.com', 603, 203, 903, 703);


-- SYSTEM_ADMIN
-- INSERT INTO System_Admin (admin_ID, name, email, shift, assignedSys_ID, team_ID)
-- VALUES
 -- (901, 'Jordan Smith', 'jsmith@admin.com', 'Morning', 801, 1001),
 -- (902, 'Lila Chavez', 'lchavez@admin.com', 'Afternoon', 802, 1002),
 -- (903, 'Aiden Ross', 'aross@admin.com', 'Night', 803, 1003);


-- SYSTEM
-- INSERT INTO System (system_ID, logs, updates, alerts)
-- VALUES
-- (801, 'System rebooted', 'Patch v1.3', 'Security Scan Complete'),
-- (802, 'Backup completed', 'Patch v1.4', 'Disk Space Low'),
-- (803, 'New login detected', 'Patch v1.5', 'Unauthorized Access');


-- ANALYSIS_TEAM
-- INSERT INTO Analysis_Team (team_ID, maintenance_task, requests)
-- VALUES
-- (1001, 'Weekly Checkup', 'Add pull-up bar'),
 -- (1002, 'Monthly Audit', 'Replace mats'),
 -- (1003, 'Biweekly Safety Check', 'Adjust dumbbell rack');


-- USER_DEVICE
-- INSERT INTO User_Device (device_ID, transfer)
-- VALUES
-- (701, 'Fitbit Sync'),
-- (702, 'Apple Health'),
-- (703, 'Google Fit');


-- REPORT
-- INSERT INTO Report (report_ID, title, checklist, completed_goals, uncompleted_goals, work_efficiency, time_based_summary)
-- VALUES
-- (601, 'Week 1 Summary', 'Stretch, Lift, Run', '2', '1', '85%', '4h 30min'),
-- (602, 'Week 2 Summary', 'Run, Bike', '1', '1', '70%', '3h 20min'),
-- (603, 'Week 3 Summary', 'Yoga, Swim', '3', '0', '95%', '6h 10min');


-- EMP_ONLY
-- INSERT INTO Emp_Only (emp_ID, policy_ID, footage_ID, equip_ID)
-- VALUES
-- (101, 1, 301, 401),
-- (102, 2, 302, 402),
 -- (103, 3, 303, 403);


-- VIDEO_FOOTAGE
-- INSERT INTO Video_Footage (footage_ID, camera_ID, timestamp)
-- VALUES
-- (301, 'CAM_A1', '2025-08-01 08:30:00'),
 -- (302, 'CAM_B2', '2025-08-02 15:00:00'),
 -- (303, 'CAM_C3', '2025-08-03 19:45:00');


-- POLICY
-- INSERT INTO Policy (policy_ID, title, description)
-- VALUES
-- (1, 'Gym Safety Policy', 'Ensure all equipment is sanitized and in good condition.'),
 -- (2, 'Video Surveillance Policy', 'All areas are monitored for safety and accountability.'),
-- (3, 'Emergency Protocols', 'Follow posted protocols in the event of an emergency.');


-- EQUIPMENT_MAINTENANCE
-- INSERT INTO Equipment_Maintenance (equip_ID, condition, requestForm)
-- VALUES
 -- (401, 'Good', 'No action needed'),
 -- (402, 'Requires Maintenance', 'Treadmill belt slipping'),
 -- (403, 'Out of Order', 'Elliptical screen not working');
