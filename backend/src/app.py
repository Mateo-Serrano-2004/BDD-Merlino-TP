from bson import ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import sqlite_db, User, Role
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4321"}})
app.config.from_object(Config)
sqlite_db.init_app(app)
mongo = PyMongo(app)

with app.app_context():
    sqlite_db.create_all()


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404


@app.route("/roles/<string:role_name>/users", methods=["POST"])
def create_user(role_name):
    data = request.get_json()

    if "name" not in data:
        return jsonify({"message": "Name not provided"}), 400
    if "email" not in data:
        return jsonify({"message": "Email not provided"}), 400
    if not role_name:
        return jsonify({"message": "Role name cannot be blank"}), 400

    role = Role.query.get(role_name)

    if not role:
        return jsonify({"message": "Role name not found"}), 404

    new_user = User(name=data["name"], email=data["email"], role_name=role.name)

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
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404


@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if user:
        sqlite_db.session.delete(user)
        sqlite_db.session.commit()
        mongo.db.posts.delete_many({"user_id": id})
        mongo.db.comments.delete_many({"user_id": id})
        return jsonify(), 204
    return jsonify({"message": "User not found"}), 404


@app.route("/roles", methods=["GET"])
def get_roles():
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles]), 200

@app.route("/roles/<string:name>", methods=["GET"])
def get_role(name):
    role = Role.query.get(name)
    if role:
        return jsonify(role.to_dict())
    return jsonify({"message": "Role not found"}), 404


@app.route("/roles", methods=["POST"])
def create_role():
    data = request.get_json()

    try:
        if Role.query.get(data["name"]):
            return jsonify({"message": "Role already exists"}), 400
        new_role = Role(name=data["name"], description=data["description"])

        sqlite_db.session.add(new_role)
        sqlite_db.session.commit()

        return jsonify(new_role.to_dict()), 201
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400


@app.route("/roles/<string:name>", methods=["PUT"])
def update_role(name):
    data = request.get_json()

    role = Role.query.get(name)
    try:
        if role:
            role.name = data["name"]
            role.description = data["description"]
            sqlite_db.session.commit()
            return jsonify(role.to_dict()), 200
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400

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
        return jsonify(), 204
    return jsonify({"message": "Role not found"}), 404


@app.route("/posts", methods=["GET"])
def get_posts():
    posts = list(mongo.db.posts.find({}))
    for post in posts:
        post["_id"] = str(post["_id"])
    return jsonify(posts), 200


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
    if "user_id" not in data.keys():
        return jsonify({"message": "Incomplete request"}), 400

    if not User.query.get(data["user_id"]):
        return jsonify({"message": "User not found"}), 404

    if "content" not in data.keys():
        return jsonify({"message": "No content provided"}), 400

    content = data["content"]
    if "text" not in content.keys() and "media" not in content.keys():
        return jsonify({"message": "Must provide text or media (or both)"}), 400

    post_data = dict()
    post_data["user_id"] = data["user_id"]
    post_data["content"] = dict()

    if "text" in content.keys() and "media" not in content.keys():
        post_data["content"]["type"] = "T"
        post_data["content"]["text"] = content["text"]
    elif "text" not in content.keys() and "media" in content.keys():
        post_data["content"]["type"] = "M"
        post_data["content"]["media"] = content["media"]
    else:
        post_data["content"]["type"] = "TM"
        post_data["content"]["text"] = content["text"]
        post_data["content"]["media"] = content["media"]

    mongo.db.posts.insert_one(post_data)
    post_data["_id"] = str(post_data["_id"])

    return jsonify(post_data), 201


