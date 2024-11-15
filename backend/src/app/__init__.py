from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
mongo = PyMongo(app)

from app import routes
