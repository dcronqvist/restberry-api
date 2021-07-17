from flask import request
from flask_restx import Resource, Namespace, fields, reqparse
from api_v1 import privilege_required
import requests as req
import config as conf
from db import coll_accounts
from api_v1 import user_client

api = Namespace("accounts", path="/economy/accounts", description="Operations regarding economy accounts")

get_requests = reqparse.RequestParser()
get_requests.add_argument("number", type=int, location="args", required=False, action="append")

get_doc = """
### Retrieval of economy accounts

Using this endpoint, you can retrieve information about the different accounts tied to your user. 

Specifying no numbers at all will retrieve all accounts available, while specifying any number of account numbers will retrieve those that match any accounts.

#### Privileges
- economy
- accounts
"""

post_model = api.model("accounts_post", {
    "number": fields.Integer(example=401, required=True),
    "name": fields.String(example="Example account", required=True),
    "desc": fields.String(example="Example account for example transactions", required=True)
})

post_doc = """
### Creation of economy accounts

Using this endpoint, you can create new economy accounts for your user.

#### Privileges
- economy
- accounts
"""

@api.route("")
class AccountsResource(Resource):

    @api.doc(description=get_doc)
    @api.expect(get_requests, validate=True)
    @privilege_required("accounts")
    @privilege_required("economy")
    def get(self):
        args = get_requests.parse_args()
        succ, username = user_client.get_username_from_token(request.headers.get("Authorization"))

        if not args["number"]:
            accs = coll_accounts.find({"user": username }, {"_id": 0}, sort=[("number", 1)])
            return list(accs), 200
        else:
            accs = coll_accounts.find({"user": username, "number": { "$in": args["number"]}}, {"_id": 0}, sort=[("number", 1)])
            return list(accs), 200

    @api.doc(description=post_doc)
    @api.response(400, "The specified account number already exists")
    @api.response(200, "Successfully created new account")
    @api.expect(post_model, validate=True)
    @privilege_required("accounts")
    @privilege_required("economy")
    def post(self):
        payload = api.payload
        succ, username = user_client.get_username_from_token(request.headers.get("Authorization"))
        test = coll_accounts.find_one({"number": payload["number"]}, {"_id": 0})

        if test:
            return { "error": f"Account number {payload['number']} already exists."}, 400
        else:
            insert = coll_accounts.insert_one(payload, {"_id": 0})
            del payload["_id"]
            return payload, 200
