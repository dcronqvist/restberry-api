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

"""
This endpoint will no matter what, return a new token.
POST { username: "dani", password: "pass" } /v1/users/login -> 200, { token: "abcda-235das-sdf452", created: 124189274 } | 401, ["ERROR: Invalid login credentials."]
"""

@app.route("/v1/users/login", methods=["POST"])
@privilege_required(None)
def v1_users_login():
    sample = {
        "username": {
            "required": True,
            "allowed_types": [str]
        },
        "password": {
            "required": True,
            "allowed_types": [str]
        }
    }
    query = request.get_json()
    succ, errors = check(sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    if users.validate_user(query["username"], query["password"]):
        succ, token = users.create_token_for_user(query["username"])
        return make_response(jsonify(token), 200)
    else:
        return make_response(jsonify(["ERROR: Invalid login credentials."]), 401)

@app.route("/v1/users/checktoken", methods=["POST"])
@privilege_required(None)
def v1_users_checktoken():
    sample = {
        "username": {
            "required": True,
            "allowed_types": [str]
        },
        "token": {
            "required": True,
            "allowed_types": [str]
        }
    }
    query = request.get_json()
    succ, errors = check(sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    succ, tokens = users.validate_token_for_user(query["username"], query["token"])
    if not succ:
        return make_response(jsonify(["ERROR: Invalid token for user."]), 401)
    else:
        return make_response(jsonify(query["token"]), 200)