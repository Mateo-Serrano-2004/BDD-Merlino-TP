from .__init__ import sql_db, no_sql_db

class SQLUser(sql_db.Model):
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    name = sql_db.Column(sql_db.String(50), nullable=False)
    email = sql_db.Column(sql_db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

class SQLHandler:

    @staticmethod
    def add_user(name, email):
        new_user = SQLUser(name=name, email=email)
        sql_db.session.add(new_user)
        sql_db.session.commit()
        return new_user

    @staticmethod
    def get_all_users():
        return SQLUser.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return SQLUser.query.get(user_id)

    @staticmethod
    def update_user(user_id, name, email):
        user = SQLUser.query.get(user_id)
        if not user:
            return None
        user.name = name
        user.email = email
        sql_db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = SQLUser.query.get(user_id)
        if not user:
            return None
        sql_db.session.delete(user)
        sql_db.session.commit()
        return user

    
class NoSQLHandler:
    def __init__(self):
        self.collection = no_sql_db['users']

    def create(self, user_data):
        self.collection.insert_one(user_data)

    def read_all(self):
        return list(self.collection.find())

    def update(self, user_id, updated_data):
        self.collection.update_one({'_id': user_id}, {'$set': updated_data})

    def delete(self, user_id):
        self.collection.delete_one({'_id': user_id})
