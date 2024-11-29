from flask import Flask, request, jsonify
from config import Config
from models import sql_db, User, Role
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object(Config)
sql_db.init_app(app)
mongo = PyMongo(app)

with app.app_context():
    sql_db.create_all()


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"message": "User not found"}), 404


@app.route("/roles/<string:role_name>/users", methods=["GET"])
def create_user(role_name):
    data = request.get_json()
    new_user = User(name=data["name"], email=data["email"], role_name=role_name)
    sql_db.session.add(new_user)
    sql_db.session.commit()
    return jsonify(new_user.to_dict()), 201


@app.route("/users/<int:id>", methods=["PUT"])
def update_user(role_name, id):
    data = request.get_json()
    user = User.query.get(id)
    if user:
        user.name = data["name"]
        user.email = data["email"]
        if not Role.query.get(data["role_name"]):
            return jsonify({"message": "Role not found"}), 404
        user.role_name = role_name
        sql_db.session.commit()
        return jsonify(user.to_dict())
    return jsonify({"message": "User not found"}), 404


@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if user:
        sql_db.session.delete(user)
        sql_db.session.commit()
        return jsonify({"message": "User deleted"})
    return jsonify({"message": "User not found"}), 404


@app.route("/roles", methods=["GET"])
def get_roles():
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles])


@app.route("/roles/<string:name>", methods=["GET"])
def get_role(id):
    role = Role.query.get(id)
    if role:
        return jsonify(role.to_dict())
    return jsonify({"message": "Role not found"}), 404


@app.route("/roles", methods=["POST"])
def create_role():
    data = request.get_json()
    if Role.query.get(data["name"]):
        return jsonify({"message": "Role already exists"}), 400
    new_role = Role(name=data["name"])
    sql_db.session.add(new_role)
    sql_db.session.commit()
    return jsonify(new_role.to_dict()), 201


@app.route("/roles/<string:name>", methods=["PUT"])
def update_role(name):
    data = request.get_json()
    role = Role.query.get(name)
    if role:
        role.name = data["name"]
        sql_db.session.commit()
        return jsonify(role.to_dict())
    return jsonify({"message": "Role not found"}), 404


@app.route("/roles/<string:name>", methods=["DELETE"])
def delete_role(name):
    role = Role.query.get(name)
    if role:
        sql_db.session.delete(role)
        sql_db.session.commit()
        return jsonify({"message": "Role deleted"})
    return jsonify({"message": "Role not found"}), 404


@app.route("/nosql/users", methods=["GET"])
def get_users_nosql():
    users = list(mongo.db.usuarios.find({}, {"_id": 0}))
    return jsonify(users)


@app.route("/nosql/posts/<string:role_name>/users", methods=["POST"])
def create_user_nosql(role_name):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400

    if "name" not in data.keys():
        return jsonify({"error": "Name not provided"}), 400
    if "email" not in data.keys():
        return jsonify({"error": "Email not provided"}), 400

    result = mongo.db.usuarios.insert_one(data)

    return (
        jsonify(
            {"mensaje": "Usuario agregado con exito", "id": str(result.inserted_id)}
        ),
        201,
    )


if __name__ == "__main__":
    app.run(debug=True)
