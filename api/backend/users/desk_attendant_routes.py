from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

desk_bp = Blueprint('desk_bp', __name__)


@desk_bp.route('/desk_attendants', methods=['GET'])
def list_desk_attendants():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT emp_ID, name, email, assigned_Area, shift, assignedUser_ID, analyst_ID
            FROM Desk_Attendant
            ORDER BY emp_ID
        ''')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing desk attendants: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/desk_attendants/<int:emp_id>', methods=['GET'])
def get_desk_attendant(emp_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT emp_ID, name, email, assigned_Area, shift, assignedUser_ID, analyst_ID FROM Desk_Attendant WHERE emp_ID = %s', (emp_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'Desk attendant not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching desk attendant {emp_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/desk_attendants', methods=['POST'])
def create_desk_attendant():
    try:
        payload = request.json or {}
        name = payload.get('name')
        email = payload.get('email')
        assigned_Area = payload.get('assigned_Area')
        shift = payload.get('shift')
        assignedUser_ID = payload.get('assignedUser_ID')
        analyst_ID = payload.get('analyst_ID')

        # analyst_ID is NOT NULL in schema
        if not (name and email and analyst_ID):
            return make_response(jsonify({'error': 'name, email and analyst_ID required'}), 400)

        cursor = db.get_db().cursor()
        cursor.execute('''
            INSERT INTO Desk_Attendant (name, email, assigned_Area, shift, assignedUser_ID, analyst_ID)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name, email, assigned_Area, shift, assignedUser_ID, analyst_ID))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Desk attendant created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating desk attendant: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/desk_attendants/<int:emp_id>', methods=['PUT'])
