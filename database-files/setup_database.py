#!/usr/bin/env python3
"""
Database Setup Script for Progress Fitness App
This script creates the database schema and populates it with sample data.
"""

import mysql.connector
from mysql.connector import Error
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'port': 3306
}

def create_database():
    """Create the progress database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS progress")
        print("✅ Database 'progress' created successfully")
        
        cursor.close()
        connection.close()
        
        # Connect to the progress database
        DB_CONFIG['database'] = 'progress'
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        return connection, cursor
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return None, None

def create_tables(cursor):
    """Create all required tables"""
    try:
        # User table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            user_ID INT AUTO_INCREMENT NOT NULL,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(75) UNIQUE NOT NULL,
            passwordHash VARCHAR(128) NOT NULL,
            address VARCHAR(128),
            gym_location VARCHAR(50) NOT NULL,
            user_type ENUM('regular', 'staff', 'admin') DEFAULT 'regular',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_ID)
        )
        """)
        
        # Goal table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Goal (
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
            FOREIGN KEY (user_ID) REFERENCES User (user_ID) ON DELETE CASCADE
        )
        """)
        
        # Membership table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Membership (
            membership_ID INT AUTO_INCREMENT NOT NULL,
            user_ID INT NOT NULL,
            status ENUM('active', 'expired', 'cancelled') DEFAULT 'active',
            start_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL,
            billing DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (membership_ID),
            FOREIGN KEY (user_ID) REFERENCES User (user_ID) ON DELETE CASCADE
        )
        """)
        
        # Report table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Report (
            report_ID INT AUTO_INCREMENT NOT NULL,
            user_ID INT NOT NULL,
            title VARCHAR(75) NOT NULL,
            checklist TEXT,
            completed_goals TEXT,
            uncompleted_goals TEXT,
            work_efficiency DECIMAL(5,2),
            workout_duration INT,
            calories_burned INT,
            time_based_summary TEXT,
            report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (report_ID),
            FOREIGN KEY (user_ID) REFERENCES User (user_ID) ON DELETE CASCADE
        )
        """)
        
        # Plan table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Plan (
            plan_ID INT AUTO_INCREMENT NOT NULL,
            user_ID INT NOT NULL,
            title VARCHAR(75) NOT NULL,
            workout_rec TEXT,
            diet TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (plan_ID),
            FOREIGN KEY (user_ID) REFERENCES User (user_ID) ON DELETE CASCADE
        )
        """)
        
        # Policy table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Policy (
            policy_ID INT AUTO_INCREMENT NOT NULL,
            title VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            category VARCHAR(50),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (policy_ID)
        )
        """)
        
        # Equipment_Maintenance table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Equipment_Maintenance (
            equip_ID INT AUTO_INCREMENT NOT NULL,
            equipment_name VARCHAR(100) NOT NULL,
            `condition` ENUM('available', 'maintenance', 'out_of_order') DEFAULT 'available',
            location VARCHAR(100) NOT NULL,
            last_maintenance DATE,
            next_maintenance DATE,
            requestForm TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (equip_ID)
        )
        """)
        
        # Workout_Log table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Workout_Log (
            workout_ID INT AUTO_INCREMENT NOT NULL,
            user_ID INT NOT NULL,
            workout_date DATE NOT NULL,
            duration_minutes INT,
            calories_burned INT,
            workout_type VARCHAR(50),
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (workout_ID),
            FOREIGN KEY (user_ID) REFERENCES User (user_ID) ON DELETE CASCADE
        )
        """)
        
        print("✅ All tables created successfully")
        
    except Error as e:
        print(f"❌ Error creating tables: {e}")

def insert_sample_data(cursor):
    """Insert sample data into tables"""
    try:
        # Insert sample users
        users_data = [
            (1, 'Maya Johnson', 'maya@email.com', 'hash123', '123 Main St', 'Downtown Gym', 'regular'),
            (2, 'Alex LaFrance', 'alex@gym.com', 'hash456', '456 Oak Rd', 'Downtown Gym', 'staff'),
            (3, 'Jordan Lee', 'jordan@email.com', 'hash789', '789 Pine Ln', 'Westside Gym', 'regular'),
            (4, 'Naomi Smith', 'naomi@admin.com', 'hash101', '101 Admin Ave', 'Central Gym', 'admin')
        ]
        
        cursor.executemany("""
        INSERT INTO User (user_ID, name, email, passwordHash, address, gym_location, user_type) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, users_data)
        
        # Insert sample goals
        goals_data = [
            (1, 1, 'Lose 10 Pounds', 'Cardio & Diet', 'Daily tracking', 'Weekly progress photos', 'Weekly reminders', '2025-12-31', 'active'),
            (2, 1, 'Build Lean Muscle', 'Strength Training', 'Bi-weekly measurements', 'Monthly progress', 'Daily motivation', '2025-12-31', 'active'),
            (3, 3, 'Improve Endurance', 'HIIT Routines', 'Heart rate tracking', 'Weekly tests', 'Morning alerts', '2025-12-31', 'active')
        ]
        
        cursor.executemany("""
        INSERT INTO Goal (goal_ID, user_ID, goal_name, task, tracking, records, reminders, target_date, status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, goals_data)
        
        # Insert sample memberships
        memberships_data = [
            (1, 1, 'active', '2025-01-01 00:00:00', '2025-12-31 23:59:59', 99.99),
            (2, 2, 'active', '2025-01-01 00:00:00', '2025-12-31 23:59:59', 0.00),
            (3, 3, 'active', '2025-06-01 00:00:00', '2026-05-31 23:59:59', 79.99),
            (4, 4, 'active', '2025-01-01 00:00:00', '2025-12-31 23:59:59', 0.00)
        ]
        
        cursor.executemany("""
        INSERT INTO Membership (membership_ID, user_ID, status, start_date, end_date, billing) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """, memberships_data)
        
        # Insert sample reports
        reports_data = [
            (1, 3, 'Week 1 Summary', 'Stretch, Lift, Run', '2 goals completed', '1 goal pending', 85.5, 270, 1200, '4h 30min total'),
            (2, 3, 'Week 2 Summary', 'Run, Bike, Swim', '1 goal completed', '2 goals pending', 92.0, 315, 1400, '5h 15min total')
        ]
        
        cursor.executemany("""
        INSERT INTO Report (report_ID, user_ID, title, checklist, completed_goals, uncompleted_goals, work_efficiency, workout_duration, calories_burned, time_based_summary) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, reports_data)
        
        # Insert sample policies
        policies_data = [
            (1, 'Gym Safety Policy', 'Ensure all equipment is sanitized and in good condition before and after use.', 'Safety'),
            (2, 'Video Surveillance Policy', 'All areas are monitored for safety and accountability. Footage is stored for 30 days.', 'Security'),
            (3, 'Emergency Protocols', 'Follow posted protocols in the event of an emergency. Know your nearest exit.', 'Safety')
        ]
        
        cursor.executemany("""
        INSERT INTO Policy (policy_ID, title, description, category) 
        VALUES (%s, %s, %s, %s)
        """, policies_data)
        
        # Insert sample equipment
        equipment_data = [
            (1, 'Treadmill #1', 'available', 'Cardio Area', '2025-07-01', '2025-10-01', 'No action needed'),
            (2, 'Bench Press #1', 'available', 'Weight Room', '2025-07-15', '2025-10-15', 'No action needed'),
            (3, 'Elliptical #1', 'maintenance', 'Cardio Area', '2025-06-01', '2025-09-01', 'Belt replacement needed'),
            (4, 'Dumbbell Set 20lb', 'available', 'Weight Room', '2025-07-01', '2025-10-01', 'No action needed')
        ]
        
        cursor.executemany("""
        INSERT INTO Equipment_Maintenance (equip_ID, equipment_name, `condition`, location, last_maintenance, next_maintenance, requestForm) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, equipment_data)
        
        # Insert sample workout logs
        workout_data = [
            (1, 1, '2025-08-10', 45, 300, 'Cardio', 'Great session, felt energized'),
            (2, 1, '2025-08-12', 60, 400, 'Strength', 'Focused on form, increased weight'),
            (3, 3, '2025-08-11', 90, 600, 'HIIT', 'High intensity intervals, excellent performance'),
            (4, 3, '2025-08-13', 75, 500, 'Mixed', 'Combined cardio and strength')
        ]
        
        cursor.executemany("""
        INSERT INTO Workout_Log (workout_ID, user_ID, workout_date, duration_minutes, calories_burned, workout_type, notes) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, workout_data)
        
        print("✅ Sample data inserted successfully")
        
    except Error as e:
        print(f"❌ Error inserting sample data: {e}")

def main():
    """Main function to set up the database"""
    print("🚀 Setting up Progress Fitness App Database...")
    
    # Create database and get connection
    connection, cursor = create_database()
    if not connection or not cursor:
        print("❌ Failed to create database connection")
        return
    
    try:
        # Create tables
        create_tables(cursor)
        
        # Insert sample data
        insert_sample_data(cursor)
        
        # Commit changes
        connection.commit()
        print("✅ Database setup completed successfully!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM User")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Goal")
        goal_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Equipment_Maintenance")
        equipment_count = cursor.fetchone()[0]
        
        print(f"\n📊 Database Summary:")
        print(f"   Users: {user_count}")
        print(f"   Goals: {goal_count}")
        print(f"   Equipment: {equipment_count}")
        
    except Error as e:
        print(f"❌ Error during setup: {e}")
        connection.rollback()
    
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
