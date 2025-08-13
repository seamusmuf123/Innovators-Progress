-- Progress Fitness App - User Stories SQL Queries
-- Based on Task.md requirements for CS 3200 Database Design Project
-- This file contains SQL queries that address all user stories for each persona

USE progress;

-- ============================================================================
-- PERSONA 1: Maya Johnson (Regular User)
-- ============================================================================

-- 1.1: Know what's available for me to use at the gym
-- Query to show available equipment for Maya's gym location
SELECT 
    e.equipment_name,
    e.`condition`,
    e.location,
    e.last_maintenance,
    e.next_maintenance
FROM Equipment_Maintenance e
WHERE e.`condition` = 'available' 
    AND e.location = (SELECT gym_location FROM User WHERE user_ID = 1);

-- 1.2: Weekly reminders to stay consistent with workouts
-- Query to set up weekly reminders for Maya
INSERT INTO Goal (user_ID, goal_name, task, tracking, records, reminders, target_date) 
VALUES (1, 'Weekly Consistency', 'Complete 3 workouts per week', 'Track workout completion', 'Weekly progress log', 'Every Monday at 8 AM', '2025-12-31');

-- 1.3: Routine planning that aligns with fitness goals
-- Query to find workout plans that align with Maya's weight loss goal
SELECT 
    p.title,
    p.workout_rec,
    p.diet,
    p.difficulty_level,
    p.duration_weeks
FROM Plan p
JOIN Goal g ON g.user_ID = 1
WHERE g.goal_name LIKE '%Lose%' 
    AND p.difficulty_level = 'intermediate'
    AND p.is_public = TRUE;

-- 1.4: Set goals that push me to the extent
-- Query to create an ambitious goal for Maya
INSERT INTO Goal (user_ID, goal_name, task, tracking, records, reminders, target_date)
VALUES (1, 'Run 10 Miles Weekly', 'Run 2 miles daily with progressive overload', 'Track each run with GPS', 'Store GPS logs and pace data', 'Daily at 6 AM', '2025-12-31');

-- 1.5: Visual progress tracker
-- Query to get Maya's progress tracking data
SELECT 
    g.goal_name,
    g.tracking,
    g.records,
    g.status,
    g.created_at,
    DATEDIFF(g.target_date, CURDATE()) as days_remaining
FROM Goal g
WHERE g.user_ID = 1 AND g.status = 'active';

-- 1.6: Consistency tracker that helps hold me accountable
-- Query to update Maya's consistency reminders
UPDATE Goal 
SET reminders = 'Daily at 6 AM, Weekly progress review every Sunday'
WHERE user_ID = 1 AND goal_name = 'Run 10 Miles Weekly';

-- ============================================================================
-- PERSONA 2: Alex LaFrance (Desk Attendant)
-- ============================================================================

-- 2.1: Know gym policy
-- Query to get all active gym policies
SELECT 
    p.policy_ID,
    p.title,
    p.description,
    p.category,
    p.created_at
FROM Policy p
WHERE p.is_active = TRUE
ORDER BY p.category, p.title;

-- 2.2: Access to active and inactive gym users
-- Query to get all gym users with their membership status
SELECT 
    u.user_ID,
    u.name,
    u.email,
    u.gym_location,
    m.status as membership_status,
    m.start_date,
    m.end_date,
    CASE 
        WHEN m.status = 'active' AND m.end_date > NOW() THEN 'Active'
        ELSE 'Inactive'
    END as current_status
FROM User u
LEFT JOIN Membership m ON u.user_ID = m.user_ID
WHERE u.user_type = 'regular'
ORDER BY m.status DESC, u.name;

-- 2.3: Access video footage for safety
-- Query to get recent video footage for safety monitoring
SELECT 
    v.footage_ID,
    v.camera_ID,
    v.location,
    v.timestamp,
    v.duration_seconds,
    v.file_path
FROM Video_Footage v
WHERE v.timestamp >= NOW() - INTERVAL 7 DAY
    AND v.is_archived = FALSE
ORDER BY v.timestamp DESC;

-- 2.4: Access to gym equipment that is eligible for use
-- Query to get all available equipment
SELECT 
    e.equip_ID,
    e.equipment_name,
    e.`condition`,
    e.location,
    e.last_maintenance,
    e.next_maintenance,
    CASE 
        WHEN e.`condition` = 'available' THEN 'Ready to use'
        WHEN e.`condition` = 'maintenance' THEN 'Under maintenance'
        ELSE 'Out of order'
    END as status_description
FROM Equipment_Maintenance e
ORDER BY e.location, e.`condition`;

