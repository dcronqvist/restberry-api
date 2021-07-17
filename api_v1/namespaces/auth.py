from flask import request
from flask_restx import Resource, Namespace, fields
from models.users.users import user_client
from api_v1 import privilege_required

api = Namespace("auth", description="Authorization operations", security=None)

class User(object):
    def __init__(self, username):
        success, user_object = user_client.find_user(username)
        if success:
            self.username = user_object["username"]
            self.password = user_object["password"]
            self.privileges = user_object["privileges"]
            self.tokens = user_object["tokens"]
        else:
            self.username = None

    def validate_password(self, password):
        return self.username and user_client.validate_user(self.username, password)

    def has_privilege(self, privilege):
        return user_client.has_privilege(self.username, privilege)

    def add_privilege(self, privilege):
        succ, user = user_client.add_privilege(self.username, privilege)
        if succ:
            self.privileges = user["privileges"]
        return succ

    def remove_privilege(self, privilege):
        succ, user = user_client.remove_privilege(self.username, privilege)
        if succ:
            self.privileges = user["privileges"]
        return succ

    def validate_token(self, token):
        succ, tokens = user_client.validate_token_for_user(self.username, token)
        if succ:
            self.tokens = tokens
        return succ

    def create_token(self):
        succ, token = user_client.create_token_for_user(self.username)
        if succ:
            self.tokens.append(token)
        return succ, token

login = api.model("login", {
    "username": fields.String(required=True, description="The API user's username"),
    "password": fields.String(required=True, description="The API user's password")
})

post_doc = """
### Attempts login using specified credentials

Using this endpoint, you can attempt to login and retrieve a token which will be valid for 60 minutes upon retrieval. This token must be supplied in **ALL** future requests as the value in an `Authorization` header to all other API endpoints.

In order to use some (in fact most) endpoints, you as a user must have specific privileges. These privileges will be documented under each endpoint, to show which are needed, like this:

#### Privileges
- no_privilege
- super_power
- doge

This login endpoint is the one exception of requiring no `Authorization` header, as it provides the means to aquire the token needed for the header.
"""

@api.route("/login")
class LoginResource(Resource):

    @api.response(401, "Invalid username or password")
    @api.response(200, "Successfully logged in, returning token")
    @api.doc(security=None, description=post_doc)
    @api.expect(login)
    @privilege_required(None)
    def post(self):
        user = User(api.payload["username"])
        if not user.validate_password(api.payload["password"]):
            return { "error": "Invalid username or password." }, 401
        succ, token = user.create_token()
        return { "success": succ, "token": token }, 200