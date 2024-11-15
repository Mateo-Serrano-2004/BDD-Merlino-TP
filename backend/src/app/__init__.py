from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from .routes import create_user_sql, get_users_sql, delete_user_sql, update_user_sql
from .routes import create_user_nosql, get_users_nosql, delete_user_nosql, update_user_nosql

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sql_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MONGO_URI'] = 'mongodb://localhost:27017/nosql_database'

    db.init_app(app)

    mongo_client = MongoClient(app.config['MONGO_URI'])
    app.mongo_db = mongo_client.get_database()

    with app.app_context():
        from . import routes

    return app

def register_routes(app):
    app.add_url_rule('/sql/users', 'create_user_sql', create_user_sql, methods=['POST'])
    app.add_url_rule('/sql/users', 'get_users_sql', get_users_sql, methods=['GET'])
    app.add_url_rule('/sql/users/<int:user_id>', 'delete_user_sql', delete_user_sql, methods=['DELETE'])
    app.add_url_rule('/sql/users/<int:user_id>', 'update_user_sql', update_user_sql, methods=['PUT'])

    app.add_url_rule('/nosql/users', 'create_user_nosql', create_user_nosql, methods=['POST'])
    app.add_url_rule('/nosql/users', 'get_users_nosql', get_users_nosql, methods=['GET'])
    app.add_url_rule('/nosql/users/<string:user_id>', 'delete_user_nosql', delete_user_nosql, methods=['DELETE'])
    app.add_url_rule('/nosql/users/<string:user_id>', 'update_user_nosql', update_user_nosql, methods=['PUT'])
