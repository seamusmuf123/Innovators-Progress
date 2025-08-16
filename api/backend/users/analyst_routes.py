from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

analyst_bp = Blueprint('analyst_bp', __name__)


@analyst_bp.route('/analysts', methods=['GET'])
def list_analysts():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT analyst_ID, name, email, report_ID, plan_ID, admin_ID, transfer_ID
            FROM Analyst
            ORDER BY analyst_ID
        ''')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing analysts: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@analyst_bp.route('/analysts/<int:analyst_id>', methods=['GET'])
def get_analyst(analyst_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('''
            SELECT analyst_ID, name, email, report_ID, plan_ID, admin_ID, transfer_ID
            FROM Analyst WHERE analyst_ID = %s
        ''', (analyst_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'Analyst not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching analyst {analyst_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@analyst_bp.route('/analysts', methods=['POST'])
def create_analyst():
    try:
        payload = request.json or {}
        name = payload.get('name')
        email = payload.get('email')
        report_ID = payload.get('report_ID')
        plan_ID = payload.get('plan_ID')
        admin_ID = payload.get('admin_ID')
        transfer_ID = payload.get('transfer_ID')

        # report_ID, plan_ID, admin_ID are NOT NULL in schema
        if not (name and email and report_ID and plan_ID and admin_ID):
            return make_response(jsonify({'error': 'name, email, report_ID, plan_ID, admin_ID required'}), 400)

        cursor = db.get_db().cursor()
        cursor.execute('''
            INSERT INTO Analyst (name, email, report_ID, plan_ID, admin_ID, transfer_ID)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name, email, report_ID, plan_ID, admin_ID, transfer_ID))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Analyst created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating analyst: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@analyst_bp.route('/analysts/<int:analyst_id>', methods=['PUT'])
def replace_analyst(analyst_id):
    try:
        payload = request.json or {}
        name = payload.get('name')
        email = payload.get('email')
        report_ID = payload.get('report_ID')
        plan_ID = payload.get('plan_ID')
        admin_ID = payload.get('admin_ID')
        transfer_ID = payload.get('transfer_ID')

        cursor = db.get_db().cursor()
        cursor.execute('''
            UPDATE Analyst SET name=%s, email=%s, report_ID=%s, plan_ID=%s, admin_ID=%s, transfer_ID=%s
            WHERE analyst_ID=%s
        ''', (name, email, report_ID, plan_ID, admin_ID, transfer_ID, analyst_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Analyst updated'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error updating analyst {analyst_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@analyst_bp.route('/analysts/<int:analyst_id>', methods=['PATCH'])
def patch_analyst(analyst_id):
    try:
        payload = request.json or {}
        cols = []
        vals = []
        allowed = ['name', 'email', 'report_ID', 'plan_ID', 'admin_ID', 'transfer_ID']
        for k in allowed:
            if k in payload:
                cols.append(f"{k}=%s")
                vals.append(payload[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields provided'}), 400)
        vals.append(analyst_id)
        query = f"UPDATE Analyst SET {', '.join(cols)} WHERE analyst_ID = %s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Analyst modified'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching analyst {analyst_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@analyst_bp.route('/analysts/<int:analyst_id>', methods=['DELETE'])
def delete_analyst(analyst_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM Analyst WHERE analyst_ID = %s', (analyst_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Analyst deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting analyst {analyst_id}: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


# ---------------------- Analysis Team endpoints ----------------------
@analyst_bp.route('/analysis_team', methods=['GET'])
def list_analysis_teams():
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT team_ID, maintenance_task, requests FROM Analysis_Team ORDER BY team_ID')
        rows = cursor.fetchall()
        return make_response(jsonify(rows), 200)
    except Exception as e:
        current_app.logger.error(f'Error listing analysis teams: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@analyst_bp.route('/analysis_team/<int:team_id>', methods=['GET'])
def get_analysis_team(team_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('SELECT team_ID, maintenance_task, requests FROM Analysis_Team WHERE team_ID=%s', (team_id,))
        row = cursor.fetchone()
        if not row:
            return make_response(jsonify({'error': 'Team not found'}), 404)
        return make_response(jsonify(row), 200)
    except Exception as e:
        current_app.logger.error(f'Error fetching team: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@analyst_bp.route('/analysis_team', methods=['POST'])
def create_analysis_team():
    try:
        p = request.json or {}
        maintenance_task = p.get('maintenance_task')
        requests = p.get('requests')
        cursor = db.get_db().cursor()
        cursor.execute('INSERT INTO Analysis_Team (maintenance_task, requests) VALUES (%s, %s)', (maintenance_task, requests))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Analysis team record created'}), 201)
    except Exception as e:
        current_app.logger.error(f'Error creating analysis team: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@analyst_bp.route('/analysis_team/<int:team_id>', methods=['PUT'])
def replace_analysis_team(team_id):
    try:
        p = request.json or {}
        maintenance_task = p.get('maintenance_task')
        requests = p.get('requests')
        cursor = db.get_db().cursor()
        cursor.execute('UPDATE Analysis_Team SET maintenance_task=%s, requests=%s WHERE team_ID=%s', (maintenance_task, requests, team_id))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Analysis team updated'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error updating team: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@analyst_bp.route('/analysis_team/<int:team_id>', methods=['PATCH'])
def patch_analysis_team(team_id):
    try:
        p = request.json or {}
        cols = []
        vals = []
        allowed = ['maintenance_task', 'requests']
        for k in allowed:
            if k in p:
                cols.append(f"{k}=%s")
                vals.append(p[k])
        if not cols:
            return make_response(jsonify({'error': 'no valid fields'}), 400)
        vals.append(team_id)
        query = f"UPDATE Analysis_Team SET {', '.join(cols)} WHERE team_ID=%s"
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(vals))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Analysis team patched'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error patching team: {e}')
        return make_response(jsonify({'error': str(e)}), 500)


@analyst_bp.route('/analysis_team/<int:team_id>', methods=['DELETE'])
def delete_analysis_team(team_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM Analysis_Team WHERE team_ID=%s', (team_id,))
        db.get_db().commit()
        return make_response(jsonify({'message': 'Analysis team deleted'}), 200)
    except Exception as e:
        current_app.logger.error(f'Error deleting team: {e}')
        return make_response(jsonify({'error': str(e)}), 500)
