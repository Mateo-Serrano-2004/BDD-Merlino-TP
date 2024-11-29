from flask_sqlalchemy import SQLAlchemy

sqlite_db = SQLAlchemy()


class User(sqlite_db.Model):
    __tablename__ = "users"
    id = sqlite_db.Column(sqlite_db.Integer, primary_key=True)
    name = sqlite_db.Column(sqlite_db.String(80), nullable=False)
    email = sqlite_db.Column(sqlite_db.String(120), unique=True, nullable=False)
    role_name = sqlite_db.Column(
        sqlite_db.String(50), sqlite_db.ForeignKey("roles.name"), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role_name": self.role_name,
        }


class Role(sqlite_db.Model):
    __tablename__ = "roles"
    name = sqlite_db.Column(sqlite_db.String(50), primary_key=True)
    description = sqlite_db.Column(sqlite_db.Text, nullable=False)

    users = sqlite_db.relationship("User", backref="role", lazy=True)

    def to_dict(self):
        return {"name": self.name, "description": self.description}
