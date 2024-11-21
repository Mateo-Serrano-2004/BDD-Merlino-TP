from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields
from app import app
from app.models import SQLHandler, NoSQLHandler

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_bp)

sql_handler = SQLHandler()
no_sql_handler = NoSQLHandler()

# Modelo para la documentación Swagger
user_model = api.model('User', {
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email address')
})

@api.route('/add_sql')
class AddSQL(Resource):
    @api.doc('add_sql')
    @api.expect(user_model)
    def post(self):
        """Add a new user to the SQL database"""
        name = request.json['name']
        email = request.json['email']
        sql_handler.add_user(name, email)
        return jsonify({'message': 'SQLUser added to SQL'}), 201

@api.route('/get_sql')
class GetSQL(Resource):
    @api.doc('get_sql')
    def get(self):
        """Get all users from the SQL database"""
        users = sql_handler.get_all_users()
        users_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
        return jsonify(users_data), 200

@api.route('/update_sql/<int:id>')
class UpdateSQL(Resource):
    @api.doc('update_sql')
    @api.expect(user_model)
    def put(self, id):
        """Update user information in the SQL database"""
        name = request.json['name']
        email = request.json['email']
        sql_handler.update_user(id, name, email)
        return jsonify({'message': 'SQLUser updated in SQL'}), 201

@api.route('/delete_sql/<int:id>')
class DeleteSQL(Resource):
    @api.doc('delete_sql')
    def delete(self, id):
        """Delete a user from the SQL database"""
        sql_handler.delete_user(id)
        return jsonify({'message': 'SQLUser deleted from SQL'}), 200

@api.route('/add_no_sql')
class AddNoSQL(Resource):
    @api.doc('add_no_sql')
    @api.expect(user_model)
    def post(self):
        """Add a new user to the NoSQL database"""
        name = request.json['name']
        email = request.json['email']
        new_user = {'name': name, 'email': email}
        no_sql_handler.create(new_user)
        return jsonify({'message': 'SQLUser added to Mongosql_db'}), 201

@api.route('/get_no_sql')
class GetNoSQL(Resource):
    @api.doc('get_no_sql')
    def get(self):
        """Get all users from the NoSQL database"""
        users = no_sql_handler.read_all()
        users_data = [{'id': str(user['_id']), 'name': user['name'], 'email': user['email']} for user in users]
        return jsonify(users_data), 200

@api.route('/update_no_sql/<user_id>')
class UpdateNoSQL(Resource):
    @api.doc('update_no_sql')
    @api.expect(user_model)
    def put(self, user_id):
        """Update user information in the NoSQL database"""
        updated_data = {
            'name': request.json['name'],
            'email': request.json['email']
        }
        no_sql_handler.update(user_id, updated_data)
        return jsonify({'message': 'SQLUser updated in Mongosql_db'}), 201

@api.route('/delete_no_sql/<user_id>')
class DeleteNoSQL(Resource):
    @api.doc('delete_no_sql')
    def delete(self, user_id):
        """Delete a user from the NoSQL database"""
        no_sql_handler.delete(user_id)
        return jsonify({'message': 'SQLUser deleted from Mongosql_db'}), 200

app.register_blueprint(api_bp)
