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

