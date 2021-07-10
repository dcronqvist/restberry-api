from datetime import datetime
from bson.objectid import ObjectId
from flask import request
from flask_restx import Resource, Namespace, fields, reqparse
from api_v1 import privilege_required
import requests as req
import config as conf
from db import coll_trans, stringify_ids, coll_accounts
from users import get_username_from_token

"""
DONE
GET /v1/economy/transactions?startDate=1023..&endDate=1415..
GET /v1/economy/transactions?id=908da84j2n76uc7sh4&id=74h289f923kv8n4d90j7g
GET /v1/economy/transactions?toAccount=401&startDate=1023..&endDate=1415..
GET /v1/economy/transactions?fromAccount=101&startDate=1023..&endDate=1415..
GET /v1/economy/transactions?toAccount=401&fromAccount=101&startDate=1023..&endDate=1415..
POST /v1/economy/transactions
PUT /v1/economy/transactions?id=908da84j2n76uc7sh4
DELETE /v1/economy/transactions?id=908da84j2n76uc7sh4
"""

api = Namespace("transactions", path="/economy/transactions", description="Operations regarding economy transactions")

between_dates = reqparse.RequestParser()
between_dates.add_argument("startDate", type=int, required=True, location="args")
between_dates.add_argument("endDate", type=int, required=True, location="args")
between_dates.add_argument("fromAccount", type=int, required=False, location="args")
between_dates.add_argument("toAccount", type=int, required=False, location="args")


get_doc = """
### Retrieval of economy accounts

Using this endpoint, you can retrieve information about the different accounts tied to your user. 

Specifying no numbers at all will retrieve all accounts available, while specifying any number of account numbers will retrieve those that match any accounts.

#### Privileges
- economy
- accounts
"""

post_model = api.model("post_transaction", {
    "amount": fields.Float(example=39.9, required=True),
    "date_trans": fields.Integer(example=round(datetime.now().timestamp()), required=False),
    "desc": fields.String(example="Transaction for stuff", required=True),
    "from_account": fields.Integer(example=101, required=True),
    "to_account": fields.Integer(example=401, required=True)            
})


@api.route("")
class TransactionByDateResource(Resource):

    @api.response(200, "Successfully retrieved transactions")
    @api.doc(description=get_doc)
    @api.expect(between_dates, validate=True)
    @privilege_required("transactions")
    @privilege_required("economy")
    def get(self):
        args = between_dates.parse_args()
        succ, username = get_username_from_token(request.headers.get("Authorization"))
        find_query = {
            "user": username,
            "date_trans": {
                "$gte": int(args["startDate"]),
                "$lte": int(args["endDate"])
            }
        }

        if args["toAccount"]:
            find_query["to_account"] = int(args["toAccount"])
        if args["fromAccount"]:
            find_query["from_account"] = int(args["fromAccount"])

        transactions = coll_trans.find(find_query)
        transactions = stringify_ids(list(transactions))
        return transactions, 200

    @api.expect(post_model, validate=True)
    @privilege_required("accounts")
    @privilege_required("economy")
    def post(self):
        accounts = [api.payload["from_account"], api.payload["to_account"]]
        succ, username = get_username_from_token(request.headers.get("Authorization"))
        errors = []
        for acc in accounts:
            test = coll_accounts.find_one({ "user": username, "number": acc})
            if not test:
                errors.append(f"Could not find an account with number {acc} associated with your user.")
        if len(errors) > 0:
            return { "errors": errors }, 400

        api.payload["date_reg"] = round(datetime.now().timestamp())
        api.payload["user"] = username
        api.payload["date_trans"] = api.payload.get("date_trans", api.payload["date_reg"])
        coll_trans.insert_one(api.payload)
        api.payload["_id"] = str(api.payload["_id"])
        return api.payload, 200

by_id = reqparse.RequestParser()
by_id.add_argument("id", type=str, required=True, location="args")

@api.route("/id")
class TransactionByIDResource(Resource):

    @api.expect(by_id)
    @privilege_required("transactions")
    @privilege_required("economy")
    def get(self):
        args = by_id.parse_args()
        succ, username = get_username_from_token(request.headers.get("Authorization"))

        transaction = coll_trans.find({"user": username, "_id": ObjectId(args["id"])})
        transaction = stringify_ids(list(transaction))
        return transaction[0], 200
