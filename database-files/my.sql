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

DROP TABLE IF EXISTS `System`;
CREATE TABLE `System` (
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
    shift VARCHAR(50),
    assignedSys_ID INT NOT NULL,
    team_ID INT,
    PRIMARY KEY (admin_ID),
    FOREIGN KEY (assignedSys_ID) REFERENCES `System` (system_ID)
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


DROP TABLE IF EXISTS User_Membership;
CREATE TABLE User_Membership (
    user_ID INT,
    membership_ID INT,
    active TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (user_ID, membership_ID),
    FOREIGN KEY (user_ID) REFERENCES User (user_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (membership_ID) REFERENCES Membership (membership_ID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
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
    camera_ID VARCHAR(50) NOT NULL,
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





-- Sample Data for All Tables



-- USER
INSERT INTO User (user_ID, name, email, address, gym_location, passwordHash)
VALUES
    (1, 'Alex Johnson', 'alex.j@gmail.com', '123 Main St', 'Downtown Gym', 'hash123'),
    (2, 'Brenda Lee', 'brenda.lee@example.com', '456 Oak Rd', 'Westside Gym', 'hash456'),
    (3, 'Carlos Torres', 'carlos.t@domain.com', '789 Pine Ln', 'Eastside Gym', 'hash789'),
    (4, 'Diana Smith', 'diana.smith@example.com', '101 Maple Ave', 'Downtown Gym', 'hash101'),
    (5, 'Ethan Brown', 'ethan.brown@example.com', '202 Cedar St', 'Westside Gym', 'hash202'),
    (6, 'Fiona White', 'fiona.white@example.com', '303 Birch Rd', 'Eastside Gym', 'hash303'),
    (7, 'George Black', 'george.black@example.com', '404 Spruce Ln', 'Downtown Gym', 'hash404'),
    (8, 'Hannah Green', 'hannah.green@example.com', '505 Willow Dr', 'Westside Gym', 'hash505'),
    (9, 'Ian Blue', 'ian.blue@example.com', '606 Aspen Ct', 'Eastside Gym', 'hash606'),
    (10, 'Julia Red', 'julia.red@example.com', '707 Poplar Pl', 'Downtown Gym', 'hash707'),
    (11, 'Kevin Gray', 'kevin.gray@example.com', '808 Walnut St', 'Westside Gym', 'hash808'),
    (12, 'Lily Violet', 'lily.violet@example.com', '909 Chestnut Ave', 'Eastside Gym', 'hash909'),
    (13, 'Mason Gold', 'mason.gold@example.com', '111 Pine St', 'Downtown Gym', 'hash111'),
    (14, 'Nina Silver', 'nina.silver@example.com', '222 Oak Ave', 'Westside Gym', 'hash222'),
    (15, 'Oscar Bronze', 'oscar.bronze@example.com', '333 Elm Rd', 'Eastside Gym', 'hash333'),
    (16, 'Paula Copper', 'paula.copper@example.com', '444 Cedar Ct', 'Downtown Gym', 'hash444'),
    (17, 'Quinn Jade', 'quinn.jade@example.com', '555 Maple Pl', 'Westside Gym', 'hash555'),
    (18, 'Rita Pearl', 'rita.pearl@example.com', '666 Birch St', 'Eastside Gym', 'hash666'),
    (19, 'Sam Ruby', 'sam.ruby@example.com', '777 Spruce Ave', 'Downtown Gym', 'hash777'),
    (20, 'Tina Amber', 'tina.amber@example.com', '888 Willow Rd', 'Westside Gym', 'hash888'),
    (21, 'Uma Coral', 'uma.coral@example.com', '999 Aspen Ln', 'Eastside Gym', 'hash999'),
    (22, 'Victor Onyx', 'victor.onyx@example.com', '121 Poplar St', 'Downtown Gym', 'hash121'),
    (23, 'Wendy Opal', 'wendy.opal@example.com', '232 Walnut Ave', 'Westside Gym', 'hash232'),
    (24, 'Xander Quartz', 'xander.quartz@example.com', '343 Chestnut Rd', 'Eastside Gym', 'hash343'),
    (25, 'Yara Sapphire', 'yara.sapphire@example.com', '454 Pine Ct', 'Downtown Gym', 'hash454'),
    (26, 'Zane Topaz', 'zane.topaz@example.com', '565 Oak Pl', 'Westside Gym', 'hash565'),
    (27, 'Ava Emerald', 'ava.emerald@example.com', '676 Elm St', 'Eastside Gym', 'hash676'),
    (28, 'Ben Garnet', 'ben.garnet@example.com', '787 Cedar Ave', 'Downtown Gym', 'hash787'),
    (29, 'Cara Diamond', 'cara.diamond@example.com', '898 Maple Rd', 'Westside Gym', 'hash898'),
    (30, 'Derek Amethyst', 'derek.amethyst@example.com', '909 Birch Pl', 'Eastside Gym', 'hash909');



-- GOAL
INSERT INTO Goal (user_ID, goal_name, task, tracking, records, reminders)
VALUES
    (1, 'Lose Weight', 'Cardio & Diet', 'Daily', 'Progress Weekly', 'Email'),
    (2, 'Build Muscle', 'Strength Training', 'Bi-weekly', 'Photos Monthly', 'SMS'),
    (3, 'Improve Stamina', 'HIIT Routines', 'Weekly', 'Pulse Tracker', 'Push Notification'),
    (4, 'Run 5k', 'Running', 'Daily', 'Time Tracker', 'App Alert'),
    (5, 'Swim 1 Mile', 'Swimming', 'Weekly', 'Lap Counter', 'Email'),
    (6, 'Cycle 100 Miles', 'Cycling', 'Monthly', 'Distance Log', 'SMS'),
    (7, 'Bench Press 200lbs', 'Strength Training', 'Weekly', 'Weight Log', 'Push Notification'),
    (8, 'Yoga Mastery', 'Yoga', 'Daily', 'Flexibility Chart', 'App Alert'),
    (9, '10 Pull-ups', 'Bodyweight', 'Weekly', 'Reps Log', 'Email'),
    (10, 'Squat 250lbs', 'Strength Training', 'Bi-weekly', 'Weight Log', 'SMS'),
    (11, 'Deadlift 300lbs', 'Strength Training', 'Monthly', 'Weight Log', 'Push Notification'),
    (12, 'Lose 10lbs', 'Cardio & Diet', 'Weekly', 'Progress Photos', 'App Alert'),
    (13, 'Gain 5lbs Muscle', 'Strength Training', 'Monthly', 'Body Scan', 'Email'),
    (14, 'Stretch Daily', 'Flexibility', 'Daily', 'Stretch Log', 'SMS'),
    (15, 'Walk 10,000 Steps', 'Walking', 'Daily', 'Step Counter', 'Push Notification'),
    (16, 'Climb 50 Flights', 'Stair Climbing', 'Weekly', 'Flight Log', 'App Alert'),
    (17, 'Row 2k', 'Rowing', 'Weekly', 'Time Tracker', 'Email'),
    (18, 'Jump Rope 500x', 'Jump Rope', 'Daily', 'Reps Log', 'SMS'),
    (19, '50 Push-ups', 'Bodyweight', 'Weekly', 'Reps Log', 'Push Notification'),
    (20, 'Plank 3 Minutes', 'Core', 'Daily', 'Time Tracker', 'App Alert'),
    (21, 'Track Calories', 'Nutrition', 'Daily', 'Calorie Log', 'Email'),
    (22, 'Sleep 8 Hours', 'Sleep', 'Daily', 'Sleep Tracker', 'SMS'),
    (23, 'Drink 2L Water', 'Hydration', 'Daily', 'Water Log', 'Push Notification'),
    (24, 'Meal Prep Weekly', 'Nutrition', 'Weekly', 'Meal Log', 'App Alert'),
    (25, 'Try New Sport', 'Recreation', 'Monthly', 'Activity Log', 'Email'),
    (26, 'Join Group Class', 'Group Fitness', 'Weekly', 'Attendance Log', 'SMS'),
    (27, 'Log Workouts Daily', 'Tracking', 'Daily', 'Workout Log', 'Push Notification'),
    (28, 'Increase Vertical Jump', 'Plyometrics', 'Weekly', 'Jump Log', 'App Alert'),
    (29, 'Improve Balance', 'Balance Training', 'Daily', 'Balance Log', 'Email'),
    (30, 'Reduce Resting HR', 'Cardio', 'Weekly', 'Heart Rate Log', 'SMS');



-- MEMBERSHIP
INSERT INTO Membership (membership_ID, status, start_date, end_date, billing)
VALUES
    (501, 'Premium', '2025-01-01', '2025-12-31', 100),
    (502, 'General', '2024-01-01', '2024-12-31', 1200),
    (503, 'Gold', '2025-06-01', '2026-05-31', 300);


-- REPORT
INSERT INTO Report (report_ID, title, checklist, completed_goals, uncompleted_goals, work_efficiency, time_based_summary)
VALUES
    (601, 'Week 1 Summary', 'Stretch, Lift, Run', '2', '1', '85%', '4h 30min'),
    (602, 'Week 2 Summary', 'Run, Bike', '1', '1', '70%', '3h 20min'),
    (603, 'Week 3 Summary', 'Yoga, Swim', '3', '0', '95%', '6h 10min');

-- PLAN
INSERT INTO Plan (plan_ID, title, workout_rec, diet)
VALUES
    (201, 'Lean Plan', '30 min cardio + weights', 'Low Carb'),
    (202, 'Bulk Plan', 'Heavy lifting routine', 'High Protein'),
    (203, 'Endurance Plan', 'Running & cycling', 'Balanced Diet');



-- ANALYSIS_TEAM
INSERT INTO Analysis_Team (team_ID, maintenance_task, requests)
VALUES
    (1001, 'Weekly Checkup', 'Add pull-up bar'),
    (1002, 'Monthly Audit', 'Replace mats'),
    (1003, 'Biweekly Safety Check', 'Adjust dumbbell rack');


-- SYSTEM
INSERT INTO `System` (system_ID, logs, updates, alerts)
VALUES
    (801, 'System rebooted', 'Patch v1.3', 'Security Scan Complete'),
    (802, 'Backup completed', 'Patch v1.4', 'Disk Space Low'),
    (803, 'New login detected', 'Patch v1.5', 'Unauthorized Access');


-- SYSTEM_ADMIN
INSERT INTO System_Admin (admin_ID, name, email, shift, assignedSys_ID, team_ID)
VALUES
    (901, 'Jordan Smith', 'jsmith@admin.com', 'Morning', 801, 1001),
    (902, 'Lila Chavez', 'lchavez@admin.com', 'Afternoon', 802, 1002),
    (903, 'Aiden Ross', 'aross@admin.com', 'Night', 803, 1003),
    (904, 'Sam Lee', 'sam.lee@admin.com', 'Morning', 801, 1001),
    (905, 'Tina Wu', 'tina.wu@admin.com', 'Afternoon', 802, 1002),
    (906, 'Omar Patel', 'omar.patel@admin.com', 'Night', 803, 1003),
    (907, 'Priya Singh', 'priya.singh@admin.com', 'Morning', 801, 1001),
    (908, 'Lucas Kim', 'lucas.kim@admin.com', 'Afternoon', 802, 1002),
    (909, 'Ella Brown', 'ella.brown@admin.com', 'Night', 803, 1003),
    (910, 'Noah Clark', 'noah.clark@admin.com', 'Morning', 801, 1001),
    (911, 'Mia Davis', 'mia.davis@admin.com', 'Afternoon', 802, 1002),
    (912, 'Liam Wilson', 'liam.wilson@admin.com', 'Night', 803, 1003),
    (913, 'Zoe Miller', 'zoe.miller@admin.com', 'Morning', 801, 1001),
    (914, 'Ethan Moore', 'ethan.moore@admin.com', 'Afternoon', 802, 1002),
    (915, 'Ava Taylor', 'ava.taylor@admin.com', 'Night', 803, 1003),
    (916, 'Mason Anderson', 'mason.anderson@admin.com', 'Morning', 801, 1001),
    (917, 'Sophia Thomas', 'sophia.thomas@admin.com', 'Afternoon', 802, 1002),
    (918, 'Logan Jackson', 'logan.jackson@admin.com', 'Night', 803, 1003),
    (919, 'Charlotte White', 'charlotte.white@admin.com', 'Morning', 801, 1001),
    (920, 'Benjamin Harris', 'benjamin.harris@admin.com', 'Afternoon', 802, 1002),
    (921, 'Amelia Martin', 'amelia.martin@admin.com', 'Night', 803, 1003),
    (922, 'Elijah Thompson', 'elijah.thompson@admin.com', 'Morning', 801, 1001),
    (923, 'Harper Garcia', 'harper.garcia@admin.com', 'Afternoon', 802, 1002),
    (924, 'William Martinez', 'william.martinez@admin.com', 'Night', 803, 1003),
    (925, 'Evelyn Robinson', 'evelyn.robinson@admin.com', 'Morning', 801, 1001),
    (926, 'James Clark', 'james.clark@admin.com', 'Afternoon', 802, 1002),
    (927, 'Abigail Lewis', 'abigail.lewis@admin.com', 'Night', 803, 1003),
    (928, 'Henry Lee', 'henry.lee@admin.com', 'Morning', 801, 1001),
    (929, 'Emily Walker', 'emily.walker@admin.com', 'Afternoon', 802, 1002),
    (930, 'Jack Hall', 'jack.hall@admin.com', 'Night', 803, 1003);


-- USER_DEVICE
INSERT INTO User_Device (device_ID, transfer)
VALUES
    (701, 'Fitbit Sync'),
    (702, 'Apple Health'),
    (703, 'Google Fit');


-- ANALYST
INSERT INTO Analyst (analyst_ID, name, email, report_ID, plan_ID, admin_ID, transfer_ID)
VALUES
    (301, 'Maya Green', 'maya@gym.com', 601, 201, 901, 701),
    (302, 'Ravi Singh', 'ravi@gym.com', 602, 202, 902, 702),
    (303, 'Nina Park', 'nina@gym.com', 603, 203, 903, 703),
    (304, 'Olivia King', 'olivia.king@gym.com', 601, 201, 904, 701),
    (305, 'Liam Scott', 'liam.scott@gym.com', 602, 202, 905, 702),
    (306, 'Emma Young', 'emma.young@gym.com', 603, 203, 906, 703),
    (307, 'Noah Adams', 'noah.adams@gym.com', 601, 201, 907, 701),
    (308, 'Ava Baker', 'ava.baker@gym.com', 602, 202, 908, 702),
    (309, 'Sophia Carter', 'sophia.carter@gym.com', 603, 203, 909, 703),
    (310, 'Jackson Evans', 'jackson.evans@gym.com', 601, 201, 910, 701),
    (311, 'Lucas Foster', 'lucas.foster@gym.com', 602, 202, 911, 702),
    (312, 'Mia Gray', 'mia.gray@gym.com', 603, 203, 912, 703),
    (313, 'Benjamin Hill', 'benjamin.hill@gym.com', 601, 201, 913, 701),
    (314, 'Charlotte James', 'charlotte.james@gym.com', 602, 202, 914, 702),
    (315, 'Elijah Kelly', 'elijah.kelly@gym.com', 603, 203, 915, 703),
    (316, 'Amelia Lee', 'amelia.lee@gym.com', 601, 201, 916, 701),
    (317, 'Harper Moore', 'harper.moore@gym.com', 602, 202, 917, 702),
    (318, 'Evelyn Nelson', 'evelyn.nelson@gym.com', 603, 203, 918, 703),
    (319, 'Henry Perez', 'henry.perez@gym.com', 601, 201, 919, 701),
    (320, 'Abigail Reed', 'abigail.reed@gym.com', 602, 202, 920, 702),
    (321, 'Jack Rivera', 'jack.rivera@gym.com', 603, 203, 921, 703),
    (322, 'Emily Sanchez', 'emily.sanchez@gym.com', 601, 201, 922, 701),
    (323, 'William Stewart', 'william.stewart@gym.com', 602, 202, 923, 702),
    (324, 'Sofia Turner', 'sofia.turner@gym.com', 603, 203, 924, 703),
    (325, 'James Ward', 'james.ward@gym.com', 601, 201, 925, 701),
    (326, 'Ella Wood', 'ella.wood@gym.com', 602, 202, 926, 702),
    (327, 'Logan Wright', 'logan.wright@gym.com', 603, 203, 927, 703),
    (328, 'Scarlett Young', 'scarlett.young@gym.com', 601, 201, 928, 701),
    (329, 'Mason Lee', 'mason.lee@gym.com', 602, 202, 929, 702),
    (330, 'Lily King', 'lily.king@gym.com', 603, 203, 930, 703);


-- DESK ATTENDANT
INSERT INTO Desk_Attendant (emp_ID, name, email, assigned_Area, shift, assignedUser_ID, analyst_ID)
VALUES
    (101, 'Jamie Adams', 'jadams@gym.com', 'Front Desk', '1', 1, 301),
    (102, 'Taylor Brown', 'tbrown@gym.com', 'Check-in', '2', 2, 302),
    (103, 'Drew Kim', 'dkim@gym.com', 'Lobby', '3', 3, 303),
    (104, 'Ava Smith', 'ava.smith@gym.com', 'Front Desk', '1', 4, 304),
    (105, 'Ethan Brown', 'ethan.brown@gym.com', 'Check-in', '2', 5, 305),
    (106, 'Mia Johnson', 'mia.johnson@gym.com', 'Lobby', '3', 6, 306),
    (107, 'Noah Lee', 'noah.lee@gym.com', 'Front Desk', '1', 7, 307),
    (108, 'Sophia Kim', 'sophia.kim@gym.com', 'Check-in', '2', 8, 308),
    (109, 'Jackson Park', 'jackson.park@gym.com', 'Lobby', '3', 9, 309),
    (110, 'Lucas Green', 'lucas.green@gym.com', 'Front Desk', '1', 10, 310),
    (111, 'Mason White', 'mason.white@gym.com', 'Check-in', '2', 11, 311),
    (112, 'Ella Black', 'ella.black@gym.com', 'Lobby', '3', 12, 312),
    (113, 'Benjamin Gray', 'benjamin.gray@gym.com', 'Front Desk', '1', 13, 313),
    (114, 'Charlotte Brown', 'charlotte.brown@gym.com', 'Check-in', '2', 14, 314),
    (115, 'Elijah Davis', 'elijah.davis@gym.com', 'Lobby', '3', 15, 315),
    (116, 'Amelia Wilson', 'amelia.wilson@gym.com', 'Front Desk', '1', 16, 316),
    (117, 'Harper Miller', 'harper.miller@gym.com', 'Check-in', '2', 17, 317),
    (118, 'Evelyn Moore', 'evelyn.moore@gym.com', 'Lobby', '3', 18, 318),
    (119, 'Henry Thomas', 'henry.thomas@gym.com', 'Front Desk', '1', 19, 319),
    (120, 'Abigail Jackson', 'abigail.jackson@gym.com', 'Check-in', '2', 20, 320),
    (121, 'Jack Harris', 'jack.harris@gym.com', 'Lobby', '3', 21, 321),
    (122, 'Emily Martin', 'emily.martin@gym.com', 'Front Desk', '1', 22, 322),
    (123, 'William Thompson', 'william.thompson@gym.com', 'Check-in', '2', 23, 323),
    (124, 'Sofia Garcia', 'sofia.garcia@gym.com', 'Lobby', '3', 24, 324),
    (125, 'James Martinez', 'james.martinez@gym.com', 'Front Desk', '1', 25, 325),
    (126, 'Ella Robinson', 'ella.robinson@gym.com', 'Check-in', '2', 26, 326),
    (127, 'Logan Clark', 'logan.clark@gym.com', 'Lobby', '3', 27, 327),
    (128, 'Scarlett Lewis', 'scarlett.lewis@gym.com', 'Front Desk', '1', 28, 328),
    (129, 'Mason Walker', 'mason.walker@gym.com', 'Check-in', '2', 29, 329),
    (130, 'Lily Hall', 'lily.hall@gym.com', 'Lobby', '3', 30, 330);


-- USER_MEMBERSHIP
INSERT INTO User_Membership (user_ID, membership_ID, active)
VALUES
    (1, 501, 1),
    (2, 502, 0),
    (3, 503, 1);


-- VIDEO_FOOTAGE
INSERT INTO Video_Footage (footage_ID, camera_ID, timestamp)
VALUES
    (301, 'CAM_A1', '2025-08-01 08:30:00'),
    (302, 'CAM_B2', '2025-08-02 15:00:00'),
    (303, 'CAM_C3', '2025-08-03 19:45:00');



-- POLICY
INSERT INTO Policy (policy_ID, title, description)
VALUES
    (1, 'Gym Safety Policy', 'Ensure all equipment is sanitized and in good condition.'),
    (2, 'Video Surveillance Policy', 'All areas are monitored for safety and accountability.'),
    (3, 'Emergency Protocols', 'Follow posted protocols in the event of an emergency.');



-- EQUIPMENT_MAINTENANCE
INSERT INTO Equipment_Maintenance (equip_ID, `condition`, requestForm)
VALUES
    (401, 'Good', 'No action needed'),
    (402, 'Requires Maintenance', 'Treadmill belt slipping'),
    (403, 'Out of Order', 'Elliptical screen not working');


-- EMP_ONLY
INSERT INTO Emp_Only (emp_ID, policy_ID, footage_ID, equip_ID)
VALUES
    (101, 1, 301, 401),
    (102, 2, 302, 402),
    (103, 3, 303, 403);

-- Additional detailed sample rows (bring each table to 30 rows where applicable)

-- ANALYSIS_TEAM (add 27 more -> total 30)
INSERT INTO Analysis_Team (team_ID, maintenance_task, requests)
VALUES
    (1004, 'Monthly equipment audit', 'Replace worn grips'),
    (1005, 'Quarterly safety drill', 'Schedule evacuation practice'),
    (1006, 'HVAC filter replacement', 'Order HEPA filters'),
    (1007, 'Inspect treadmills', 'Lubricate deck belts'),
    (1008, 'Weight rack alignment', 'Tighten bolts'),
    (1009, 'Pool chlorine check', 'Adjust chemical levels'),
    (1010, 'Lighting check', 'Replace burnt bulbs'),
    (1011, 'Sound system test', 'Calibrate speakers'),
    (1012, 'Emergency exit signage', 'Replace faded signs'),
    (1013, 'Locker maintenance', 'Replace broken locks'),
    (1014, 'First-aid kit audit', 'Replenish supplies'),
    (1015, 'Floor mat replacement', 'Order anti-slip mats'),
    (1016, 'Bike maintenance', 'True bike wheels'),
    (1017, 'Cable machine inspection', 'Check pulleys'),
    (1018, 'Rope and strap check', 'Replace frayed ropes'),
    (1019, 'Paint touch-up', 'Repaint worn areas'),
    (1020, 'Sauna heater service', 'Clean heater coils'),
    (1021, 'Ventilation cleaning', 'Ductwork vacuuming'),
    (1022, 'Signage update', 'Add new health notices'),
    (1023, 'Handrail stability', 'Re-secure loose rails'),
    (1024, 'Stairwell lighting', 'Add motion sensors'),
    (1025, 'Thermostat calibration', 'Sync zones'),
    (1026, 'Emergency drill report', 'Compile incident logs'),
    (1027, 'Pool deck resurfacing', 'Schedule contractor'),
    (1028, 'Window seal check', 'Replace failed seals'),
    (1029, 'Accessibility ramp check', 'Repair damaged sections'),
    (1030, 'Exterior cleanup', 'Pressure-wash entrance');

-- PLAN (add 27 more -> total 30)
INSERT INTO Plan (plan_ID, title, workout_rec, diet)
VALUES
    (204, 'Strength & Conditioning', '3x/week strength + 2x cardio', 'High Protein'),
    (205, 'Cardio Focus', '5x/week cardio sessions', 'Balanced'),
    (206, 'Flexibility & Mobility', 'Daily stretching routine', 'Anti-inflammatory'),
    (207, 'Beginner Strength', 'Full-body 3x/week', 'Moderate Protein'),
    (208, 'Hypertrophy Plan', '4x/week split', 'High Protein + Calorie Surplus'),
    (209, 'Endurance Build', 'Long runs + intervals', 'Carb-heavy'),
    (210, 'Weight Loss Blitz', 'HIIT + calorie deficit', 'Low Carb'),
    (211, 'Post-Injury Rehab', 'Low-impact strengthening', 'Balanced + Anti-inflammatory'),
    (212, 'Athlete Prep', 'Sport-specific drills', 'Periodized nutrition'),
    (213, 'Core Strength', 'Daily core circuits', 'Balanced'),
    (214, 'Pilates Fusion', 'Pilates 3x/week + mobility', 'Whole foods'),
    (215, 'Circuit Training', 'Full-body circuits 4x/week', 'Protein-focused'),
    (216, 'Yoga & Recovery', '3x/week yoga + recovery', 'Plant-forward'),
    (217, 'Strength Endurance', 'Heavy circuits', 'Mixed Macronutrients'),
    (218, 'Powerlifting Prep', 'Squat/Bench/Deadlift cycles', 'High Protein'),
    (219, 'Sprint Training', 'Short sprints + plyometrics', 'High Carb around workouts'),
    (220, 'Triathlon Base', 'Swim/Bike/Run balance', 'Endurance-focused'),
    (221, 'Functional Fitness', 'Movement-based workouts', 'Mixed Macronutrients'),
    (222, 'Senior Mobility', 'Low-impact mobility + balance', 'Heart-healthy diet'),
    (223, 'Teen Fitness', 'Education + supervised strength', 'Balanced growth diet'),
    (224, 'Weekend Warrior', '2 intense weekend sessions', 'Flexible diet'),
    (225, 'Boxing Conditioning', 'Bag + footwork drills', 'Lean Protein'),
    (226, 'Dance Cardio', 'Choreography + cardio', 'Carb-timed meals'),
    (227, 'Functional Hypertrophy', 'Compound lifts + volume', 'Protein & Carb periodization'),
    (228, 'Low Impact Cardio', 'Elliptical & pool sessions', 'Low Fat'),
    (229, 'Military Prep', 'Ruck marches + strength', 'High Calorie'),
    (230, 'Postpartum Return', 'Gradual strength rebuild', 'Nutrient-dense'),
    (231, 'Sprint to Marathon', 'Speed + long-run mix', 'Endurance nutrition');

-- REPORT (add 27 more -> total 30)
INSERT INTO Report (report_ID, title, checklist, completed_goals, uncompleted_goals, work_efficiency, time_based_summary)
VALUES
    (604, 'Week 4 Summary', 'Warmup, Program Adherence', '3', '0', '88%', '5h 10min'),
    (605, 'Week 5 Summary', 'HIIT, Strength', '2', '2', '72%', '4h 45min'),
    (606, 'Month 2 Summary', 'Cardio, Mobility', '8', '1', '80%', '20h 0min'),
    (607, 'Q2 Review', 'Metrics audit, equipment log', '15', '3', '82%', '65h 30min'),
    (608, 'Injury Follow-up', 'Rehab checklist', '1', '0', '90%', '2h 15min'),
    (609, 'Membership Trends', 'Churn analysis, cohort', '0', '0', '75%', '12h 0min'),
    (610, 'Safety Incident Log', 'Incident checklist', '0', '1', '60%', '1h 20min'),
    (611, 'Facility Audit', 'Maintenance checklist', '10', '2', '85%', '8h 40min'),
    (612, 'Staff Training', 'Attendance checklist', '5', '0', '95%', '6h 0min'),
    (613, 'Equipment Performance', 'Reliability checklist', '2', '1', '78%', '3h 55min'),
    (614, 'Monthly Engagement', 'Event checklist', '12', '0', '87%', '14h 5min'),
    (615, 'Program Effectiveness', 'Survey + metrics', '6', '2', '81%', '10h 10min'),
    (616, 'Nutrition Workshops', 'Attendance + feedback', '3', '0', '92%', '5h 0min'),
    (617, 'Member Feedback', 'Collect + act', '9', '1', '84%', '7h 30min'),
    (618, 'System Downtime', 'Restore checklist', '0', '0', '70%', '0h 45min'),
    (619, 'New Equipment Rollout', 'Install checklist', '0', '0', '88%', '2h 30min'),
    (620, 'Holiday Operations', 'Staffing checklist', '1', '0', '83%', '9h 20min'),
    (621, 'Attendance Spike', 'Investigate cause', '0', '0', '76%', '1h 10min'),
    (622, 'Retention Study', 'Cohort analysis', '4', '2', '79%', '30h 0min'),
    (623, 'Equipment Loss Audit', 'Inventory checklist', '0', '1', '67%', '2h 0min'),
    (624, 'Weekly Highlights', 'Top performers', '7', '0', '90%', '3h 0min'),
    (625, 'Challenge Wrap-up', 'Competition checklist', '20', '0', '93%', '6h 15min'),
    (626, 'Maintenance Summary', 'Completed jobs', '25', '0', '89%', '16h 0min'),
    (627, 'Energy Efficiency', 'Meter readings', '0', '0', '74%', '4h 40min'),
    (628, 'Staff Performance', 'Review checklist', '6', '1', '86%', '10h 30min'),
    (629, 'Monthly Revenue', 'Billing checklist', '0', '0', '91%', '2h 55min'),
    (630, 'Client Onboarding', 'Welcome checklist', '30', '0', '98%', '12h 0min');

-- SYSTEM (add 27 more -> total 30)
INSERT INTO `System` (system_ID, logs, updates, alerts)
VALUES
    (804, 'Firewall updated', 'Patch v1.6', 'No alerts'),
    (805, 'Database backup', 'Backup script v2', 'Storage warning'),
    (806, 'SSL Certificate renewed', 'Cert v3', 'Expiring soon'),
    (807, 'API latency spike', 'Investigate third-party', 'High latency'),
    (808, 'Disk cleanup', 'Remove temp files', 'Disk low'),
    (809, 'User session reset', 'Auth fix', 'Login failures'),
    (810, 'Monitoring added', 'New metrics', 'No alerts'),
    (811, 'Logging rotation', 'Rotate logs', 'No alerts'),
    (812, 'Storage migrated', 'Move to SSD', 'Migration complete'),
    (813, 'Service restart', 'Worker restart', 'Service degraded'),
    (814, 'Dependency update', 'Library patch', 'Compatibility note'),
    (815, 'Cache cleared', 'Cache invalidation', 'No alerts'),
    (816, 'Rate limiting enabled', 'Throttle added', 'No alerts'),
    (817, 'Third-party auth fix', 'OAuth adjustment', 'Token errors'),
    (818, 'Monitoring alert', 'Threshold adjusted', 'Repeated alerts'),
    (819, 'API auth issue', 'Hotfix applied', 'Auth errors'),
    (820, 'Worker scale', 'Scale up workers', 'Scaling events'),
    (821, 'Queue backlog', 'Process backlog', 'High queue depth'),
    (822, 'Health check added', 'Probe configured', 'No alerts'),
    (823, 'DB index added', 'Query perf improved', 'No alerts'),
    (824, 'TLS hardened', 'Protocols updated', 'No alerts'),
    (825, 'User import', 'Bulk users added', 'No alerts'),
    (826, 'Analytics job', 'Hourly job', 'Job failed occasionally'),
    (827, 'Search indexer', 'Reindex', 'No alerts'),
    (828, 'Configuration audit', 'Permissions updated', 'No alerts'),
    (829, 'Backup verify', 'Checksum ok', 'No alerts'),
    (830, 'Service decommission', 'Old worker removed', 'No alerts');

-- VIDEO_FOOTAGE (add 27 more -> total 30)
INSERT INTO Video_Footage (footage_ID, camera_ID, timestamp)
VALUES
    (304, 'CAM_D4', '2025-08-04 09:00:00'),
    (305, 'CAM_E5', '2025-08-05 10:15:00'),
    (306, 'CAM_F6', '2025-08-06 11:30:00'),
    (307, 'CAM_G7', '2025-08-07 12:45:00'),
    (308, 'CAM_H8', '2025-08-08 13:00:00'),
    (309, 'CAM_I9', '2025-08-09 14:10:00'),
    (310, 'CAM_J10', '2025-08-10 15:20:00'),
    (311, 'CAM_K11', '2025-08-11 16:30:00'),
    (312, 'CAM_L12', '2025-08-12 17:40:00'),
    (313, 'CAM_M13', '2025-08-13 18:50:00'),
    (314, 'CAM_N14', '2025-08-14 19:00:00'),
    (315, 'CAM_O15', '2025-08-15 20:10:00'),
    (316, 'CAM_P16', '2025-08-16 21:20:00'),
    (317, 'CAM_Q17', '2025-08-17 22:30:00'),
    (318, 'CAM_R18', '2025-08-18 23:40:00'),
    (319, 'CAM_S19', '2025-08-19 08:05:00'),
    (320, 'CAM_T20', '2025-08-20 09:15:00'),
    (321, 'CAM_U21', '2025-08-21 10:25:00'),
    (322, 'CAM_V22', '2025-08-22 11:35:00'),
    (323, 'CAM_W23', '2025-08-23 12:45:00'),
    (324, 'CAM_X24', '2025-08-24 13:55:00'),
    (325, 'CAM_Y25', '2025-08-25 14:05:00'),
    (326, 'CAM_Z26', '2025-08-26 15:15:00'),
    (327, 'CAM_AA27', '2025-08-27 16:25:00'),
    (328, 'CAM_BB28', '2025-08-28 17:35:00'),
    (329, 'CAM_CC29', '2025-08-29 18:45:00'),
    (330, 'CAM_DD30', '2025-08-30 19:55:00');

-- POLICY (add 27 more -> total 30)
INSERT INTO Policy (policy_ID, title, description)
VALUES
    (4, 'Equipment Usage Policy', 'Members must wipe equipment after use and follow posted instructions.'),
    (5, 'Membership Refund Policy', 'Refunds are processed within 30 days with valid reason.'),
    (6, 'Child Policy', 'Children under 12 must be supervised by an adult.'),
    (7, 'Locker Policy', 'Lockers are provided; remove items daily.'),
    (8, 'Hygiene Policy', 'Towels required on benches and machines.'),
    (9, 'Noise Policy', 'Keep noise to a minimum during peak hours.'),
    (10, 'Guest Policy', 'Guests allowed with paid pass.'),
    (11, 'Smoking Policy', 'No smoking on premises.'),
    (12, 'Alcohol Policy', 'No alcohol allowed in gym areas.'),
    (13, 'Dress Code', 'Proper athletic attire required.'),
    (14, 'Personal Trainer Policy', 'Certified trainers only.'),
    (15, 'Equipment Reservation', 'Reserve specialty equipment in advance.'),
    (16, 'Cleaning Policy', 'Deep cleaning on Sundays.'),
    (17, 'Privacy Policy', 'CCTV used for safety; footage retained 30 days.'),
    (18, 'ADA Compliance', 'Facilities accessible to persons with disabilities.'),
    (19, 'Lost & Found', 'Items kept for 30 days then donated.'),
    (20, 'Payment Policy', 'Auto-renewal requires cancellation 7 days prior.'),
    (21, 'Cancellation Policy', 'Membership cancellation processed within billing cycle.'),
    (22, 'Referral Policy', 'Refer a friend and receive a credit.'),
    (23, 'Photo Policy', 'Photos allowed in public areas only.'),
    (24, 'Trainer Certification', 'All trainers must show certification.'),
    (25, 'Safety Gear', 'Helmets required for bike studio.'),
    (26, 'Equipment Sharing', 'Share equipment politely and timely.'),
    (27, 'No Pets', 'Pets not allowed except service animals.'),
    (28, 'Food Policy', 'No outside food in gym areas.'),
    (29, 'Temperature Policy', 'HVAC maintained between 68-74F.'),
    (30, 'Incident Reporting', 'Report incidents to front desk immediately.');

-- EQUIPMENT_MAINTENANCE (add 27 more -> total 30)
INSERT INTO Equipment_Maintenance (equip_ID, `condition`, requestForm)
VALUES
    (404, 'Good', 'Replace treadmill display cover'),
    (405, 'Requires Maintenance', 'Adjust elliptical resistance'),
    (406, 'Out of Order', 'Spin bike belt replacement'),
    (407, 'Good', 'Clean rowing machine rail'),
    (408, 'Requires Maintenance', 'Fix incline motor'),
    (409, 'Good', 'Tighten dumbbell rack'),
    (410, 'Requires Maintenance', 'Lubricate cable pulley'),
    (411, 'Out of Order', 'Repair smith machine guide'),
    (412, 'Good', 'Replace bench padding'),
    (413, 'Requires Maintenance', 'Rebuild resistance bands'),
    (414, 'Good', 'Calibrate leg press'),
    (415, 'Requires Maintenance', 'Replace treadmill belt'),
    (416, 'Out of Order', 'Fix rowing footrests'),
    (417, 'Good', 'Service bike chain'),
    (418, 'Requires Maintenance', 'Inspect pulley bearings'),
    (419, 'Good', 'Update touchscreen OS'),
    (420, 'Requires Maintenance', 'Check power supplies'),
    (421, 'Out of Order', 'Replace broken mirror panel'),
    (422, 'Good', 'Clean AC vents'),
    (423, 'Requires Maintenance', 'Repaint locker area'),
    (424, 'Good', 'Replace jump rope handles'),
    (425, 'Requires Maintenance', 'Footing on plyo boxes'),
    (426, 'Good', 'Balance platform recalibration'),
    (427, 'Requires Maintenance', 'Fix lat pulldown attachment'),
    (428, 'Out of Order', 'Repair smith machine cable'),
    (429, 'Good', 'Replace exercise mat stock'),
    (430, 'Requires Maintenance', 'Inspect treadmill emergency stop');