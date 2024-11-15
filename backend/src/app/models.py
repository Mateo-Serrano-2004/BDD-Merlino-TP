from app import db, mongo_db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

def insert_user_mongo(username, email):
    user = {
        "username": username,
        "email": email
    }
    mongo_db.users.insert_one(user)

def get_users_mongo():
    return mongo_db.users.find()
