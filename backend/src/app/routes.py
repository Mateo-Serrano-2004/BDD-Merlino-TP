from flask import request, jsonify
from app import app
from app.models import SQLHandler, NoSQLHandler

sql_handler = SQLHandler()
no_sql_handler = NoSQLHandler()

@app.route('/add_sql', methods=['POST'])
def add_sql():
    name = request.json['name']
    email = request.json['email']
    sql_handler.add_user(name, email)
    return jsonify({'message': 'SQLUser added to SQL'}), 201

@app.route('/get_sql', methods=['GET'])
def get_sql():
    users = sql_handler.get_all_users()
    users_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(users_data), 200

@app.route('/update_sql/<int:id>', methods=['PUT'])
def update_sql(id):
    name = request.json['name']
    email = request.json['email']
    sql_handler.update_user(id, name, email)
    return jsonify({'message': 'SQLUser updated in SQL'}), 201

@app.route('/delete_sql/<int:id>', methods=['DELETE'])
def delete_sql(id):
    sql_handler.delete_user(id)
    return jsonify({'message': 'SQLUser deleted from SQL'}), 200

@app.route('/add_no_sql', methods=['POST'])
def add_no_sql():
    name = request.json['name']
    email = request.json['email']
    new_user = {'name': name, 'email': email}
    no_sql_handler.create(new_user)
    return jsonify({'message': 'SQLUser added to Mongosql_db'}), 201

@app.route('/get_no_sql', methods=['GET'])
def get_no_sql():
    users = no_sql_handler.read_all()
    users_data = [{'id': str(user['_id']), 'name': user['name'], 'email': user['email']} for user in users]
    return jsonify(users_data), 200

@app.route('/update_no_sql/<user_id>', methods=['PUT'])
def update_no_sql(user_id):
    updated_data = {
        'name': request.json['name'],
        'email': request.json['email']
    }
    no_sql_handler.update(user_id, updated_data)
    return jsonify({'message': 'SQLUser updated in Mongosql_db'}), 201

@app.route('/delete_no_sql/<user_id>', methods=['DELETE'])
def delete_no_sql(user_id):
    no_sql_handler.delete(user_id)
    return jsonify({'message': 'SQLUser deleted from Mongosql_db'}), 200
