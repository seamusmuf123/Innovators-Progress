from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import json
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'database': os.getenv('DB_NAME', 'progress'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# ============================================================================
# PERSONA 1: Maya Johnson (Regular User) - Fitness Tracking Endpoints
# ============================================================================

@app.route('/api/equipment/available', methods=['GET'])
def get_available_equipment():
    """Get available equipment for a specific gym location"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id parameter required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        # Get user's gym location and available equipment
        query = """
        SELECT e.equipment_name, e.`condition`, e.location, 
               e.last_maintenance, e.next_maintenance
        FROM Equipment_Maintenance e
        WHERE e.`condition` = 'available' 
            AND e.location = (SELECT gym_location FROM User WHERE user_ID = %s)
        """
        
        cursor.execute(query, (user_id,))
        equipment = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'user_id': user_id,
            'equipment': equipment,
            'count': len(equipment)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/goals', methods=['GET', 'POST'])
def manage_goals():
    """Get user goals or create new goal"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'GET':
            user_id = request.args.get('user_id', type=int)
            if not user_id:
                return jsonify({'error': 'user_id parameter required'}), 400
            
            query = """
            SELECT goal_ID, goal_name, task, tracking, records, 
                   reminders, target_date, status, created_at
            FROM Goal 
            WHERE user_ID = %s
            ORDER BY created_at DESC
            """
            
            cursor.execute(query, (user_id,))
            goals = cursor.fetchall()
            
            return jsonify({
                'user_id': user_id,
                'goals': goals,
                'count': len(goals)
            })
            
        elif request.method == 'POST':
            data = request.get_json()
            required_fields = ['user_ID', 'goal_name']
            
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Missing required fields'}), 400
            
            query = """
            INSERT INTO Goal (user_ID, goal_name, task, tracking, records, 
                            reminders, target_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                data['user_ID'],
                data['goal_name'],
                data.get('task'),
                data.get('tracking'),
                data.get('records'),
                data.get('reminders'),
                data.get('target_date'),
                data.get('status', 'active')
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            goal_id = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'message': 'Goal created successfully',
                'goal_id': goal_id,
                'goal': data
            }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plans/recommended', methods=['GET'])
def get_recommended_plans():
    """Get workout plans that align with user's fitness goals"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id parameter required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT p.plan_ID, p.title, p.workout_rec, p.diet, 
               p.difficulty_level, p.duration_weeks
        FROM Plan p
        JOIN Goal g ON g.user_ID = %s
        WHERE p.is_public = TRUE
        ORDER BY p.difficulty_level, p.duration_weeks
        """
        
        cursor.execute(query, (user_id,))
        plans = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'user_id': user_id,
            'plans': plans,
            'count': len(plans)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress/tracker', methods=['GET'])
def get_progress_tracker():
    """Get user's progress tracking data"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id parameter required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT g.goal_name, g.tracking, g.records, g.status, 
               g.created_at, g.target_date,
               DATEDIFF(g.target_date, CURDATE()) as days_remaining
        FROM Goal g
        WHERE g.user_ID = %s AND g.status = 'active'
        ORDER BY g.created_at DESC
        """
        
        cursor.execute(query, (user_id,))
        goals = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'user_id': user_id,
            'goals': goals,
            'count': len(goals)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# PERSONA 2: Alex LaFrance (Desk Attendant) - Gym Management Endpoints
# ============================================================================

@app.route('/api/policies', methods=['GET'])
def get_gym_policies():
    """Get all active gym policies"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT policy_ID, title, description, category, created_at
        FROM Policy 
        WHERE is_active = TRUE
        ORDER BY category, title
        """
        
        cursor.execute(query)
        policies = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'policies': policies,
            'count': len(policies)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/membership-status', methods=['GET'])
def get_user_membership_status():
    """Get all gym users with their membership status"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT u.user_ID, u.name, u.email, u.gym_location,
               m.status as membership_status, m.start_date, m.end_date,
               CASE 
                   WHEN m.status = 'active' AND m.end_date > NOW() THEN 'Active'
                   ELSE 'Inactive'
               END as current_status
        FROM User u
        LEFT JOIN Membership m ON u.user_ID = m.user_ID
        WHERE u.user_type = 'regular'
        ORDER BY m.status DESC, u.name
        """
        
        cursor.execute(query)
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'users': users,
            'count': len(users)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/security/video-footage', methods=['GET'])
def get_video_footage():
    """Get recent video footage for safety monitoring"""
    try:
        days = request.args.get('days', 7, type=int)
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT footage_ID, camera_ID, location, timestamp, 
               duration_seconds, file_path
        FROM Video_Footage 
        WHERE timestamp >= NOW() - INTERVAL %s DAY
            AND is_archived = FALSE
        ORDER BY timestamp DESC
        """
        
        cursor.execute(query, (days,))
        footage = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'footage': footage,
            'count': len(footage),
            'days_back': days
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/equipment/status', methods=['GET'])
def get_equipment_status():
    """Get all gym equipment status"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT equip_ID, equipment_name, `condition`, location,
               last_maintenance, next_maintenance,
               CASE 
                   WHEN `condition` = 'available' THEN 'Ready to use'
                   WHEN `condition` = 'maintenance' THEN 'Under maintenance'
                   ELSE 'Out of order'
               END as status_description
        FROM Equipment_Maintenance 
        ORDER BY location, `condition`
        """
        
        cursor.execute(query)
        equipment = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'equipment': equipment,
            'count': len(equipment)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# PERSONA 3: Jordan Lee (Analyst) - Analytics Endpoints
# ============================================================================

@app.route('/api/analytics/workout-efficiency', methods=['GET'])
def get_workout_efficiency():
    """Get user's workout efficiency analytics"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id parameter required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT report_ID, title, work_efficiency, workout_duration,
               calories_burned, time_based_summary, report_date
        FROM Report 
        WHERE user_ID = %s
        ORDER BY report_date DESC
        """
        
        cursor.execute(query, (user_id,))
        reports = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'user_id': user_id,
            'reports': reports,
            'count': len(reports)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/time-summaries', methods=['GET'])
def get_time_summaries():
    """Get time-based workout summaries"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id parameter required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT report_ID, title, time_based_summary, workout_duration,
               calories_burned, report_date,
               CONCAT(
                   FLOOR(workout_duration / 60), 'h ',
                   MOD(workout_duration, 60), 'm'
               ) as formatted_duration
        FROM Report 
        WHERE user_ID = %s
        ORDER BY report_date DESC
        """
        
        cursor.execute(query, (user_id,))
        summaries = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'user_id': user_id,
            'summaries': summaries,
            'count': len(summaries)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/sync', methods=['GET'])
def get_device_sync_info():
    """Get user's device information for syncing"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id parameter required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT ud.device_ID, ud.device_type, ud.device_name,
               ud.transfer, ud.last_sync, ud.is_active,
               u.name as user_name
        FROM User_Device ud
        JOIN User u ON ud.user_ID = u.user_ID
        WHERE ud.user_ID = %s AND ud.is_active = TRUE
        """
        
        cursor.execute(query, (user_id,))
        devices = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'user_id': user_id,
            'devices': devices,
            'count': len(devices)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# PERSONA 4: Naomi (System Admin) - System Management Endpoints
# ============================================================================

@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    """Get system status and alerts"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT system_ID, system_name, alerts, status, last_updated,
               CASE 
                   WHEN status != 'online' THEN 'CRITICAL - System offline'
                   WHEN alerts IS NOT NULL THEN 'Alert detected'
                   ELSE 'All systems operational'
               END as alert_status
        FROM `system`
        WHERE alerts IS NOT NULL OR status != 'online'
        """
        
        cursor.execute(query)
        systems = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'systems': systems,
            'count': len(systems)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/logs', methods=['GET'])
def get_system_logs():
    """Get detailed system activity logs"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT s.system_ID, s.system_name, s.logs, s.status,
               s.last_updated, sa.admin_ID, u.name as admin_name
        FROM `system` s
        JOIN System_Admin sa ON s.system_ID = sa.assignedSys_ID
        JOIN User u ON sa.user_ID = u.user_ID
        WHERE s.logs IS NOT NULL
        ORDER BY s.last_updated DESC
        """
        
        cursor.execute(query)
        logs = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'logs': logs,
            'count': len(logs)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/inactive-memberships', methods=['GET'])
def get_inactive_memberships():
    """Get users with inactive memberships"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT u.user_ID, u.name, u.email, u.gym_location,
               m.membership_ID, m.status, m.start_date, m.end_date,
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
        ORDER BY m.end_date DESC
        """
        
        cursor.execute(query)
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'users': users,
            'count': len(users)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# GENERAL ANALYTICS ENDPOINTS
# ============================================================================

@app.route('/api/analytics/gym-usage', methods=['GET'])
def get_gym_usage_stats():
    """Get overall gym usage statistics"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            COUNT(DISTINCT u.user_ID) as total_users,
            COUNT(DISTINCT m.membership_ID) as total_memberships,
            COUNT(DISTINCT CASE WHEN m.status = 'active' THEN m.membership_ID END) as active_memberships,
            COUNT(DISTINCT w.workout_ID) as total_workouts,
            AVG(w.duration_minutes) as avg_workout_duration,
            SUM(w.calories_burned) as total_calories_burned
        FROM User u
        LEFT JOIN Membership m ON u.user_ID = m.user_ID
        LEFT JOIN Workout_Log w ON u.user_ID = w.user_ID
        """
        
        cursor.execute(query)
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/equipment-utilization', methods=['GET'])
def get_equipment_utilization():
    """Get equipment utilization analysis"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            location,
            COUNT(*) as total_equipment,
            COUNT(CASE WHEN `condition` = 'available' THEN 1 END) as available_equipment,
            COUNT(CASE WHEN `condition` = 'maintenance' THEN 1 END) as maintenance_equipment,
            COUNT(CASE WHEN `condition` = 'out_of_order' THEN 1 END) as out_of_order_equipment,
            ROUND(
                (COUNT(CASE WHEN `condition` = 'available' THEN 1 END) / COUNT(*)) * 100, 2
            ) as availability_percentage
        FROM Equipment_Maintenance 
        GROUP BY location
        ORDER BY availability_percentage DESC
        """
        
        cursor.execute(query)
        utilization = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'utilization': utilization,
            'count': len(utilization)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
