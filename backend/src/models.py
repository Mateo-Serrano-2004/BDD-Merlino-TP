from flask_sqlalchemy import SQLAlchemy

sql_db = SQLAlchemy()


class User(sql_db.Model):
    __tablename__ = "users"
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    name = sql_db.Column(sql_db.String(80), nullable=False)
    email = sql_db.Column(sql_db.String(120), unique=True, nullable=False)
    role_name = sql_db.Column(
        sql_db.String(50), sql_db.ForeignKey("roles.name"), nullable=False
    )
    role = sql_db.relationship("Role", backref=sql_db.backref("users", lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role_name": self.role_name,
            "role": self.role.to_dict(),
        }


class Role(sql_db.Model):
    __tablename__ = "roles"
    name = sql_db.Column(sql_db.String(50), primary_key=True)
    description = sql_db.Column(sql_db.Text, nullable=False)

    def to_dict(self):
        return {"name": self.name, "description": self.description}


class Post(sql_db.Model):
    __tablename__ = "posts"
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    title = sql_db.Column(sql_db.String(100), nullable=False)
    content = sql_db.Column(sql_db.Text, nullable=False)
    user_id = sql_db.Column(
        sql_db.Integer, sql_db.ForeignKey("users.id"), nullable=False
    )
    user = sql_db.relationship("User", backref=sql_db.backref("posts", lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "user": self.user.to_dict(),
        }