-- 2.5: Access to user requests
-- Query to get all team requests and maintenance tasks
SELECT 
    at.team_ID,
    at.team_name,
    at.maintenance_task,
    at.requests,
    at.team_chat_log,
    at.created_at
FROM Analysis_Team at
ORDER BY at.created_at DESC;

-- 2.6: Ensure users have active memberships
-- Query to verify active memberships for gym access
SELECT 
    u.user_ID,
    u.name,
    u.email,
    m.membership_ID,
    m.status,
    m.start_date,
    m.end_date,
    m.plan_type,
    CASE 
        WHEN m.status = 'active' AND m.end_date > NOW() THEN 'Access Granted'
        ELSE 'Access Denied - Check Membership'
    END as access_status
FROM User u
JOIN Membership m ON u.user_ID = m.user_ID
WHERE u.user_type = 'regular'
ORDER BY m.status, u.name;

-- ============================================================================
-- PERSONA 3: Jordan Lee (Analyst)
-- ============================================================================

-- 3.1: Smart recommendations
-- Query to get smart workout recommendations based on Jordan's goals
SELECT 
    p.plan_ID,
    p.title,
    p.workout_rec,
    p.diet,
    p.difficulty_level,
    p.duration_weeks,
    g.goal_name as user_goal
FROM Plan p
JOIN Goal g ON g.user_ID = 3
WHERE (g.goal_name LIKE '%muscle%' OR g.goal_name LIKE '%strength%' OR g.task LIKE '%lift%')
    AND p.difficulty_level = 'advanced'
    AND p.is_public = TRUE;

-- 3.2: Workout efficiency analytics
-- Query to get Jordan's workout efficiency data
SELECT 
    r.report_ID,
    r.title,
    r.work_efficiency,
    r.workout_duration,
    r.calories_burned,
    r.time_based_summary,
    r.report_date
FROM Report r
WHERE r.user_ID = 3
ORDER BY r.report_date DESC;

-- 3.3: Time-based summaries
-- Query to get time-based workout summaries for Jordan
SELECT 
    r.report_ID,
    r.title,
    r.time_based_summary,
    r.workout_duration,
    r.calories_burned,
    r.report_date,
    CONCAT(
        FLOOR(r.workout_duration / 60), 'h ',
        MOD(r.workout_duration, 60), 'm'
    ) as formatted_duration
FROM Report r
WHERE r.user_ID = 3
ORDER BY r.report_date DESC;

-- 3.4: Goal-based alerts
-- Query to get Jordan's goal reminders and alerts
SELECT 
    g.goal_ID,
    g.goal_name,
    g.task,
    g.reminders,
    g.target_date,
    DATEDIFF(g.target_date, CURDATE()) as days_remaining,
    CASE 
        WHEN DATEDIFF(g.target_date, CURDATE()) <= 7 THEN 'URGENT - Due within a week'
        WHEN DATEDIFF(g.target_date, CURDATE()) <= 30 THEN 'Due within a month'
        ELSE 'On track'
    END as alert_level
FROM Goal g
WHERE g.user_ID = 3 AND g.status = 'active';

-- 3.5: Know user diets
-- Query to get diet information from Jordan's workout plans
SELECT 
    p.plan_ID,
    p.title,
    p.diet,
    p.workout_rec,
    g.goal_name as related_goal
FROM Plan p
JOIN Goal g ON g.user_ID = 3
WHERE p.diet IS NOT NULL
ORDER BY p.created_at DESC;

-- 3.6: Device syncing
-- Query to get Jordan's device information for syncing
SELECT 
    ud.device_ID,
    ud.device_type,
    ud.device_name,
    ud.transfer,
    ud.last_sync,
    ud.is_active,
    u.name as user_name
FROM User_Device ud
JOIN User u ON ud.user_ID = u.user_ID
WHERE ud.user_ID = 3 AND ud.is_active = TRUE;

-- ============================================================================
-- PERSONA 4: Naomi (System Admin)
-- ============================================================================

-- 4.1: Receive alerts when system is down
-- Query to get all system alerts
SELECT 
    s.system_ID,
    s.system_name,
    s.alerts,
    s.status,
    s.last_updated,
    CASE 
        WHEN s.status != 'online' THEN 'CRITICAL - System offline'
        WHEN s.alerts IS NOT NULL THEN 'Alert detected'
        ELSE 'All systems operational'
    END as alert_status
FROM `system` s
WHERE s.alerts IS NOT NULL OR s.status != 'online';

