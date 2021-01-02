import config
import users
from api import app, auth, privilege_required
from flask import abort, make_response, jsonify, request, render_template
import requests
import datetime
import re
from pytechecker import check
from bson.objectid import ObjectId

from db import coll_accounts, coll_trans, stringify_ids
from api.routes.economy import get_dates_month_period


get_transactions_to_from_account_sample = {
    "account": {
        "required": True,
        "allowed_types": [int]  # Account ID
    },
    "from_date": {
        "required": False,
        "allowed_types": [int]  # UNIX Timestamp
    },
    "to_date": {
        "required": False,
        "allowed_types": [int]  # UNIX Timestamp
    }
}

@app.route("/econ/transactions/fromaccount", methods=["POST"])
def get_transactions_from_account():
    """
    Returns all transactions that come FROM the specified account, within optional specified dates.

    Expected Payload (example):
    {
        "account": 46,
        "from_date": 160929120, # optional
        "to_date": 1610000120, # optional
    }
    """
    query = request.get_json()
    username = auth.username()
    succ, errors = check(get_transactions_to_from_account_sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    if "from_date" not in query and "to_date" not in query:
        transactions = coll_trans.find({"from_account": query["account"], "user": username}, {"_id": 0})
        return make_response(jsonify(stringify_ids(list(transactions))), 200)
    if "from_date" in query and "to_date" not in query:
        transactions = coll_trans.find({"from_account": query["account"], "user": username, "date_trans": { "$gte": query["from_date"] } }, {"_id": 0})
        return make_response(jsonify(stringify_ids(list(transactions))), 200)
    if "to_date" in query and "from_date" not in query:
        transactions = coll_trans.find({"from_account": query["account"], "user": username, "date_trans": { "$lte": query["to_date"] } }, {"_id": 0})
        return make_response(jsonify(stringify_ids(list(transactions))), 200)
    if "to_date" in query and "from_date" in query:
        transactions = coll_trans.find({"from_account": query["account"], "user": username, "date_trans": { "$lte": query["to_date"], "$gte": query["from_date"] } }, {"_id": 0})
        return make_response(jsonify(stringify_ids(list(transactions))), 200)


@app.route("/econ/transactions/toaccount", methods=["POST"])
def get_transactions_to_account():
    """
    Returns all transactions that go TO the specified account, within optional specified dates.

    Expected Payload (example):
    {
        "account": 21,
        "from_date": 160929120, # optional
        "to_date": 1610000120, # optional
    }
    """
    query = request.get_json()
    username = auth.username()
    succ, errors = check(get_transactions_to_from_account_sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    if "from_date" not in query and "to_date" not in query:
        transactions = coll_trans.find({"to_account": query["account"], "user": username}, {"_id": 0})
        return make_response(jsonify(stringify_ids(list(transactions))), 200)
    if "from_date" in query and "to_date" not in query:
        transactions = coll_trans.find({"to_account": query["account"], "user": username, "date_trans": { "$gte": query["from_date"] } }, {"_id": 0})
        return make_response(jsonify(stringify_ids(list(transactions))), 200)
    if "to_date" in query and "from_date" not in query:
        transactions = coll_trans.find({"to_account": query["account"], "user": username, "date_trans": { "$lte": query["to_date"] } }, {"_id": 0})
        return make_response(jsonify(stringify_ids(list(transactions))), 200)
    if "to_date" in query and "from_date" in query:
        transactions = coll_trans.find({"to_account": query["account"], "user": username, "date_trans": { "$lte": query["to_date"], "$gte": query["from_date"] } }, {"_id": 0})
        return make_response(jsonify(stringify_ids(list(transactions))), 200)


post_transactions_between_dates_sample = {
    "from_date": {
        "required": True,
        "allowed_types": [int]
    },
    "to_date": {
        "required": True,
        "allowed_types": [int]
    }
}

@app.route("/econ/transactions/betweendates", methods=["POST"])
def post_transactions_between_dates():
    query = request.get_json()
    username = auth.username()
    succ, errors = check(post_transactions_between_dates_sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    transactions = coll_trans.find({"user": username, "date_trans": { "$lte": query["to_date"], "$gte": query["from_date"] } })
    transactions = stringify_ids(list(transactions))
    return make_response(jsonify(list(transactions)), 200)

post_create_transaction_sample = {
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

@app.route("/econ/transactions/create", methods=["POST"])
def post_create_transaction():
    query = request.get_json()
    username = auth.username()
    succ, errors = check(post_create_transaction_sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
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


get_transactions_month_period_sample = {
    "date": {
        "required": False,
        "allowed_types": [int]
    }
}

@app.route("/econ/transactions/period", methods=["POST"])
def get_transactions_month_period():
    query = request.get_json()
    username = auth.username()
    succ, errors = check(get_transactions_month_period_sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    if not "date" in query:
        start, end = get_dates_month_period(datetime.datetime.today())
        transactions = coll_trans.find({"user": username, "date_trans": { "$lte": end.timestamp(), "$gte": start.timestamp() } })
        transactions = stringify_ids(list(transactions))
        return make_response(jsonify(transactions), 200)
    else:
        start, end = get_dates_month_period(datetime.datetime.fromtimestamp(query["date"]))
        transactions = coll_trans.find({"user": username, "date_trans": { "$lte": end.timestamp(), "$gte": start.timestamp() } })
        transactions = stringify_ids(list(transactions))
        return make_response(jsonify(transactions), 200)


@app.route("/econ/transactions/delete/<string:_id>", methods=["DELETE"])
def delete_transaction_by_id(_id):
    username = auth.username()
    test = coll_trans.find_one_and_delete({"user": username, "_id": ObjectId(_id) })
    if test:
        del test["_id"]
        return make_response(jsonify(test), 200)
    else:
        return make_response(jsonify(["ERROR: No transaction was found with that ID."]), 400)
    

@app.route("/econ/transactions/<int:year>/<int:month>", methods=["GET"])
def get_get_transactions_in_month_year(year, month):
    username = auth.username()
    date = datetime.datetime(year, month, 1)
    start, end = get_dates_month_period(date)
    transactions = coll_trans.find({"user": username, "date_trans": { "$lte": end.timestamp(), "$gte": start.timestamp() } })
    transactions = stringify_ids(list(transactions))
    return make_response(jsonify(transactions), 200)
        

