import config
import users
from api import app, privilege_required
from flask import abort, make_response, jsonify, request, render_template
import requests
import datetime
import re
from pytechecker import check
from bson.objectid import ObjectId

from db import coll_accounts, coll_trans, stringify_ids
from api.routes.economy import get_dates_month_period

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

@app.route("/v1/economy/transactions", methods=["GET"])
@privilege_required("economy_transactions")
def get_economy_transactions():
    sample_args_1 = {
        "startDate": {
            "required": True,
            "allowed_types": [str]
        },
        "endDate": {
            "required": True,
            "allowed_types": [str]
        },
        "toAccount": {
            "required": False,
            "allowed_types": [str]
        },
        "fromAccount": {
            "required": False,
            "allowed_types": [str]
        },
        "username": {
            "required": True,
            "allowed_types": [str]
        }
    }
    sample_args_2 = {
        "id": {
            "required": True,
            "allowed_types": [list],
            "list_element": {
                "allowed_types": [str]
            }
        },
        "username": {
            "required": True,
            "allowed_types": [list],
            "list_element": {
                "allowed_types": [str]
            }
        }
    }
    args1 = request.args.to_dict(flat=True)
    succ1, errors1 = check(sample_args_1, args1)
    args2 = request.args.to_dict(flat=False)
    succ2, errors2 = check(sample_args_2, args2)
    if not succ1 and not succ2:
        return make_response(jsonify(errors1 + errors2), 400)
    elif succ2 and not succ1:
        username = args2["username"][0]
        l = [x for x in args2["id"] if len(x) == 24]
        transactions = coll_trans.find({"user": username, "_id": { "$in": [ObjectId(i) for i in l]}})
        transactions = stringify_ids(list(transactions))
        return make_response(jsonify(transactions), 200)
    elif succ1 and not succ2:
        username = args1["username"]
        find_query = {
            "user": username,
            "date_trans": {
                "$gte": int(args1["startDate"]),
                "$lte": int(args1["endDate"])
            }
        }

        if "toAccount" in args1:
            find_query["to_account"] = int(args1["toAccount"])
        if "fromAccount" in args1:
            find_query["from_account"] = int(args1["fromAccount"])

        transactions = coll_trans.find(find_query)
        transactions = stringify_ids(list(transactions))
        return make_response(jsonify(transactions), 200)
    elif succ1 and succ2:
        return make_response(jsonify(["ERROR: You may not specify a transaction id if retrieving using dates and accounts."]), 400)


@app.route("/v1/economy/transactions", methods=["POST"])
@privilege_required("economy_transactions")
def post_economy_transactions():
    sample = {
        "amount": {
            "required": True,
            "allowed_types": [float, int]
        },
        "date_trans": {
            "required": False,
            "allowed_types": [int]
        },
        "desc": {
            "required": True,
            "allowed_types": [str]
        },
        "from_account": {
            "required": True,
            "allowed_types": [int]
        },
        "to_account": {
            "required": True,
            "allowed_types": [int]
        }
    }
    sample_args = {
        "username": {
            "required": True,
            "allowed_types": [str]
        }
    }
    query = request.get_json()
    args = request.args.to_dict(flat=True)
    succ1, errors1 = check(sample, query)
    succ2, errors2 = check(sample_args, args)
    if not succ1 or not succ2:
        return make_response(jsonify(erorrs1 + errors2), 400)
    username = args["username"]
    # Check that both accounts exist.
    accs = [query["from_account"], query["to_account"]]
    errors = []
    for acc in accs:
        test = coll_accounts.find_one({"user": username, "number": acc})
        if not test:
            errors.append(f"ERROR: Account with number {acc} does not exist.")
    if len(errors) != 0:
        return make_response(jsonify(errors), 400)
    # Add date_reg and user
    query["date_reg"] = round(datetime.datetime.today().timestamp())
    query["user"] = username
    if "date_trans" not in query:
        query["date_trans"] = query["date_reg"]
    # return new transaction
    coll_trans.insert_one(query)
    query["_id"] = str(query["_id"])
    return make_response(jsonify(query), 200)
    

@app.route("/v1/economy/transactions", methods=["PUT"])
@privilege_required("economy_transactions")
def put_economy_transactions():
    sample_json = {
        "amount": {
            "required": False,
            "allowed_types": [float, int]
        },
        "date_trans": {
            "required": False,
            "allowed_types": [int]
        },
        "desc": {
            "required": False,
            "allowed_types": [str]
        },
        "from_account": {
            "required": False,
            "allowed_types": [int]
        },
        "to_account": {
            "required": False,
            "allowed_types": [int]
        }
    }
    sample_args = {
        "id": {
            "required": True,
            "allowed_types": [str]
        },
        "username": {
            "required": True,
            "allowed_types": [str]
        }
    }
    query = request.get_json()
    args = request.args.to_dict(flat=True)
    succ1, errors1 = check(sample_args, args)
    succ2, errors2 = check(sample_json, query)
    if not succ1 or not succ2:
        return make_response(jsonify(errors1 + errors2), 400)
    username = args["username"]
    filter_query = {
        "user": username,
        "_id": ObjectId(args["id"])
    }
    update_query = { "$set": dict() }
    for key in query:
        update_query["$set"][key] = query[key]
    transaction = coll_trans.update_one(filter_query, update_query)
    return make_response(jsonify(transaction.modified_count), 200)


@app.route("/v1/economy/transactions", methods=["DELETE"])
@privilege_required("economy_transactions")
def delete_economy_transactions():
    sample_args = {
        "id": {
            "required": True,
            "allowed_types": [str]
        },
        "username": {
            "required": True,
            "allowed_types": [str]
        }
    }
    args = request.args.to_dict(flat=True)
    succ, errors = check(sample_args, args)
    if not succ:
        return make_response(jsonify(errors), 400)
    username = args["username"]
    trans = coll_trans.delete_one({"user": username, "_id": ObjectId(args["id"])})
    return make_response(jsonify(trans.deleted_count), 200)