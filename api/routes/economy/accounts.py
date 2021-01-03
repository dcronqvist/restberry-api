import config
import users
from api import app, auth, privilege_required
from flask import abort, make_response, jsonify, request, render_template
import requests
import datetime
import re
from pytechecker import check
from db import coll_accounts, coll_trans


# You can specify zero number params in the query string, and you'll retrieve all your accounts.
# If you, however, specify one or more numbers, like this ?number=599&number=244, you'll get all the ones you specified.
# You will always get an array of accounts, even if you only specify one number.
# curl "user:pass@127.0.0.1:5000/v1/economy/accounts?number=599"
@app.route("/v1/economy/accounts", methods=["GET"])
@privilege_required("economy")
def get_economy_accounts():
    sample = {
        "number": {
            "required": False,
            "allowed_types": [list],
            "list_element": {
                "allowed_types": [str]
            }
        }
    }
    username = auth.username()
    query = request.args.to_dict(flat=False)
    succ, errors = check(sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    if "number" in query:
        accs = coll_accounts.find({"user": username, "number": { "$in": [int(i) for i in query["number"]] }}, {"_id": 0})
        return make_response(jsonify(list(accs)), 200)
    else:
        accs = coll_accounts.find({"user": username}, {"_id": 0})
        return make_response(jsonify(list(accs)), 200)


# Expects nothing in the query string.
# Returns the new account, after creating it.
# curl -X POST -H "Content-Type: application/json" -d '{ "number": 599, "name": "Testing account", "desc": "Account used for testing purposes." }' "user:pass@127.0.0.1:5000/v1/economy/accounts"
@app.route("/v1/economy/accounts", methods=["POST"])
@privilege_required("economy")
def post_economy_accounts():
    sample = {
        "number": {
            "required": True,
            "allowed_types": [int]
        },
        "name": {
            "required": True,
            "allowed_types": [str]
        },
        "desc": {
            "required": True,
            "allowed_types": [str]
        }
    }
    username = auth.username()
    query = request.get_json()
    succ, errors = check(sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    query["user"] = username
    test = coll_accounts.find_one({"number": query["number"]}, {"_id": 0})
    if test:
        return make_response(jsonify(["ERROR: Account number already exists."]), 400)
    else:
        insert = coll_accounts.insert_one(query, {"_id": 0})
        del query["_id"]
        return make_response(jsonify(query), 200)


# Expects only one number=x in the query string.
# Returns the new account, after updating it.
# curl -X PUT -H "Content-Type: application/json" -d '{ "number": 599, "name": "Testing account", "desc": "Account used for testing purposes." }' "user:pass@127.0.0.1:5000/v1/economy/accounts?number=599"
@app.route("/v1/economy/accounts", methods=["PUT"])
@privilege_required("economy")
def put_economy_accounts():
    sample_json = {
        "number": {
            "required": True,
            "allowed_types": [int]
        },
        "name": {
            "required": True,
            "allowed_types": [str]
        },
        "desc": {
            "required": True,
            "allowed_types": [str]
        }
    }
    sample_args = {
        "number": {
            "required": True,
            "allowed_types": [str]
        }
    }
    args = request.args.to_dict(flat=True)
    query = request.get_json()
    username = auth.username()
    # Check args
    succ, errors = check(sample_args, args)
    if not succ:
        return make_response(jsonify(errors), 400)
    # Check query
    succ, errors = check(sample_json, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    num = 0
    try:
        num = int(args["number"])
    except:
        return make_response(jsonify(["ERROR: Required parameter 'number' was not an integer."]), 400)
    # check if account exists.
    test = coll_accounts.find_one({"user": username, "number": num})
    if not test:
        return make_response(jsonify("ERROR: No such account exists."), 404)
    query["user"] = username
    coll_accounts.replace_one({"user": username, "number": num}, query)
    return make_response(jsonify(query), 200)


# Expects at least one num=x in the query string, you can specify multiple.
# Returns the amount of accounts that were deleted.    
# curl -X DELETE "user:pass@127.0.0.1:5000/v1/economy/accounts?number=599"
@app.route("/v1/economy/accounts", methods=["DELETE"])
@privilege_required("economy")
def delete_economy_accounts():
    sample = {
        "number": {
            "required": True,
            "allowed_types": [list],
            "list_element": {
                "allowed_types": [str]
            }
        }
    }
    args = request.args.to_dict(flat=False)
    username = auth.username()
    succ, errors = check(sample, args)
    if not succ:
        return make_response(jsonify(errors), 400)
    x = coll_accounts.delete_many({"number": { "$in": [int(i) for i in args["number"]] }, "user": username})
    return make_response(jsonify(x.deleted_count), 200)
