import config
import users
import sheets
from flask_app import app, auth
from flask import make_response, jsonify, request, render_template
import requests
import datetime

# Get first and last date of the week the specified day is in
def week_first_last(day):
    day_of_week = day.weekday()

    to_beginning_of_week = datetime.timedelta(days=day_of_week)
    beginning_of_week = day - to_beginning_of_week

    to_end_of_week = datetime.timedelta(days=6 - day_of_week)
    end_of_week = day + to_end_of_week

    return (beginning_of_week, end_of_week)

# Get the week's foods at Kårrestaurangen, depending on language.
def jh_get_karr_week(lang):
    today = datetime.datetime.today()
    first, last = week_first_last(today)
    response = requests.get(f"http://carbonateapiprod.azurewebsites.net/api/v1/mealprovidingunits/21f31565-5c2b-4b47-d2a1-08d558129279/dishoccurrences?startDate={first.strftime('%Y-%m-%d')}&endDate={last.strftime('%Y-%m-%d')}")
    week = dict()
    for day in range(5):
        dayName = "monday"
        if day == 1:
            dayName = "tuesday"
        elif day == 2:
            dayName = "wednesday"
        elif day == 3:
            dayName = "thursday"
        elif day == 4:
            dayName = "friday"
        dispNames = response.json()[day].get("displayNames")
        for dispName in dispNames:
            if lang in dispName.get("displayNameCategory").get("displayNameCategoryName").lower():
                week[dayName] = dispName.get("dishDisplayName")
    return week

# Get the week's foods at Express, depending on language
def jh_get_express_week(lang):
    today = datetime.datetime.today()
    first, last = week_first_last(today)
    response = requests.get(f"http://carbonateapiprod.azurewebsites.net/api/v1/mealprovidingunits/3d519481-1667-4cad-d2a3-08d558129279/dishoccurrences?startDate={first.strftime('%Y-%m-%d')}&endDate={last.strftime('%Y-%m-%d')}")
    week = dict()
    for day in range(5):
        dayName = "monday"
        if day == 1:
            dayName = "tuesday"
        elif day == 2:
            dayName = "wednesday"
        elif day == 3:
            dayName = "thursday"
        elif day == 4:
            dayName = "friday"
        dispNames = response.json()[day].get("displayNames")
        for dispName in dispNames:
            if lang in dispName.get("displayNameCategory").get("displayNameCategoryName").lower():
                week[dayName] = dispName.get("dishDisplayName")
    return week

# API Endpoint for retrieving today's week's Kårrestaurangen
@app.route("/food/jh/karr/week/<string:lang>")
def api_jh_karr_week(lang):
    return make_response(jsonify(jh_get_karr_week(lang)), 200)

# API Endpoint for retrieving today's week's Express
@app.route("/food/jh/express/week/<string:lang>")
def api_jh_express_week(lang):
    return make_response(jsonify(jh_get_karr_week(lang)), 200)