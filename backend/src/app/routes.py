from flask import request
from flask_restx import Resource
from app import api
from app.models import SQLHandler, NoSQLHandler

sql_handler = SQLHandler()
no_sql_handler = NoSQLHandler()

@api.route('/sql/users')
class UsersSQL(Resource):
    def get(self):
        users = sql_handler.get_all_users()
        return users, 200

    def post(self):
        name = request.json['name']
        email = request.json['email']
        sql_handler.add_user(name, email)
        return {'message': 'User added to SQL database'}, 201

@api.route('/sql/users/<int:id>')
class UserSQL(Resource):
    def put(self, id):
        name = request.json['name']
        email = request.json['email']
        sql_handler.update_user(id, name, email)
        return {'message': 'User updated in SQL database'}, 200

    def delete(self, id):
        sql_handler.delete_user(id)
        return {'message': 'User deleted from SQL database'}, 200

@api.route('/no_sql/users')
class UsersNoSQL(Resource):
    def get(self):
        users = no_sql_handler.read_all()
        return users, 200

    def post(self):
        name = request.json['name']
        email = request.json['email']
        new_user = {'name': name, 'email': email}
        no_sql_handler.create(new_user)
        return {'message': 'User added to NoSQL database'}, 201

@api.route('/no_sql/users/<user_id>')
class UserNoSQL(Resource):
    def put(self, user_id):
        updated_data = {
            'name': request.json['name'],
            'email': request.json['email']
        }
        no_sql_handler.update(user_id, updated_data)
        return {'message': 'User updated in NoSQL database'}, 201

    def delete(self, user_id):
        no_sql_handler.delete(user_id)
        return {'message': 'User deleted from NoSQL database'}, 200
    