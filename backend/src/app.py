from bson import ObjectId
from flask import Flask, request, jsonify
from config import Config
from models import sqlite_db, User, Role
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object(Config)
sqlite_db.init_app(app)
mongo = PyMongo(app)

with app.app_context():
    sqlite_db.create_all()


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
    sqlite_db.session.add(new_user)
    sqlite_db.session.commit()
    return jsonify(new_user.to_dict()), 201


@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if user:
        user.name = data["name"]
        user.email = data["email"]
        if not Role.query.get(data["role_name"]):
            return jsonify({"message": "Role not found"}), 404
        user.role_name = data["role_name"]
        sqlite_db.session.commit()
        return jsonify(user.to_dict())
    return jsonify({"message": "User not found"}), 404


@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if user:
        sqlite_db.session.delete(user)
        sqlite_db.session.commit()
        posts = mongo.db.posts.delete_many({"user_id": id})
        for post in posts:
            mongo.db.comments.delete_many({"post_id": post["_id"]})
        mongo.db.comments.delete_many({"user_id": id})
        return 204
    return jsonify({"message": "User not found"}), 404


@app.route("/roles", methods=["GET"])
def get_roles():
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles])

@app.route("/roles/<string:name>", methods=["GET"])
def get_role(name):
    role = Role.query.get(name)
    if role:
        return jsonify(role.to_dict())
    return jsonify({"message": "Role not found"}), 404


@app.route("/roles", methods=["POST"])
def create_role():
    data = request.get_json()
    if Role.query.get(data["name"]):
        return jsonify({"message": "Role already exists"}), 400
    new_role = Role(name=data["name"])
    sqlite_db.session.add(new_role)
    sqlite_db.session.commit()
    return jsonify(new_role.to_dict()), 201


@app.route("/roles/<string:name>", methods=["PUT"])
def update_role(name):
    data = request.get_json()
    role = Role.query.get(name)
    if role:
        role.name = data["name"]
        sqlite_db.session.commit()
        return jsonify(role.to_dict())
    return jsonify({"message": "Role not found"}), 404


@app.route("/roles/<string:name>", methods=["DELETE"])
def delete_role(name):
    role = Role.query.get(name)
    if role:
        users = User.query.filter_by(role_name=name).all()
        for user in users:
            delete_user(user.id)
        sqlite_db.session.delete(role)
        sqlite_db.session.commit()
        return 204
    return jsonify({"message": "Role not found"}), 404


@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify(list(mongo.db.posts.find({})))


@app.route("/posts/<string:id>", methods=["GET"])
def get_post(id):
    try:
        post = mongo.db.posts.find_one({"_id": ObjectId(id)})
        if not post:
            return jsonify({"message": "Post not found"}), 404
        post["_id"] = str(post["_id"])
        return jsonify(post)
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400


@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    if not User.query.get(data["user_id"]):
        return jsonify({"message": "User not found"}), 404
    result = mongo.db.posts.insert_one(data)
    result["_id"] = str(result["_id"])
    return jsonify(result), 201


@app.route("/posts/<string:id>", methods=["PUT"])
def update_post(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400
        if data["user_id"]:
            return jsonify({"message": "User cannot be updated"}), 400
        updated_post = mongo.db.posts.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": data}, return_document=True
        )
        if not updated_post:
            return jsonify({"message": "Post not found"}), 404
        updated_post["_id"] = str(updated_post["_id"])
        return jsonify(updated_post)
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400


@app.route("/posts/<string:post_id>", methods=["DELETE"])
def delete_post(post_id):
    try:
        result = mongo.db.posts.delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count == 0:
            return jsonify({"message": "Post not found"}), 404
        mongo.db.comments.delete_many({"post_id": post_id})
        return 204
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400


@app.route("/comments", methods=["GET"])
def get_comments():
    return jsonify(list(mongo.db.comments.find({})))

@app.route("/comments/<string:comment_id>", methods=["GET"])
def get_comment(comment_id):
    try:
        comment = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            return jsonify({"message": "Comment not found"}), 404
        comment["_id"] = str(comment["_id"])
        return jsonify(comment)
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400

@app.route("/comments", methods=["POST"])
def create_comment():
    try:
        data = request.get_json()
        if not User.query.get(data["user_id"]):
            return jsonify({"message": "User not found"}), 404
        if not mongo.db.posts.find_one({"_id": ObjectId(data["post_id"])}):
            return jsonify({"message": "Post not found"}), 404
        result = mongo.db.comments.insert_one(data)
        result["_id"] = str(result["_id"])
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400


@app.route("/comments/<string:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    try:
        data = request.get_json()
        updated_comment = mongo.db.comments.find_one_and_update(
            {"_id": ObjectId(comment_id)},
            {"$set": data},
            return_document=True,
        )
        if not updated_comment:
            return jsonify({"message": "Comment not found"}), 404
        updated_comment["_id"] = str(updated_comment.inserted_id)
        return jsonify(updated_comment)
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400


@app.route("/comments/<string:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    try:
        result = mongo.db.comments.delete_one({"_id": ObjectId(comment_id)})
        if result.deleted_count == 0:
            return jsonify({"message": "Comment not found"}), 404
        return 204
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400
    

if __name__ == "__main__":
    app.run(debug=True)
