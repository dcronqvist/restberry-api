import config
import users
from api import app, auth, privilege_required
from flask import abort, make_response, jsonify, request, render_template
import requests
import datetime
import re
from pytechecker import check

from db import coll_accounts, coll_trans

@app.route("/econ/accounts/all", methods=["GET"])
def get_all_accounts():
    username = auth.username()
    accs = coll_accounts.find({"user": username }, {"_id": 0})
    return make_response(jsonify(list(accs)), 200)

post_search_accounts_sample = {
    "search": {
        "required": True,
        "allowed_types": [str]
    }
}

@app.route("/econ/accounts/search", methods=["POST"])
def post_search_accounts():
    query = request.get_json()
    username = auth.username()
    succ, errors = check(post_search_accounts_sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    accounts = coll_accounts.find({ "name": { "$regex": query["search"], "$options": "i" }, "user": username}, {"_id": 0})
    return make_response(jsonify(list(accounts)), 200)


@app.route("/econ/accounts/id/<int:_id>", methods=["GET"])
def get_account_by_id(_id):
    username = auth.username()
    acc = coll_accounts.find_one({"number": _id, "user": username}, {"_id": 0})
    if acc:
        return make_response(jsonify(acc), 200)
    else:
        return make_response(jsonify(None), 404)

post_new_account_sample = {
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

@app.route("/econ/accounts/create", methods=["POST"])
def post_new_account():
    username = auth.username()
    query = request.get_json()
    succ, errors = check(post_new_account_sample, query)
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
    

