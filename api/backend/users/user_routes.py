from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Blueprint for user endpoints
users = Blueprint('users', __name__)


# GET /users - list all users
@users.route('/users', methods=['GET'])
def list_users():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT user_ID, name, email, address, gym_location
            FROM User
            ORDER BY user_ID
        ''')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing users: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# GET /users/<id> - get detail
@users.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT user_ID, name, email, address, gym_location FROM User WHERE user_ID = %s', (user_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'User not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching user {user_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# POST /users - create user
@users.route('/users', methods=['POST'])
def create_user():
    try:
        payload = request.json or {}
        name = payload.get('name')
        email = payload.get('email')
        passwordHash = payload.get('passwordHash')
        address = payload.get('address')
        gym_location = payload.get('gym_location')

        if not (email and passwordHash):
            return make_response(jsonify({'error': 'email and passwordHash required'}), 400)

        cursor = db.get_db().cursor()
        cursor.execute('''
            INSERT INTO User (name, email, passwordHash, address, gym_location)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, email, passwordHash, address, gym_location))
        db.get_db().commit()
        return make_response(jsonify({'message': 'User created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating user: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# PUT /users/<id> - full replace
@users.route('/users/<int:user_id>', methods=['PUT'])
def replace_user(user_id):
    try:
        payload = request.json or {}
        name = payload.get('name')
        email = payload.get('email')
        passwordHash = payload.get('passwordHash')
        address = payload.get('address')
        gym_location = payload.get('gym_location')

        cursor = db.get_db().cursor()
        cursor.execute('''
            UPDATE User SET name=%s, email=%s, passwordHash=%s, address=%s, gym_location=%s
            WHERE user_ID=%s
        ''', (name, email, passwordHash, address, gym_location, user_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'User updated'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error replacing user {user_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# PATCH /users/<id> - partial update
@users.route('/users/<int:user_id>', methods=['PATCH'])
def modify_user(user_id):
    try:
        payload = request.json or {}
        # Build dynamic SET clause
        cols = []
        vals = []
        allowed = ['name', 'email', 'passwordHash', 'address', 'gym_location']
        for k in allowed:
            if k in payload:
                cols.append(f"{k}=%s")
                vals.append(payload[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields provided'}), 400)
        vals.append(user_id)
        query = f"UPDATE User SET {', '.join(cols)} WHERE user_ID = %s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'User modified'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching user {user_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# DELETE /users/<id>
@users.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM User WHERE user_ID = %s', (user_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'User deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting user {user_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# ---------------------- Goals (Goal table) ----------------------
@users.route('/goals', methods=['GET'])
def list_goals():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT user_ID, goal_name, task, tracking, records, reminders FROM Goal ORDER BY user_ID')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing goals: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/goals/<int:user_id>/<goal_name>', methods=['GET'])
def get_goal(user_id, goal_name):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT user_ID, goal_name, task, tracking, records, reminders FROM Goal WHERE user_ID=%s AND goal_name=%s', (user_id, goal_name))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'Goal not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching goal: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/goals', methods=['POST'])
def create_goal():
    try:
        p = request.json or {}
        user_ID = p.get('user_ID')
        goal_name = p.get('goal_name')
        task = p.get('task')
        tracking = p.get('tracking')
        records = p.get('records')
        reminders = p.get('reminders')
        if not (user_ID and goal_name):
            return make_response(jsonify({'error': 'user_ID and goal_name required'}), 400)
        cursor = db.get_db().cursor()
        cursor.execute('INSERT INTO Goal (user_ID, goal_name, task, tracking, records, reminders) VALUES (%s,%s,%s,%s,%s,%s)', (user_ID, goal_name, task, tracking, records, reminders))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Goal created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating goal: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/goals/<int:user_id>/<goal_name>', methods=['PUT'])
def replace_goal(user_id, goal_name):
    try:
        p = request.json or {}
        task = p.get('task')
        tracking = p.get('tracking')
        records = p.get('records')
        reminders = p.get('reminders')
        cursor = db.get_db().cursor()
        cursor.execute('UPDATE Goal SET task=%s, tracking=%s, records=%s, reminders=%s WHERE user_ID=%s AND goal_name=%s', (task, tracking, records, reminders, user_id, goal_name))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Goal replaced'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error replacing goal: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/goals/<int:user_id>/<goal_name>', methods=['PATCH'])
def patch_goal(user_id, goal_name):
    try:
        p = request.json or {}
        cols = []
        vals = []
        allowed = ['task', 'tracking', 'records', 'reminders']
        for k in allowed:
            if k in p:
                cols.append(f"{k}=%s")
                vals.append(p[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields'}), 400)
        vals.extend([user_id, goal_name])
        query = f"UPDATE Goal SET {', '.join(cols)} WHERE user_ID=%s AND goal_name=%s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Goal patched'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching goal: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/goals/<int:user_id>/<goal_name>', methods=['DELETE'])
def delete_goal(user_id, goal_name):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM Goal WHERE user_ID=%s AND goal_name=%s', (user_id, goal_name))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Goal deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting goal: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# ---------------------- Plans (Plan table) ----------------------
@users.route('/plans', methods=['GET'])
def list_plans():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT plan_ID, title, workout_rec, diet FROM Plan ORDER BY plan_ID')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing plans: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/plans/<int:plan_id>', methods=['GET'])
def get_plan(plan_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT plan_ID, title, workout_rec, diet FROM Plan WHERE plan_ID=%s', (plan_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'Plan not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching plan: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/plans', methods=['POST'])
def create_plan():
    try:
        p = request.json or {}
        title = p.get('title')
        workout_rec = p.get('workout_rec')
        diet = p.get('diet')
        if not title:
            return make_response(jsonify({'error': 'title required'}), 400)
        cursor = db.get_db().cursor()
        cursor.execute('INSERT INTO Plan (title, workout_rec, diet) VALUES (%s,%s,%s)', (title, workout_rec, diet))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Plan created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating plan: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/plans/<int:plan_id>', methods=['PUT'])
def replace_plan(plan_id):
    try:
        p = request.json or {}
        title = p.get('title')
        workout_rec = p.get('workout_rec')
        diet = p.get('diet')
        cursor = db.get_db().cursor()
        cursor.execute('UPDATE Plan SET title=%s, workout_rec=%s, diet=%s WHERE plan_ID=%s', (title, workout_rec, diet, plan_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Plan replaced'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error replacing plan: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/plans/<int:plan_id>', methods=['PATCH'])
def patch_plan(plan_id):
    try:
        p = request.json or {}
        cols = []
        vals = []
        allowed = ['title', 'workout_rec', 'diet']
        for k in allowed:
            if k in p:
                cols.append(f"{k}=%s")
                vals.append(p[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields'}), 400)
        vals.append(plan_id)
        query = f"UPDATE Plan SET {', '.join(cols)} WHERE plan_ID=%s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Plan patched'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching plan: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/plans/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM Plan WHERE plan_ID=%s', (plan_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Plan deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting plan: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# ---------------------- Reports (Report table) ----------------------
@users.route('/reports', methods=['GET'])
def list_reports():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT report_ID, title, checklist, completed_goals, uncompleted_goals, work_efficiency, time_based_summary FROM Report ORDER BY report_ID')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing reports: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/reports/<int:report_id>', methods=['GET'])
def get_report(report_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT report_ID, title, checklist, completed_goals, uncompleted_goals, work_efficiency, time_based_summary FROM Report WHERE report_ID=%s', (report_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'Report not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching report: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/reports', methods=['POST'])
def create_report():
    try:
        p = request.json or {}
        title = p.get('title')
        checklist = p.get('checklist')
        completed_goals = p.get('completed_goals')
        uncompleted_goals = p.get('uncompleted_goals')
        work_efficiency = p.get('work_efficiency')
        time_based_summary = p.get('time_based_summary')
        if not time_based_summary:
            return make_response(jsonify({'error': 'time_based_summary required'}), 400)
        cursor = db.get_db().cursor()
        cursor.execute('INSERT INTO Report (title, checklist, completed_goals, uncompleted_goals, work_efficiency, time_based_summary) VALUES (%s,%s,%s,%s,%s,%s)', (title, checklist, completed_goals, uncompleted_goals, work_efficiency, time_based_summary))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Report created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating report: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/reports/<int:report_id>', methods=['PUT'])
def replace_report(report_id):
    try:
        p = request.json or {}
        title = p.get('title')
        checklist = p.get('checklist')
        completed_goals = p.get('completed_goals')
        uncompleted_goals = p.get('uncompleted_goals')
        work_efficiency = p.get('work_efficiency')
        time_based_summary = p.get('time_based_summary')
        cursor = db.get_db().cursor()
        cursor.execute('UPDATE Report SET title=%s, checklist=%s, completed_goals=%s, uncompleted_goals=%s, work_efficiency=%s, time_based_summary=%s WHERE report_ID=%s', (title, checklist, completed_goals, uncompleted_goals, work_efficiency, time_based_summary, report_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Report replaced'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error replacing report: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/reports/<int:report_id>', methods=['PATCH'])
def patch_report(report_id):
    try:
        p = request.json or {}
        cols = []
        vals = []
        allowed = ['title', 'checklist', 'completed_goals', 'uncompleted_goals', 'work_efficiency', 'time_based_summary']
        for k in allowed:
            if k in p:
                cols.append(f"{k}=%s")
                vals.append(p[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields'}), 400)
        vals.append(report_id)
        query = f"UPDATE Report SET {', '.join(cols)} WHERE report_ID=%s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Report patched'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching report: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM Report WHERE report_ID=%s', (report_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Report deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting report: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# ---------------------- Memberships (User_Membership) ----------------------
@users.route('/memberships', methods=['GET'])
def list_memberships():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT user_ID, membership_ID, active FROM User_Membership ORDER BY user_ID')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing memberships: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/memberships/<int:user_id>/<int:membership_id>', methods=['GET'])
def get_membership(user_id, membership_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT user_ID, membership_ID, active FROM User_Membership WHERE user_ID=%s AND membership_ID=%s', (user_id, membership_id))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'Membership not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching membership: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/memberships', methods=['POST'])
def create_membership():
    try:
        p = request.json or {}
        user_ID = p.get('user_ID')
        membership_ID = p.get('membership_ID')
        active = p.get('active', 1)
        if not (user_ID and membership_ID):
            return make_response(jsonify({'error': 'user_ID and membership_ID required'}), 400)
        cursor = db.get_db().cursor()
        cursor.execute('INSERT INTO User_Membership (user_ID, membership_ID, active) VALUES (%s,%s,%s)', (user_ID, membership_ID, active))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Membership created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating membership: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/memberships/<int:user_id>/<int:membership_id>', methods=['PUT'])
def replace_membership(user_id, membership_id):
    try:
        p = request.json or {}
        active = p.get('active', 1)
        cursor = db.get_db().cursor()
        cursor.execute('UPDATE User_Membership SET active=%s WHERE user_ID=%s AND membership_ID=%s', (active, user_id, membership_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Membership updated'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error updating membership: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/memberships/<int:user_id>/<int:membership_id>', methods=['DELETE'])
def delete_membership(user_id, membership_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM User_Membership WHERE user_ID=%s AND membership_ID=%s', (user_id, membership_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Membership deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting membership: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# ---------------------- User_Device endpoints ----------------------
@users.route('/devices', methods=['GET'])
def list_devices():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT device_ID, transfer FROM User_Device ORDER BY device_ID')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing devices: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT device_ID, transfer FROM User_Device WHERE device_ID=%s', (device_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'Device not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching device: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/devices', methods=['POST'])
def create_device():
    try:
        p = request.json or {}
        transfer = p.get('transfer')
        cursor = db.get_db().cursor()
        cursor.execute('INSERT INTO User_Device (transfer) VALUES (%s)', (transfer,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Device created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating device: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/devices/<int:device_id>', methods=['PUT'])
def replace_device(device_id):
    try:
        p = request.json or {}
        transfer = p.get('transfer')
        cursor = db.get_db().cursor()
        cursor.execute('UPDATE User_Device SET transfer=%s WHERE device_ID=%s', (transfer, device_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Device updated'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error updating device: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/devices/<int:device_id>', methods=['PATCH'])
def patch_device(device_id):
    try:
        p = request.json or {}
        cols = []
        vals = []
        allowed = ['transfer']
        for k in allowed:
            if k in p:
                cols.append(f"{k}=%s")
                vals.append(p[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields'}), 400)
        vals.append(device_id)
        query = f"UPDATE User_Device SET {', '.join(cols)} WHERE device_ID=%s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Device patched'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching device: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@users.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM User_Device WHERE device_ID=%s', (device_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Device deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting device: {e}')
        return make_response(jsonify({'error': str(e)}), 500)
