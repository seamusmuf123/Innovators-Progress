from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

sysadmin_bp = Blueprint('sysadmin_bp', __name__)


@sysadmin_bp.route('/system_admins', methods=['GET'])
def list_system_admins():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT admin_ID, name, role, contact_email, phone
            FROM System_Admin
            ORDER BY admin_ID
        ''')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing system admins: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@sysadmin_bp.route('/system_admins/<int:admin_id>', methods=['GET'])
def get_system_admin(admin_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT admin_ID, name, role, contact_email, phone FROM System_Admin WHERE admin_ID = %s', (admin_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'System admin not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching system admin {admin_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)

# ---------------------- System endpoints ----------------------
@sysadmin_bp.route('/systems', methods=['GET'])
def list_systems():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT system_ID, logs, updates, alerts FROM `System` ORDER BY system_ID')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing systems: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@sysadmin_bp.route('/systems/<int:system_id>', methods=['GET'])
def get_system(system_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT system_ID, logs, updates, alerts FROM `System` WHERE system_ID = %s', (system_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'System not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching system {system_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@sysadmin_bp.route('/systems', methods=['POST'])
def create_system():
    try:
        payload = request.json or {}
        logs = payload.get('logs')
        updates = payload.get('updates')
        alerts = payload.get('alerts')
        cursor = db.get_db().cursor()
        cursor.execute('INSERT INTO `System` (logs, updates, alerts) VALUES (%s, %s, %s)', (logs, updates, alerts))
        db.get_db().commit()
        return make_response(jsonify({'message': 'System record created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating system: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@sysadmin_bp.route('/systems/<int:system_id>', methods=['PUT'])
def replace_system(system_id):
    try:
        payload = request.json or {}
        logs = payload.get('logs')
        updates = payload.get('updates')
        alerts = payload.get('alerts')
        cursor = db.get_db().cursor()
        cursor.execute('UPDATE `System` SET logs=%s, updates=%s, alerts=%s WHERE system_ID = %s', (logs, updates, alerts, system_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'System updated'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error updating system {system_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@sysadmin_bp.route('/systems/<int:system_id>', methods=['PATCH'])
def patch_system(system_id):
    try:
        payload = request.json or {}
        cols = []
        vals = []
        allowed = ['logs', 'updates', 'alerts']
        for k in allowed:
            if k in payload:
                cols.append(f"{k}=%s")
                vals.append(payload[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields provided'}), 400)
        vals.append(system_id)
        query = f"UPDATE `System` SET {', '.join(cols)} WHERE system_ID = %s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'System patched'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching system {system_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@sysadmin_bp.route('/systems/<int:system_id>', methods=['DELETE'])
def delete_system(system_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM `System` WHERE system_ID = %s', (system_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'System deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting system {system_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


"""
Commented placeholder routes for System Admin endpoints.
"""
@sysadmin_bp.route('/system_admins', methods=['POST'])
def create_system_admin():
    try:
        payload = request.json or {}
        name = payload.get('name')
        role = payload.get('role')
        contact_email = payload.get('contact_email')
        phone = payload.get('phone')

        if not (name and contact_email):
            return make_response(jsonify({'error': 'name and contact_email required'}), 400)

        cursor = db.get_db().cursor()
        cursor.execute('''
            INSERT INTO System_Admin (name, role, contact_email, phone)
            VALUES (%s, %s, %s, %s)
        ''', (name, role, contact_email, phone))
        db.get_db().commit()
        return make_response(jsonify({'message': 'System admin created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating system admin: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@sysadmin_bp.route('/system_admins/<int:admin_id>', methods=['PUT'])
def replace_system_admin(admin_id):
    try:
        payload = request.json or {}
        name = payload.get('name')
        role = payload.get('role')
        contact_email = payload.get('contact_email')
        phone = payload.get('phone')

        cursor = db.get_db().cursor()
        cursor.execute('''
            UPDATE System_Admin SET name=%s, role=%s, contact_email=%s, phone=%s
            WHERE admin_ID=%s
        ''', (name, role, contact_email, phone, admin_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'System admin updated'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error updating system admin {admin_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@sysadmin_bp.route('/system_admins/<int:admin_id>', methods=['PATCH'])
def patch_system_admin(admin_id):
    try:
        payload = request.json or {}
        cols = []
        vals = []
        allowed = ['name', 'role', 'contact_email', 'phone']
        for k in allowed:
            if k in payload:
                cols.append(f"{k}=%s")
                vals.append(payload[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields provided'}), 400)
        vals.append(admin_id)
        query = f"UPDATE System_Admin SET {', '.join(cols)} WHERE admin_ID = %s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'System admin modified'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching system admin {admin_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@sysadmin_bp.route('/system_admins/<int:admin_id>', methods=['DELETE'])
def delete_system_admin(admin_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM System_Admin WHERE admin_ID = %s', (admin_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'System admin deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting system admin {admin_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)
"""
Commented placeholder routes for System Admin endpoints.
"""
from flask import Blueprint, request, jsonify

admin = Blueprint('system_admin', __name__)

# @admin.route('/system_admins', methods=['GET'])
# def list_admins():
#     """GET: Return list of system admins"""
#     pass

# @admin.route('/system_admins', methods=['POST'])
# def create_admin():
#     """POST: Create a new system admin"""
#     pass

# @admin.route('/system_admins/<int:admin_id>', methods=['PUT'])
# def replace_admin(admin_id):
#     """PUT: Replace (full update) a system admin record"""
#     pass

# @admin.route('/system_admins/<int:admin_id>', methods=['PATCH'])
# def modify_admin(admin_id):
#     """PATCH: Partial update for a system admin"""
#     pass

# @admin.route('/system_admins/<int:admin_id>', methods=['DELETE'])
# def delete_admin(admin_id):
#     """DELETE: Remove a system admin"""
#     pass
