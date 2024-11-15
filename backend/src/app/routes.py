from flask import request, jsonify
from . import db
from .models import UserSQL, UserNoSQL

def create_user_sql():
    data = request.get_json()
    new_user = UserSQL(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created in SQL DB'}), 201

def get_users_sql():
    users = UserSQL.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

def delete_user_sql(user_id):
    user = UserSQL.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted from SQL DB'}), 200

def update_user_sql(user_id):
    data = request.get_json()
    user = UserSQL.query.get_or_404(user_id)
    user.name = data['name']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated in SQL DB'}), 200

def create_user_nosql():
    data = request.get_json()
    user_data = UserNoSQL(_id=None, name=data['name'], email=data['email'])
    user = dict(name=user_data.name, email=user_data.email)
    app.mongo_db.users.insert_one(user)
    return jsonify({'message': 'User created in NoSQL DB'}), 201

def get_users_nosql():
    users = app.mongo_db.users.find()
    return jsonify([{'name': user['name'], 'email': user['email']} for user in users])

def delete_user_nosql(user_id):
    result = app.mongo_db.users.delete_one({'_id': user_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted from NoSQL DB'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

def update_user_nosql(user_id):
    data = request.get_json()
    result = app.mongo_db.users.update_one({'_id': user_id}, {'$set': {'name': data['name'], 'email': data['email']}})
    if result.matched_count > 0:
        return jsonify({'message': 'User updated in NoSQL DB'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
