import config
import users
from api import app, auth, privilege_required
from flask import abort, make_response, jsonify, request, render_template
import requests
import datetime
import re
from pytechecker import check
from api.routes.economy import get_dates_month_period

@app.route("/econ/periods/currentmonth", methods=["GET"])
def get_periods_currentmonth():
    start, end = get_dates_month_period(datetime.datetime.today())
    result = {
        "start": start.timestamp(),
        "end": end.timestamp()
    }
    return make_response(jsonify(result), 200)

post_periods_date_sample = {
    "date": {
        "required": True,
        "allowed_types": [int]
    }
}

@app.route("/econ/periods/date", methods=["POST"])
def post_periods_date():
    query = request.get_json()
    succ, errors = check(post_periods_date_sample, query)
    if not succ:
        return make_response(jsonify(errors), 400)
    d = datetime.datetime.fromtimestamp(query["date"])
    start, end = get_dates_month_period(d)
    result = {
        "start": start.timestamp(),
        "end": end.timestamp()
    }
    return make_response(jsonify(result), 200)


@app.route("/econ/periods/now", methods=["GET"])
def get_periods_now():
    today = datetime.datetime.today()
    return make_response(jsonify(round(today.timestamp())), 200)


@app.route("/econ/periods/<int:year>/<int:month>", methods=["GET"])
def get_period_year_month(year, month):
    d = datetime.datetime(year, month, 1)
    start, end = get_dates_month_period(d)
    return make_response(jsonify({
        "start": start.timestamp(),
        "end": end.timestamp()
    }), 200)