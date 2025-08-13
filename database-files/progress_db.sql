-- Progress Fitness App Database Schema
-- Based on Task.md requirements for CS 3200 Database Design Project

DROP DATABASE IF EXISTS progress;
CREATE DATABASE progress;
USE progress;

-- User table for all app users
DROP TABLE IF EXISTS User;
CREATE TABLE User (
    user_ID INT AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(75) UNIQUE NOT NULL,
    passwordHash VARCHAR(128) NOT NULL,
    address VARCHAR(128),
    gym_location VARCHAR(50) NOT NULL,
    user_type ENUM('regular', 'desk_attendant', 'analyst', 'system_admin') DEFAULT 'regular',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_ID)
);

-- Goal table for user fitness goals
DROP TABLE IF EXISTS Goal;
CREATE TABLE Goal (
    goal_ID INT AUTO_INCREMENT NOT NULL,
    user_ID INT NOT NULL,
    goal_name VARCHAR(50) NOT NULL,
    task VARCHAR(75),
    tracking VARCHAR(100),
    records TEXT,
    reminders VARCHAR(100),
    target_date DATE,
    status ENUM('active', 'completed', 'paused') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (goal_ID),
    FOREIGN KEY (user_ID) REFERENCES User (user_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Membership table for gym memberships
DROP TABLE IF EXISTS Membership;
CREATE TABLE Membership (
    membership_ID INT AUTO_INCREMENT NOT NULL,
    user_ID INT NOT NULL,
    status ENUM('active', 'expired', 'suspended') DEFAULT 'active',
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    billing DECIMAL(10,2),
    plan_type VARCHAR(50),
    PRIMARY KEY (membership_ID),
    FOREIGN KEY (user_ID) REFERENCES User (user_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Plan table for workout and diet plans
DROP TABLE IF EXISTS Plan;
CREATE TABLE Plan (
    plan_ID INT AUTO_INCREMENT NOT NULL,
    title VARCHAR(75) NOT NULL,
    workout_rec TEXT,
    diet TEXT,
    difficulty_level ENUM('beginner', 'intermediate', 'advanced'),
    duration_weeks INT,
    created_by INT,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (plan_ID),
    FOREIGN KEY (created_by) REFERENCES User (user_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- Report table for workout analytics and summaries
DROP TABLE IF EXISTS Report;
CREATE TABLE Report (
    report_ID INT AUTO_INCREMENT NOT NULL,
    user_ID INT NOT NULL,
    title VARCHAR(75) NOT NULL,
    checklist TEXT,
    completed_goals TEXT,
    uncompleted_goals TEXT,
    work_efficiency DECIMAL(5,2),
    time_based_summary TEXT NOT NULL,
    workout_duration INT, -- in minutes
    calories_burned INT,
    report_date DATE DEFAULT (CURDATE()),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (report_ID),
    FOREIGN KEY (user_ID) REFERENCES User (user_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Analysis_Team table for team collaboration
DROP TABLE IF EXISTS Analysis_Team;
CREATE TABLE Analysis_Team (
    team_ID INT AUTO_INCREMENT NOT NULL,
    team_name VARCHAR(100) NOT NULL,
    maintenance_task TEXT,
    requests TEXT,
    team_chat_log TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (team_ID)
);

-- System table for system monitoring
DROP TABLE IF EXISTS `system`;
CREATE TABLE `system` (
    system_ID INT AUTO_INCREMENT NOT NULL,
    system_name VARCHAR(100) NOT NULL,
    logs TEXT NOT NULL,
    updates VARCHAR(100),
    alerts VARCHAR(100),
    status ENUM('online', 'offline', 'maintenance') DEFAULT 'online',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (system_ID)
);

-- System_Admin table for system administrators
DROP TABLE IF EXISTS System_Admin;
CREATE TABLE System_Admin (
    admin_ID INT AUTO_INCREMENT NOT NULL,
    user_ID INT NOT NULL,
    shift VARCHAR(50),
    assignedSys_ID INT NOT NULL,
    team_ID INT,
    permissions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (admin_ID),
    FOREIGN KEY (user_ID) REFERENCES User (user_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (assignedSys_ID) REFERENCES `system` (system_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (team_ID) REFERENCES Analysis_Team (team_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- User_Device table for device syncing
DROP TABLE IF EXISTS User_Device;
CREATE TABLE User_Device (
    device_ID INT AUTO_INCREMENT NOT NULL,
    user_ID INT NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    device_name VARCHAR(100),
    transfer VARCHAR(75),
    last_sync TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (device_ID),
    FOREIGN KEY (user_ID) REFERENCES User (user_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Analyst table for data analysts
DROP TABLE IF EXISTS Analyst;
CREATE TABLE Analyst (
    analyst_ID INT AUTO_INCREMENT NOT NULL,
    user_ID INT NOT NULL,
    report_ID INT,
    plan_ID INT,
    admin_ID INT,
    transfer_ID INT,
    specialization VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (analyst_ID),
    FOREIGN KEY (user_ID) REFERENCES User (user_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (report_ID) REFERENCES Report (report_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY (plan_ID) REFERENCES Plan (plan_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY (admin_ID) REFERENCES System_Admin (admin_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY (transfer_ID) REFERENCES User_Device (device_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- Desk_Attendant table for gym staff
DROP TABLE IF EXISTS Desk_Attendant;
CREATE TABLE Desk_Attendant (
    emp_ID INT AUTO_INCREMENT NOT NULL,
    user_ID INT NOT NULL,
    assigned_Area VARCHAR(75),
    shift INT,
    assignedUser_ID INT,
    analyst_ID INT,
    permissions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (emp_ID),
    FOREIGN KEY (user_ID) REFERENCES User (user_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (assignedUser_ID) REFERENCES User (user_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY (analyst_ID) REFERENCES Analyst (analyst_ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- Policy table for gym policies
DROP TABLE IF EXISTS Policy;
CREATE TABLE Policy (
    policy_ID INT AUTO_INCREMENT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (policy_ID)
);

-- Video_Footage table for security monitoring
DROP TABLE IF EXISTS Video_Footage;
CREATE TABLE Video_Footage (
    footage_ID INT AUTO_INCREMENT NOT NULL,
    camera_ID INT NOT NULL,
    location VARCHAR(100),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    duration_seconds INT,
    file_path VARCHAR(255),
    is_archived BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (footage_ID)
);

-- Equipment_Maintenance table for gym equipment
DROP TABLE IF EXISTS Equipment_Maintenance;
CREATE TABLE Equipment_Maintenance (
    equip_ID INT AUTO_INCREMENT NOT NULL,
    equipment_name VARCHAR(100) NOT NULL,
    `condition` ENUM('available', 'maintenance', 'out_of_order') DEFAULT 'available',
    requestForm VARCHAR(128),
    last_maintenance DATE,
    next_maintenance DATE,
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (equip_ID)
);

-- Emp_Only table for employee-only access
DROP TABLE IF EXISTS Emp_Only;
CREATE TABLE Emp_Only (
    emp_ID INT,
    policy_ID INT,
    footage_ID INT,
    equip_ID INT,
    access_level ENUM('read', 'write', 'admin') DEFAULT 'read',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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

-- Workout_Log table for tracking individual workouts
DROP TABLE IF EXISTS Workout_Log;
CREATE TABLE Workout_Log (
    workout_ID INT AUTO_INCREMENT NOT NULL,
    user_ID INT NOT NULL,
    workout_date DATE NOT NULL,
    workout_type VARCHAR(50),
    duration_minutes INT,
    calories_burned INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (workout_ID),
    FOREIGN KEY (user_ID) REFERENCES User (user_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Exercise table for workout exercises
DROP TABLE IF EXISTS Exercise;
CREATE TABLE Exercise (
    exercise_ID INT AUTO_INCREMENT NOT NULL,
    exercise_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    muscle_group VARCHAR(100),
    difficulty_level ENUM('beginner', 'intermediate', 'advanced'),
    instructions TEXT,
    equipment_needed VARCHAR(100),
    PRIMARY KEY (exercise_ID)
);

-- Workout_Exercise table for linking workouts to exercises
DROP TABLE IF EXISTS Workout_Exercise;
CREATE TABLE Workout_Exercise (
    workout_ID INT,
    exercise_ID INT,
    sets INT,
    reps INT,
    weight DECIMAL(6,2),
    duration_seconds INT,
    rest_seconds INT,
    order_index INT,
    FOREIGN KEY (workout_ID) REFERENCES Workout_Log (workout_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (exercise_ID) REFERENCES Exercise (exercise_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    PRIMARY KEY (workout_ID, exercise_ID, order_index)
);

-- Insert sample data

-- Sample Users
INSERT INTO User (name, email, passwordHash, address, gym_location, user_type) VALUES
('Maya Johnson', 'maya.johnson@email.com', 'hash123', '123 Fitness St', 'Downtown Gym', 'regular'),
('Alex LaFrance', 'alex.lafrance@gym.com', 'hash456', '456 Gym Ave', 'Downtown Gym', 'desk_attendant'),
('Jordan Lee', 'jordan.lee@email.com', 'hash789', '789 Tech Blvd', 'Westside Gym', 'analyst'),
('Naomi Smith', 'naomi.smith@admin.com', 'hash101', '101 Admin Rd', 'Central Gym', 'system_admin'),
('Sarah Wilson', 'sarah.wilson@email.com', 'hash202', '202 Health St', 'Downtown Gym', 'regular'),
('Mike Chen', 'mike.chen@email.com', 'hash303', '303 Strength Ave', 'Westside Gym', 'regular');

-- Sample Goals
INSERT INTO Goal (user_ID, goal_name, task, tracking, records, reminders, target_date) VALUES
(1, 'Lose 10 Pounds', 'Cardio & Diet', 'Daily weigh-ins', 'Weekly progress photos', 'Daily at 6 AM', '2025-12-31'),
(1, 'Build Lean Muscle', 'Strength Training', 'Bi-weekly measurements', 'Monthly body composition', 'Every Monday', '2025-12-31'),
(5, 'Improve Endurance', 'HIIT Routines', 'Weekly cardio sessions', 'Running distance logs', 'Every Wednesday', '2025-12-31'),
(6, 'Gain Strength', 'Heavy Lifting', 'Progressive overload', 'Lift progression logs', 'Every Friday', '2025-12-31');

-- Sample Plans
INSERT INTO Plan (title, workout_rec, diet, difficulty_level, duration_weeks, created_by, is_public) VALUES
('Lean Plan', '30 min cardio + weights 3x/week', 'Low carb, high protein', 'intermediate', 12, 3, TRUE),
('Bulk Plan', 'Heavy lifting 4x/week', 'High protein, moderate carbs', 'advanced', 16, 3, TRUE),
('Endurance Plan', 'Running & cycling 5x/week', 'Balanced diet with carbs', 'beginner', 8, 3, TRUE),
('Weight Loss Plan', 'Cardio 5x/week + strength 2x/week', 'Calorie deficit, high protein', 'beginner', 12, 3, TRUE);

-- Sample Reports
INSERT INTO Report (user_ID, title, checklist, completed_goals, uncompleted_goals, work_efficiency, time_based_summary, workout_duration, calories_burned) VALUES
(1, 'Week 1 Summary', 'Stretch, Lift, Run', '2', '1', 85.50, '4h 30min total workout time', 270, 1200),
(1, 'Week 2 Summary', 'Run, Bike, Yoga', '3', '0', 92.00, '5h 15min total workout time', 315, 1400),
(5, 'Week 1 Summary', 'HIIT, Cardio', '1', '1', 78.00, '3h 20min total workout time', 200, 900),
(6, 'Week 1 Summary', 'Bench Press, Squats, Deadlifts', '2', '1', 88.00, '2h 45min total workout time', 165, 800);

-- Sample Analysis Team
INSERT INTO Analysis_Team (team_name, maintenance_task, requests) VALUES
('Fitness Analytics Team', 'Weekly performance review', 'Add new progress tracking metrics'),
('Equipment Maintenance Team', 'Monthly equipment check', 'Replace worn-out gym mats'),
('Safety & Security Team', 'Biweekly safety audit', 'Install additional security cameras');

-- Sample System
INSERT INTO `system` (system_name, logs, updates, alerts) VALUES
('Progress App Server', 'System running normally', 'Patch v1.3 installed', 'All systems operational'),
('Database Server', 'Daily backup completed', 'Database optimized', 'No issues detected'),
('Security System', 'All cameras operational', 'Security protocols updated', 'System secure');

-- Sample System Admin
INSERT INTO System_Admin (user_ID, shift, assignedSys_ID, team_ID, permissions) VALUES
(4, 'Morning', 1, 1, '{"read": true, "write": true, "admin": true}'),
(4, 'Afternoon', 2, 2, '{"read": true, "write": true, "admin": true}'),
(4, 'Night', 3, 3, '{"read": true, "write": true, "admin": true}');

-- Sample User Devices
INSERT INTO User_Device (user_ID, device_type, device_name, transfer) VALUES
(1, 'Smartwatch', 'Apple Watch Series 7', 'Health app sync'),
(1, 'Phone', 'iPhone 14', 'App data sync'),
(3, 'Smartwatch', 'Garmin Fenix', 'Garmin Connect'),
(3, 'Phone', 'Samsung Galaxy', 'Samsung Health');

-- Sample Analyst
INSERT INTO Analyst (user_ID, report_ID, plan_ID, admin_ID, transfer_ID, specialization) VALUES
(3, 1, 1, 1, 3, 'Fitness Analytics'),
(3, 2, 2, 1, 4, 'Performance Optimization'),
(3, 3, 3, 2, 3, 'Data Science');

-- Sample Desk Attendant
INSERT INTO Desk_Attendant (user_ID, assigned_Area, shift, assignedUser_ID, analyst_ID, permissions) VALUES
(2, 'Front Desk', 1, 1, 1, '{"read": true, "write": false, "admin": false}'),
(2, 'Check-in', 2, 5, 2, '{"read": true, "write": false, "admin": false}'),
(2, 'Lobby', 3, 6, 3, '{"read": true, "write": false, "admin": false}');

-- Sample Policies
INSERT INTO Policy (title, description, category) VALUES
('Gym Safety Policy', 'Ensure all equipment is sanitized and in good condition before and after use.', 'Safety'),
('Video Surveillance Policy', 'All areas are monitored for safety and accountability. Footage is stored for 30 days.', 'Security'),
('Emergency Protocols', 'Follow posted protocols in the event of an emergency. Know your nearest exit.', 'Emergency'),
('Equipment Usage Policy', 'Report any equipment issues immediately. Do not use damaged equipment.', 'Equipment'),
('Membership Policy', 'Valid membership required for gym access. Guest passes available with member escort.', 'Membership');

-- Sample Video Footage
INSERT INTO Video_Footage (camera_ID, location, duration_seconds, file_path) VALUES
(1, 'Main Entrance', 3600, '/footage/cam1_2025_08_01.mp4'),
(2, 'Weight Room', 3600, '/footage/cam2_2025_08_01.mp4'),
(3, 'Cardio Area', 3600, '/footage/cam3_2025_08_01.mp4'),
(4, 'Locker Room Entrance', 3600, '/footage/cam4_2025_08_01.mp4');

-- Sample Equipment
INSERT INTO Equipment_Maintenance (equipment_name, `condition`, requestForm, last_maintenance, next_maintenance, location) VALUES
('Treadmill #1', 'available', 'No action needed', '2025-07-15', '2025-08-15', 'Cardio Area'),
('Bench Press #1', 'available', 'No action needed', '2025-07-10', '2025-08-10', 'Weight Room'),
('Elliptical #1', 'maintenance', 'Belt slipping, needs adjustment', '2025-07-01', '2025-08-01', 'Cardio Area'),
('Squat Rack #1', 'available', 'No action needed', '2025-07-20', '2025-08-20', 'Weight Room'),
('Dumbbell Set (5-50 lbs)', 'available', 'No action needed', '2025-07-05', '2025-08-05', 'Weight Room');

-- Sample Memberships
INSERT INTO Membership (user_ID, status, start_date, end_date, billing, plan_type) VALUES
(1, 'active', '2025-01-01 00:00:00', '2025-12-31 23:59:59', 99.99, 'Premium'),
(5, 'active', '2025-06-01 00:00:00', '2026-05-31 23:59:59', 79.99, 'Standard'),
(6, 'active', '2025-07-01 00:00:00', '2026-06-30 23:59:59', 89.99, 'Premium');

-- Sample Exercises
INSERT INTO Exercise (exercise_name, category, muscle_group, difficulty_level, instructions, equipment_needed) VALUES
('Bench Press', 'Strength', 'Chest, Triceps, Shoulders', 'intermediate', 'Lie on bench, lower bar to chest, press up', 'Barbell, Bench'),
('Squats', 'Strength', 'Quadriceps, Glutes, Hamstrings', 'beginner', 'Stand with feet shoulder-width, lower body, stand up', 'Bodyweight or Barbell'),
('Deadlifts', 'Strength', 'Back, Glutes, Hamstrings', 'advanced', 'Stand with feet hip-width, bend down, lift bar', 'Barbell'),
('Push-ups', 'Strength', 'Chest, Triceps, Shoulders', 'beginner', 'Plank position, lower body, push up', 'Bodyweight'),
('Running', 'Cardio', 'Full Body', 'beginner', 'Jog at moderate pace', 'Running Shoes'),
('Cycling', 'Cardio', 'Legs, Core', 'beginner', 'Pedal at moderate resistance', 'Stationary Bike');

-- Sample Workout Logs
INSERT INTO Workout_Log (user_ID, workout_date, workout_type, duration_minutes, calories_burned, notes) VALUES
(1, '2025-08-01', 'Strength Training', 60, 400, 'Great session, felt strong today'),
(1, '2025-08-03', 'Cardio', 45, 350, 'Ran 3 miles, good pace'),
(5, '2025-08-01', 'HIIT', 30, 450, 'High intensity intervals, challenging'),
(6, '2025-08-01', 'Strength Training', 75, 500, 'Heavy lifting day, PR on deadlifts');

-- Sample Workout Exercises
INSERT INTO Workout_Exercise (workout_ID, exercise_ID, sets, reps, weight, duration_seconds, rest_seconds, order_index) VALUES
(1, 1, 3, 8, 135.00, NULL, 120, 1),
(1, 2, 3, 10, 95.00, NULL, 90, 2),
(1, 3, 3, 5, 185.00, NULL, 180, 3),
(2, 5, NULL, NULL, NULL, 2700, 0, 1),
(3, 5, NULL, NULL, NULL, 1800, 0, 1),
(4, 2, 4, 8, 135.00, NULL, 120, 1),
(4, 3, 4, 5, 225.00, NULL, 180, 2);

-- Sample Emp_Only access
INSERT INTO Emp_Only (emp_ID, policy_ID, footage_ID, equip_ID, access_level) VALUES
(1, 1, 1, 1, 'read'),
(1, 2, 2, 2, 'read'),
(1, 3, 3, 3, 'read'),
(1, 4, 4, 4, 'read'),
(1, 5, 1, 5, 'read');

-- Show all tables
SHOW TABLES;

-- Display table counts
SELECT 
    'User' as table_name, COUNT(*) as record_count FROM User
UNION ALL
SELECT 'Goal', COUNT(*) FROM Goal
UNION ALL
SELECT 'Plan', COUNT(*) FROM Plan
UNION ALL
SELECT 'Report', COUNT(*) FROM Report
UNION ALL
SELECT 'Membership', COUNT(*) FROM Membership
UNION ALL
SELECT 'Exercise', COUNT(*) FROM Exercise
UNION ALL
SELECT 'Workout_Log', COUNT(*) FROM Workout_Log;
