from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

sql_db = SQLAlchemy(app)

no_sql_db = MongoClient(app.config['MONGO_URI']).get_database()

# creo las tablas sql
with app.app_context():
    sql_db.create_all()

from app import routes
