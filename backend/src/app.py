from flask import Flask, request, jsonify
from config import Config
from models import sql_db, User, Role, Post

app = Flask(__name__)
app.config.from_object(Config) 
sql_db.init_app(app)

with app.app_context():
    sql_db.create_all()


@app.route("/sql/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@app.route("/sql/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"message": "User not found"}), 404


@app.route("/sql/posts/<string:role_name>/users", methods=["GET"])
def create_user(role_name):
    data = request.get_json()
    new_user = User(name=data["name"], email=data["email"], role_name=role_name)
    sql_db.session.add(new_user)
    sql_db.session.commit()
    return jsonify(new_user.to_dict()), 201


@app.route("/sql/users/<int:id>", methods=["PUT"])
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


@app.route("/sql/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if user:
        sql_db.session.delete(user)
        sql_db.session.commit()
        return jsonify({"message": "User deleted"})
    return jsonify({"message": "User not found"}), 404


@app.route("/sql/roles", methods=["GET"])
def get_roles():
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles])


@app.route("/sql/roles/<int:id>", methods=["GET"])
def get_role(id):
    role = Role.query.get(id)
    if role:
        return jsonify(role.to_dict())
    return jsonify({"message": "Role not found"}), 404


@app.route("/sql/roles", methods=["POST"])
def create_role():
    data = request.get_json()
    new_role = Role(name=data["name"])
    sql_db.session.add(new_role)
    sql_db.session.commit()
    return jsonify(new_role.to_dict()), 201


@app.route("/sql/roles/<int:id>", methods=["PUT"])
def update_role(id):
    data = request.get_json()
    role = Role.query.get(id)
    if role:
        role.name = data["name"]
        sql_db.session.commit()
        return jsonify(role.to_dict())
    return jsonify({"message": "Role not found"}), 404


@app.route("/sql/roles/<int:id>", methods=["DELETE"])
def delete_role(id):
    role = Role.query.get(id)
    if role:
        sql_db.session.delete(role)
        sql_db.session.commit()
        return jsonify({"message": "Role deleted"})
    return jsonify({"message": "Role not found"}), 404


@app.route("/sql/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])


@app.route("/sql/posts/<int:id>", methods=["GET"])
def get_post(id):
    post = Post.query.get(id)
    if post:
        return jsonify(post.to_dict())
    return jsonify({"message": "Post not found"}), 404


@app.route("/sql/users/<int:user_id>/posts", methods=["POST"])
def create_post(user_id):
    data = request.get_json()
    if not User.query.get(user_id):
        return jsonify({"message": "User not found"}), 404
    new_post = Post(title=data["title"], content=data["content"], user_id=user_id)
    sql_db.session.add(new_post)
    sql_db.session.commit()
    return jsonify(new_post.to_dict()), 201


@app.route("/sql/posts/<int:id>", methods=["PUT"])
def update_post(id):
    data = request.get_json()
    post = Post.query.get(id)
    if post:
        post.title = data["title"]
        post.content = data["content"]
        if not User.query.get(data["user_id"]):
            return jsonify({"message": "User not found"}), 404
        post.user_id = data["user_id"]
        sql_db.session.commit()
        return jsonify(post.to_dict())
    return jsonify({"message": "Post not found"}), 404


@app.route("/sql/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = Post.query.get(id)
    if post:
        sql_db.session.delete(post)
        sql_db.session.commit()
        return jsonify({"message": "Post deleted"})
    return jsonify({"message": "Post not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
