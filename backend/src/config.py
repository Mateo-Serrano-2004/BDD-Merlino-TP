class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sql_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGO_URI = "mongodb://localhost:27017/sql_database"
