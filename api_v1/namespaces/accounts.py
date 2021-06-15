from flask_restx import Resource, Namespace
from api_v1 import privilege_required
import requests as req
import config as conf

api = Namespace("accounts", path="/economy/accounts", description="Information about dani's pihole")

@api.route("/")
class AccountsResource(Resource):
    def get(self):
        return { "yas": True }, 200