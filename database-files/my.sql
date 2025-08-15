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