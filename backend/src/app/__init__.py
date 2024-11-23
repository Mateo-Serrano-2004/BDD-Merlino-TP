from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

sql_db = SQLAlchemy(app)

no_sql_db = MongoClient(app.config["MONGO_URI"]).get_database()

api = Api(
    app,
    version="1.0",
    title="Mi API",
    description="Una API de ejemplo que interactúa con bases de datos SQL y NoSQL",
)

with app.app_context():
    sql_db.create_all()