def replace_desk_attendant(emp_id):
    try:
        payload = request.json or {}
        name = payload.get('name')
        email = payload.get('email')
        assigned_Area = payload.get('assigned_Area')
        shift = payload.get('shift')
        assignedUser_ID = payload.get('assignedUser_ID')
        analyst_ID = payload.get('analyst_ID')

        cursor = db.get_db().cursor()
        cursor.execute('''
            UPDATE Desk_Attendant SET name=%s, email=%s, assigned_Area=%s, shift=%s, assignedUser_ID=%s, analyst_ID=%s
            WHERE emp_ID=%s
        ''', (name, email, assigned_Area, shift, assignedUser_ID, analyst_ID, emp_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Desk attendant updated'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error updating desk attendant {emp_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/desk_attendants/<int:emp_id>', methods=['PATCH'])
def patch_desk_attendant(emp_id):
    try:
        payload = request.json or {}
        cols = []
        vals = []
        allowed = ['name', 'email', 'assigned_Area', 'shift', 'assignedUser_ID', 'analyst_ID']
        for k in allowed:
            if k in payload:
                cols.append(f"{k}=%s")
                vals.append(payload[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields provided'}), 400)
        vals.append(emp_id)
        query = f"UPDATE Desk_Attendant SET {', '.join(cols)} WHERE emp_ID = %s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Desk attendant modified'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching desk attendant {emp_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/desk_attendants/<int:emp_id>', methods=['DELETE'])
def delete_desk_attendant(emp_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM Desk_Attendant WHERE emp_ID = %s', (emp_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Desk attendant deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting desk attendant {emp_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)

"""
Desk attendant endpoints implemented above.
"""


# ---------------------- Policy endpoints ----------------------
@desk_bp.route('/policies', methods=['GET'])
def list_policies():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT policy_ID, title, description FROM Policy ORDER BY policy_ID')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing policies: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/policies/<int:policy_id>', methods=['GET'])
def get_policy(policy_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT policy_ID, title, description FROM Policy WHERE policy_ID=%s', (policy_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'Policy not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching policy: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/policies', methods=['POST'])
def create_policy():
    try:
        p = request.json or {}
        title = p.get('title')
        description = p.get('description')
        if not (title and description):
            return make_response(jsonify({'error': 'title and description required'}), 400)
        cursor = db.get_db().cursor()
        cursor.execute('INSERT INTO Policy (title, description) VALUES (%s, %s)', (title, description))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Policy created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating policy: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/policies/<int:policy_id>', methods=['PUT'])
def replace_policy(policy_id):
    try:
        p = request.json or {}
        title = p.get('title')
        description = p.get('description')
        cursor = db.get_db().cursor()
        cursor.execute('UPDATE Policy SET title=%s, description=%s WHERE policy_ID=%s', (title, description, policy_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Policy updated'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error updating policy: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/policies/<int:policy_id>', methods=['PATCH'])
def patch_policy(policy_id):
    try:
        p = request.json or {}
        cols = []
        vals = []
        allowed = ['title', 'description']
        for k in allowed:
            if k in p:
                cols.append(f"{k}=%s")
                vals.append(p[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields'}), 400)
        vals.append(policy_id)
        query = f"UPDATE Policy SET {', '.join(cols)} WHERE policy_ID=%s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Policy patched'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching policy: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/policies/<int:policy_id>', methods=['DELETE'])
def delete_policy(policy_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM Policy WHERE policy_ID=%s', (policy_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Policy deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting policy: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# ---------------------- Video Footage endpoints ----------------------
@desk_bp.route('/video_footage', methods=['GET'])
def list_footage():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT footage_ID, camera_ID, timestamp FROM Video_Footage ORDER BY footage_ID')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing footage: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/video_footage/<int:footage_id>', methods=['GET'])
def get_footage(footage_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT footage_ID, camera_ID, timestamp FROM Video_Footage WHERE footage_ID=%s', (footage_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'Footage not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching footage: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/video_footage', methods=['POST'])
def create_footage():
    try:
        p = request.json or {}
        camera_ID = p.get('camera_ID')
        timestamp = p.get('timestamp')
        if not camera_ID:
            return make_response(jsonify({'error': 'camera_ID required'}), 400)
        cursor = db.get_db().cursor()
        cursor.execute('INSERT INTO Video_Footage (camera_ID, timestamp) VALUES (%s, %s)', (camera_ID, timestamp))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Footage record created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating footage: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/video_footage/<int:footage_id>', methods=['DELETE'])
def delete_footage(footage_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM Video_Footage WHERE footage_ID=%s', (footage_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Footage deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting footage: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# ---------------------- Equipment Maintenance endpoints ----------------------
@desk_bp.route('/equipment', methods=['GET'])
def list_equipment():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT equip_ID, `condition`, requestForm FROM Equipment_Maintenance ORDER BY equip_ID')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing equipment: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/equipment/<int:equip_id>', methods=['GET'])
def get_equipment(equip_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT equip_ID, `condition`, requestForm FROM Equipment_Maintenance WHERE equip_ID=%s', (equip_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'Equipment not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching equipment: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/equipment', methods=['POST'])
def create_equipment():
    try:
        p = request.json or {}
        condition = p.get('condition')
        requestForm = p.get('requestForm')
        cursor = db.get_db().cursor()
        cursor.execute('INSERT INTO Equipment_Maintenance (`condition`, requestForm) VALUES (%s, %s)', (condition, requestForm))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Equipment record created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating equipment: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/equipment/<int:equip_id>', methods=['PUT'])
def replace_equipment(equip_id):
    try:
        p = request.json or {}
        condition = p.get('condition')
        requestForm = p.get('requestForm')
        cursor = db.get_db().cursor()
        cursor.execute('UPDATE Equipment_Maintenance SET `condition`=%s, requestForm=%s WHERE equip_ID=%s', (condition, requestForm, equip_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Equipment updated'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error updating equipment: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@desk_bp.route('/equipment/<int:equip_id>', methods=['PATCH'])
def patch_equipment(equip_id):
    try:
        p = request.json or {}
        cols = []
        vals = []
        allowed = ['condition', 'requestForm']
        for k in allowed:
            if k in p:
                cols.append(f"`{k}`=%s" if k == 'condition' else f"{k}=%s")
                vals.append(p[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields'}), 400)
        vals.append(equip_id)
        query = f"UPDATE Equipment_Maintenance SET {', '.join(cols)} WHERE equip_ID=%s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Equipment patched'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching equipment: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


