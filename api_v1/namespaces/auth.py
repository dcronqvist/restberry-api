from flask import request
from flask_restx import Resource, Namespace, fields
import users as users
from api_v1 import privilege_required

api = Namespace("auth", description="Authorization operations", security=None)

class User(object):
    def __init__(self, username):
        success, user_object = users.find_user(username)
        if success:
            self.username = user_object["username"]
            self.password = user_object["password"]
            self.privileges = user_object["privileges"]
            self.tokens = user_object["tokens"]
        else:
            self.username = None

    def validate_password(self, password):
        return self.username and users.validate_user(self.username, password)

    def has_privilege(self, privilege):
        return users.has_privilege(self.username, privilege)

    def add_privilege(self, privilege):
        succ, user = users.add_privilege(self.username, privilege)
        if succ:
            self.privileges = user["privileges"]
        return succ

    def remove_privilege(self, privilege):
        succ, user = users.remove_privilege(self.username, privilege)
        if succ:
            self.privileges = user["privileges"]
        return succ

    def validate_token(self, token):
        succ, tokens = users.validate_token_for_user(self.username, token)
        if succ:
            self.tokens = tokens
        return succ

    def create_token(self):
        succ, token = users.create_token_for_user(self.username)
        if succ:
            self.tokens.append(token)
        return succ, token

login = api.model("login", {
    "username": fields.String(required=True, description="The API user's username"),
    "password": fields.String(required=True, description="The API user's password")
})

@api.route("/login")
class LoginResource(Resource):

    @api.response(401, "Invalid username or password")
    @api.response(200, "Successfully logged in, returning token")
    @api.doc(security=None)
    @api.expect(login)
    @privilege_required(None)
    def post(self):
        user = User(api.payload["username"])
        if not user.validate_password(api.payload["password"]):
            return { "error": "Invalid username or password." }, 401
        succ, token = user.create_token()
        return { "success": succ, "token": token }, 200