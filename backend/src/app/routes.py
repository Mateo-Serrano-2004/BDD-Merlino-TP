from flask import request
from flask_restx import Resource
from .__init__ import api
from .models import SQLHandler, NoSQLHandler

sql_handler = SQLHandler()
no_sql_handler = NoSQLHandler()


@api.route("/sql/users")
class UsersSQL(Resource):
    def get(self):
        return sql_handler.get_all_users(), 200


@api.route("/sql/roles/<string:role_name>/users")
class UserWithRoleSQL(Resource):
    def post(self, role_name):
        if not sql_handler.add_user(
            request.json["name"], request.json["email"], role_name 
        ):
            return {"message": "Role does not exist"}, 404
        return {"message": "User added to SQL database"}, 201


@api.route("/sql/users/<int:id>")
class UserSQL(Resource):
    def put(self, id):
        if not sql_handler.update_user(id, request.json["name"], request.json["email"]):
            return {"message": "User does not exist"}, 404
        return {"message": "User updated in SQL database"}, 200

    def delete(self, id):
        if not sql_handler.delete_user(id):
            return {"message": "User does not exist"}, 404
        return {"message": "User deleted from SQL database"}, 200


@api.route("/sql/roles")
class RolesSQL(Resource):
    def get(self):
        return sql_handler.get_all_roles(), 200

    def post(self):
        sql_handler.add_role(request.json["name"], request.json["description"])
        return {"message": "Role added to SQL database"}, 201


@api.route("/sql/roles/<string:name>")
class RoleSQL(Resource):
    def put(self, name):
        if not sql_handler.update_role(name, request.json["description"]):
            return {"message": "Role does not exist"}, 404
        return {"message": "Role updated in SQL database"}, 200

    def delete(self, name):
        if not sql_handler.delete_role(name):
            return {"message": "Role does not exist"}, 404
        return {"message": "Role deleted from SQL database"}, 200


@api.route("/sql/posts")
class PostsSQL(Resource):
    def get(self):
        return sql_handler.get_all_posts(), 200


@api.route("/sql/users/<int:user_id>/posts")
class PostWithUserSQL(Resource):
    def post(self, user_id):
        if not sql_handler.add_post(
            request.json["title"], request.json["content"], user_id
        ):
            return {"message": "User does not exist"}, 404
        return {"message": "Post added to SQL database"}, 201


@api.route("/sql/posts/<int:id>")
class PostSQL(Resource):
    def put(self, id):
        if not sql_handler.update_post(
            id, request.json["title"], request.json["content"]
        ):
            return {"message": "Post does not exist"}, 404
        return {"message": "Post updated in SQL database"}, 200

    def delete(self, id):
        if not sql_handler.delete_post(id):
            return {"message": "Post does not exist"}, 404
        return {"message": "Post deleted from SQL database"}, 200


@api.route("/no_sql/users")
class UsersNoSQL(Resource):
    def get(self):
        return no_sql_handler.read_all(), 200

    def post(self):
        new_user = {"name": request.json["name"], "email": request.json["email"]}
        no_sql_handler.create(new_user)
        return {"message": "User added to NoSQL database"}, 201


@api.route("/no_sql/users/<int:id>")
class UserNoSQL(Resource):
    def put(self, id):
        updated_data = {"name": request.json["name"], "email": request.json["email"]}
        no_sql_handler.update(id, updated_data)
        return {"message": "User updated in NoSQL database"}, 201

    def delete(self, id):
        no_sql_handler.delete(id)
        return {"message": "User deleted from NoSQL database"}, 200