@app.route("/posts/<string:id>", methods=["PUT"])
def update_post(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400
        if "user_id" in data.keys():
            return jsonify({"message": "User cannot be updated"}), 400

        if "content" not in data.keys():
            return jsonify({"message": "No content provided"}), 400

        content = data["content"]
        if "text" not in content.keys() and "media" not in content.keys():
            return jsonify({"message": "Must provide text or media (or both)"}), 400
        if "type" not in content.keys():
            return jsonify({"message": "No type provided"}), 400

        post_data = dict()
        post_data["content"] = dict()

        if "text" in content.keys() and "media" not in content.keys():
            post_data["content"]["type"] = "T"
            post_data["content"]["text"] = content["text"]
        elif "text" not in content.keys() and "media" in content.keys():
            post_data["content"]["type"] = "M"
            post_data["content"]["media"] = content["media"]
        else:
            post_data["content"]["type"] = "TM"
            post_data["content"]["text"] = content["text"]
            post_data["content"]["media"] = content["media"]

        updated_post = mongo.db.posts.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": post_data}, return_document=True
        )

        if not updated_post:
            return jsonify({"message": "Post not found"}), 404

        updated_post["_id"] = str(updated_post["_id"])

        return jsonify(updated_post), 200
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400


@app.route("/posts/<string:post_id>", methods=["DELETE"])
def delete_post(post_id):
    try:
        result = mongo.db.posts.delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count == 0:
            return jsonify({"message": "Post not found"}), 404
        mongo.db.comments.delete_many({"post_id": post_id})

        return jsonify(), 204
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400


@app.route("/comments", methods=["GET"])
def get_comments():
    comments = list(mongo.db.comments.find({}))

    for comment in comments:
        comment["_id"] = str(comment["_id"])
        comment["user_id"] = str(comment["user_id"])
        comment["post_id"] = str(comment["post_id"])

    return jsonify(comments), 200


@app.route("/comments/<string:comment_id>", methods=["GET"])
def get_comment(comment_id):
    try:
        comment = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            return jsonify({"message": "Comment not found"}), 404
        comment["_id"] = str(comment["_id"])
        return jsonify(comment), 200
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

        if "content" not in data.keys():
            return jsonify({"message": "No content provided"}), 400

        content = data["content"]
        if "text" not in content.keys() and "media" not in content.keys():
            return jsonify({"message": "Must provide text or media (or both)"}), 400

        comment_data = dict()
        comment_data["user_id"] = data["user_id"]
        comment_data["post_id"] = data["post_id"]
        comment_data["content"] = dict()

        if "text" in content.keys() and "media" not in content.keys():
            comment_data["content"]["type"] = "T"
            comment_data["content"]["text"] = content["text"]
        elif "text" not in content.keys() and "media" in content.keys():
            comment_data["content"]["type"] = "M"
            comment_data["content"]["media"] = content["media"]
        else:
            comment_data["content"]["type"] = "TM"
            comment_data["content"]["text"] = content["text"]
            comment_data["content"]["media"] = content["media"]

        mongo.db.comments.insert_one(comment_data)
        comment_data["_id"] = str(comment_data["_id"])

        return jsonify(comment_data), 201
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400


@app.route("/comments/<string:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    try:
        data = request.get_json()

        if "content" not in data.keys():
            return jsonify({"message": "No content provided"}), 400

        content = data["content"]
        if "text" not in content.keys() and "media" not in content.keys():
            return jsonify({"message": "Must provide text or media (or both)"}), 400
        if "type" not in content.keys():
            return jsonify({"message": "Must provide type"}), 400

        comment_data = dict()
        comment_data["content"] = dict()

        if "text" in content.keys() and "media" not in content.keys():
            comment_data["content"]["type"] = "T"
            comment_data["content"]["text"] = content["text"]
        elif "text" not in content.keys() and "media" in content.keys():
            comment_data["content"]["type"] = "M"
            comment_data["content"]["media"] = content["media"]
        else:
            comment_data["content"]["type"] = "TM"
            comment_data["content"]["text"] = content["text"]
            comment_data["content"]["media"] = content["media"]

        updated_comment = mongo.db.comments.find_one_and_update(
            {"_id": ObjectId(comment_id)},
            {"$set": comment_data},
            return_document=True,
        )
        if not updated_comment:
            return jsonify({"message": "Comment not found"}), 404

        updated_comment["_id"] = str(updated_comment["_id"])
        return jsonify(updated_comment), 201
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400


@app.route("/comments/<string:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    try:
        result = mongo.db.comments.delete_one({"_id": ObjectId(comment_id)})
        if result.deleted_count == 0:
            return jsonify({"message": "Comment not found"}), 404
        return jsonify(), 204
    except Exception as e:
        return jsonify({"message": "Error processing request", "error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
