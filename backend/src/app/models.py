from .__init__ import sql_db, no_sql_db

class User(sql_db.Model):
    __tablename__ = 'users'
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    name = sql_db.Column(sql_db.String(50), nullable=False)
    email = sql_db.Column(sql_db.String(120), unique=True, nullable=False)
    role_name = sql_db.Column(sql_db.Integer, sql_db.ForeignKey('roles.name'), nullable=False)
    posts = sql_db.relationship('Post', backref='author', lazy=True)

class Role(sql_db.Model):
    __tablename__ = 'roles'
    name = sql_db.Column(sql_db.String(50), primary_key=True)
    description = sql_db.Column(sql_db.String(255), nullable=True)
    users = sql_db.relationship('User', backref='role', lazy=True)

class Post(sql_db.Model):
    __tablename__ = 'posts'
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    title = sql_db.Column(sql_db.String(100), nullable=False)
    content = sql_db.Column(sql_db.Text, nullable=False)
    author_id = sql_db.Column(sql_db.Integer, sql_db.ForeignKey('users.id'), nullable=False)

class SQLHandler:

    @staticmethod
    def add_user(name, email, role_name):
        new_user = User(name=name, email=email, role_name=role_name)
        sql_db.session.add(new_user)
        sql_db.session.commit()
        return new_user

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(id):
        return User.query.get(id)

    @staticmethod
    def update_user(id, name, email):
        user = User.query.get(id)
        if not user:
            return None
        user.name = name
        user.email = email
        sql_db.session.commit()
        return user

    @staticmethod
    def delete_user(id):
        user = User.query.get(id)
        if not user:
            return None
        sql_db.session.delete(user)
        sql_db.session.commit()
        return user
    
    @staticmethod
    def add_role(name, description):
        new_role = Role(name=name, description=description)
        sql_db.session.add(new_role)
        sql_db.session.commit()
        return new_role

    @staticmethod
    def get_all_roles():
        return Role.query.all()
    
    @staticmethod
    def update_role(name, description):
        role = Role.query.get(name)
        if not role:
            return None
        role.description = description
        sql_db.session.commit()
        return role
    
    @staticmethod
    def delete_role(name):
        role = Role.query.get(name)
        if not role:
            return None
        sql_db.session.delete(role)
        sql_db.session.commit()
        return role

    @staticmethod
    def add_post(title, content, author_id):
        new_post = Post(title=title, content=content, author_id=author_id)
        sql_db.session.add(new_post)
        sql_db.session.commit()
        return new_post

    @staticmethod
    def get_all_posts():
        return Post.query.all()
    
    @staticmethod
    def update_post(id, title, content):
        post = Post.query.get(id)
        if not post:
            return None
        post.title = title
        post.content = content
        sql_db.session.commit()
        return post
    
    @staticmethod
    def delete_post(id):
        post = Post.query.get(id)
        if not post:
            return None
        sql_db.session.delete(post)
        sql_db.session.commit()
        return post
    
class NoSQLHandler:
    def __init__(self):
        self.collection = no_sql_db['users']

    def create(self, user_data):
        self.collection.insert_one(user_data)

    def read_all(self):
        return list(self.collection.find())

    def update(self, id, updated_data):
        self.collection.update_one({'_id': id}, {'$set': updated_data})

    def delete(self, id):
        self.collection.delete_one({'_id': id})
