from flask import request
from flask_restx import Resource, Namespace, fields, reqparse
from api_v1 import privilege_required
import requests as req
import config as conf
from db import coll_accounts
from users import get_username_from_token

api = Namespace("accounts", path="/economy/accounts", description="Information about dani's pihole")

get_requests = reqparse.RequestParser()
get_requests.add_argument("number", type=int, location="args", required=False, action="append")

@api.route("")
class AccountsResource(Resource):

    @api.expect(get_requests, validate=True)
    def get(self):
        args = get_requests.parse_args()
        succ, username = get_username_from_token(request.headers.get("Authorization"))

        if len(args) == 0:
            accs = coll_accounts.find({"user": username }, {"_id": 0}, sort=[("number", 1)])
            return list(accs), 200
        else:
            accs = coll_accounts.find({"user": username, "number": { "$in": args["number"]}}, {"_id": 0}, sort=[("number", 1)])
            return list(accs), 200