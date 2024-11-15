from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from ..config import Config

db = SQLAlchemy()
client = MongoClient("mongodb://localhost:27017")
mongo_db = client["mydatabase"]

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
