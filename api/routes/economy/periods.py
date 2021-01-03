import config
import users
from api import app, auth, privilege_required
from flask import abort, make_response, jsonify, request, render_template
import requests
import datetime
import re
from pytechecker import check
from api.routes.economy import get_dates_month_period
from db import coll_accounts, coll_trans, stringify_ids
import pymongo


"""
DONE
/v1/economy/periods/months
/v1/economy/periods/months?year=2020&month=1
/v1/economy/periods/months?year=2020&month=1&month=3
/v1/economy/periods/months?year=2020&month=1&month=3&year=2021
/v1/economy/periods/months?year=2020
/v1/economy/periods/months?year=2020&year=2021
/v1/economy/periods/months?month=1
/v1/economy/periods/months?month=1&month=3
/v1/economy/periods/months/current
/v1/economy/periods/years
/v1/economy/periods/years?year=2020
/v1/economy/periods/years?year=2020&year=2021
/v1/economy/periods/years/current
"""

@app.route("/v1/economy/periods/months", methods=["GET"])
@privilege_required("economy")
def get_economy_periods_months():
    sample_args = {
        "year": {
            "required": False,
            "allowed_types": [list],
            "list_element": {
                "allowed_types": [str]
            }
        },
        "month": {
            "required": False,
            "allowed_types": [list],
            "list_element": {
                "allowed_types": [str]
            }
        }
    }
    username = auth.username()
    args = request.args.to_dict(flat=False)
    succ, errors = check(sample_args, args)
    if not succ:
        return make_response(jsonify(errors), 400)

    periods = []
    if "year" in args and len(args["year"]) > 0 and "month" in args and len(args["month"]) > 0:
        for year in args["year"]:
            for month in args["month"]:
                d = datetime.datetime(int(year), int(month), 1)
                start, end = get_dates_month_period(d)
                periods.append({
                    "year": year,
                    "month": month,
                    "start": start,
                    "start_timestamp": start.timestamp(),
                    "end": end,
                    "end_timestamp": end.timestamp()
                })
    elif "year" in args and len(args["year"]) > 0 and "month" not in args:
        for year in args["year"]:
            for month in range(1, 13):
                d = datetime.datetime(int(year), int(month), 1)
                start, end = get_dates_month_period(d)
                periods.append({
                    "year": year,
                    "month": month,
                    "start": start,
                    "start_timestamp": start.timestamp(),
                    "end": end,
                    "end_timestamp": end.timestamp()
                })
    elif "month" in args and len(args["month"]) > 0 and "year" not in args:
        first = coll_trans.find({"user": username}).sort("date_trans", pymongo.ASCENDING).limit(1).next()
        last = coll_trans.find({"user": username}).sort("date_trans", pymongo.DESCENDING).limit(1).next()
        d = datetime.datetime.fromtimestamp(first["date_trans"])
        today = datetime.datetime.today()

        for month in args["month"]:
            for year in range(d.year, today.year + 1):
                dt = datetime.datetime(int(year), int(month), 1)
                start, end = get_dates_month_period(dt)
                if start.timestamp() < last["date_trans"]:
                    periods.append({
                        "year": year,
                        "month": month,
                        "start": start,
                        "start_timestamp": start.timestamp(),
                        "end": end,
                        "end_timestamp": end.timestamp()
                    })

    return make_response(jsonify(periods), 200)


@app.route("/v1/economy/periods/months/current", methods=["GET"])
@privilege_required("economy")
def get_economy_periods_months_current():
    sample_args = {}
    args = request.args.to_dict()
    succ, errors = check(sample_args, args)
    if not succ:
        return make_response(jsonify(errors), 400)
    d = datetime.datetime.today()
    start, end = get_dates_month_period(d)
    period = {
        "year": end.year,
        "month": end.month,
        "start": start,
        "start_timestamp": start.timestamp(),
        "end": end,
        "end_timestamp": end.timestamp()
    }
    return make_response(jsonify(period), 200)


@app.route("/v1/economy/periods/years", methods=["GET"])
@privilege_required("economy")
def get_economy_periods_years():
    sample_args = {
        "year": {
            "required": False,
            "allowed_types": [list],
            "list_element": {
                "allowed_types": [str]
            }
        }
    }
    username = auth.username()
    args = request.args.to_dict(flat=False)
    succ, errors = check(sample_args, args)
    if not succ:
        return make_response(jsonify(errors), 400)
    first = coll_trans.find({"user": username}).sort("date_trans", pymongo.ASCENDING).limit(1).next()
    last = coll_trans.find({"user": username}).sort("date_trans", pymongo.DESCENDING).limit(1).next()
    first_date = datetime.datetime.fromtimestamp(first["date_trans"])
    last_date = datetime.datetime.fromtimestamp(last["date_trans"])
    _, end_f = get_dates_month_period(first_date)
    _, end_l = get_dates_month_period(last_date)
    periods = []
    for year in range(end_f.year, end_l.year + 1):
        start = datetime.datetime(year - 1, 12, 25)
        end = datetime.datetime(year, 12, 24, 23, 59, 59)
        periods.append({
            "start_timestamp": start.timestamp(),
            "start": start,
            "end": end,
            "end_timestamp": end.timestamp(),
            "year": year
        })
    if "year" in args:
        periods = [period for period in periods if str(period["year"]) in args["year"]]
    return make_response(jsonify(periods), 200)


@app.route("/v1/economy/periods/years/current", methods=["GET"])
@privilege_required("economy")
def get_economy_periods_years_current():
    dt = datetime.datetime.today()
    start, end = get_dates_month_period(dt)

    start = datetime.datetime(end.year - 1, 12, 25)
    end = datetime.datetime(end.year, 12, 24, 23, 59, 59)

    period = {
        "start_timestamp": start.timestamp(),
        "start": start,
        "end": end,
        "end_timestamp": end.timestamp(),
        "year": end.year
    }

    return make_response(jsonify(period), 200)