-- 4.2: Schedule regular system updates during off-peak hours
-- Query to update system maintenance schedule
UPDATE `system` 
SET updates = 'Scheduled for 03:00 AM - 05:00 AM daily maintenance window'
WHERE system_ID = 1;

-- 4.3: Automate routine maintenance tasks
-- Query to add automated maintenance task
INSERT INTO Analysis_Team (team_name, maintenance_task, requests) 
VALUES ('System Maintenance Team', 'Automated daily system health check', 'Implement automated monitoring and alerting');

-- 4.4: Access to detailed logs of system activity
-- Query to get all system logs
SELECT 
    s.system_ID,
    s.system_name,
    s.logs,
    s.status,
    s.last_updated,
    sa.admin_ID,
    u.name as admin_name
FROM `system` s
JOIN System_Admin sa ON s.system_ID = sa.assignedSys_ID
JOIN User u ON sa.user_ID = u.user_ID
WHERE s.logs IS NOT NULL
ORDER BY s.last_updated DESC;

-- 4.5: Access to user accounts with memberships to know which ones are inactive
-- Query to get inactive user memberships
SELECT 
    u.user_ID,
    u.name,
    u.email,
    u.gym_location,
    m.membership_ID,
    m.status,
    m.start_date,
    m.end_date,
    m.plan_type,
    CASE 
        WHEN m.status = 'expired' THEN 'Membership Expired'
        WHEN m.status = 'suspended' THEN 'Membership Suspended'
        WHEN m.end_date < NOW() THEN 'Membership Expired (Past End Date)'
        ELSE 'Active'
    END as membership_status
FROM User u
JOIN Membership m ON u.user_ID = m.user_ID
WHERE m.status != 'active' OR m.end_date < NOW()
ORDER BY m.end_date DESC;

-- 4.6: Collaborate with analysis team using team chat
-- Query to add team collaboration request
INSERT INTO Analysis_Team (team_name, maintenance_task, requests) 
VALUES ('System Admin Team', 'Daily system monitoring', 'Team chat for collaboration and real-time communication');

-- ============================================================================
-- ADDITIONAL ANALYTICS QUERIES FOR ALL PERSONAS
-- ============================================================================

-- Cross-persona query: Get overall gym usage statistics
SELECT 
    COUNT(DISTINCT u.user_ID) as total_users,
    COUNT(DISTINCT m.membership_ID) as total_memberships,
    COUNT(DISTINCT CASE WHEN m.status = 'active' THEN m.membership_ID END) as active_memberships,
    COUNT(DISTINCT w.workout_ID) as total_workouts,
    AVG(w.duration_minutes) as avg_workout_duration,
    SUM(w.calories_burned) as total_calories_burned
FROM User u
LEFT JOIN Membership m ON u.user_ID = m.user_ID
LEFT JOIN Workout_Log w ON u.user_ID = w.user_ID;

-- Equipment utilization analysis
SELECT 
    e.location,
    COUNT(*) as total_equipment,
    COUNT(CASE WHEN e.`condition` = 'available' THEN 1 END) as available_equipment,
    COUNT(CASE WHEN e.`condition` = 'maintenance' THEN 1 END) as maintenance_equipment,
    COUNT(CASE WHEN e.`condition` = 'out_of_order' THEN 1 END) as out_of_order_equipment,
    ROUND(
        (COUNT(CASE WHEN e.`condition` = 'available' THEN 1 END) / COUNT(*)) * 100, 2
    ) as availability_percentage
FROM Equipment_Maintenance e
GROUP BY e.location
ORDER BY availability_percentage DESC;

-- User goal completion analysis
SELECT 
    g.goal_name,
    COUNT(*) as total_users,
    COUNT(CASE WHEN g.status = 'completed' THEN 1 END) as completed_goals,
    COUNT(CASE WHEN g.status = 'active' THEN 1 END) as active_goals,
    COUNT(CASE WHEN g.status = 'paused' THEN 1 END) as paused_goals,
    ROUND(
        (COUNT(CASE WHEN g.status = 'completed' THEN 1 END) / COUNT(*)) * 100, 2
    ) as completion_rate
FROM Goal g
GROUP BY g.goal_name
ORDER BY completion_rate DESC;

-- Workout efficiency trends
SELECT 
    DATE_FORMAT(r.report_date, '%Y-%m') as month,
    COUNT(*) as total_reports,
    AVG(r.work_efficiency) as avg_efficiency,
    AVG(r.workout_duration) as avg_duration,
    SUM(r.calories_burned) as total_calories
FROM Report r
GROUP BY DATE_FORMAT(r.report_date, '%Y-%m')
ORDER BY month DESC;

