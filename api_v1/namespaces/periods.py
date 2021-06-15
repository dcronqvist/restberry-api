import datetime as dt
from flask_restx import Resource, Namespace, reqparse
from api_v1 import privilege_required
import requests as req
import config as conf

def get_dates_month_period(date):
    today = date

    current_month = today.month

    if today.day >= 25:
        start_date = dt.datetime(today.year, today.month, 25)
        end_year = today.year
        if today.month >= 12:
            end_year += 1
        end_month = today.month + 1
        if end_month > 12:
            end_month = end_month % 12
        
        end_date = dt.datetime(end_year, end_month, 24, 23, 59, 59)

        return start_date, end_date
    else:
        if today.month == 1:
            start_date = dt.datetime(today.year - 1, 12, 25)
            end_date = dt.datetime(today.year, today.month, 24, 23, 59, 59)
            return start_date, end_date
        else:
            start_date = dt.datetime(today.year, today.month - 1, 25)
            end_date = dt.datetime(today.year, today.month, 24, 23, 59, 59)
            return start_date, end_date

api = Namespace("periods", path="/economy/periods", description="Get previous, current or historical economy period.")

get_month_doc = """
### Get month period

Returns the economic period for the specified month. Expects the month to be a value in the range of 1-12. Also allows for an optional parameter `year` for if you want e.g. month 10 of the 3 previous years like `?month=10&year=2021&year=2020&year=2019`. 

Upon not entering the year, the **current calender year** will be assumed.

#### Privileges
- periods
- economy

"""

get_parser = reqparse.RequestParser()
get_parser.add_argument("month", required=True, action="append", type=int, help="Which month of the year.", location="args", choices=[i for i in range(1, 13)])
get_parser.add_argument("year", action="append", type=int, help="Which year.", location="args")

@api.route("/months")
class PeriodMonthResource(Resource):
    @api.doc("periods_get_months", description=get_month_doc)
    @api.response(400, "User failed to specify at least one month.")
    @api.response(200, "Successfully returned period")
    @api.expect(get_parser, validate=True)
    @privilege_required("periods")
    @privilege_required("economy")
    def get(self):
        args = get_parser.parse_args()
        if not args["year"] and not args["month"]:
            return { "error": "Must specify at least one month."}, 400
        if not args["year"]:
            args["year"] = [dt.datetime.now().year]
        if not args["month"]:
            args["month"] = [dt.datetime.now().month]
        periods = list()
        for y in args["year"]:
            for m in args["month"]:
                start, end = get_dates_month_period(dt.date(y, m, 1))
                periods.append({
                    "year": y,
                    "month": m,
                    "start": start.isoformat(),
                    "start_timestamp": start.timestamp(),
                    "end": end.isoformat(),
                    "end_timestamp": end.timestamp()
                })
        return periods, 200

get_month_current_doc = """
### Get **current** month period

Returns the economic period for the current month.

#### Privileges
- periods
- economy
"""

@api.route("/months/current")
class PeriodMonthCurrentResource(Resource):

    @api.doc("periods_get_months_current", description=get_month_current_doc)
    @api.response(200, "Successfully returned period")
    @privilege_required("periods")
    @privilege_required("economy")
    def get(self):
        d = dt.datetime.today()
        start, end = get_dates_month_period(d)

        period = {
            "start_timestamp": start.timestamp(),
            "start": start.isoformat(),
            "end": end.isoformat(),
            "end_timestamp": end.timestamp(),
            "year": end.year
        }
        return period, 200

get_years_parser = reqparse.RequestParser()
get_years_parser.add_argument("year", required=True, action="store", type=int, help="Which year.", location="args")

get_year_doc = """
### Get year period

Returns the economic period for the specified year. Allows for a single year to be specified.

#### Privileges
- periods
- economy
"""

@api.route("/years")
class PeriodYearResource(Resource):

    @api.doc("periods_get_years", description=get_year_doc)
    @api.response(400, "User failed to specify at least one year.")
    @api.response(200, "Successfully returned period")
    @api.expect(get_years_parser, validate=True)
    @privilege_required("periods")
    @privilege_required("economy")
    def get(self):
        args = get_years_parser.parse_args()

        start = dt.datetime(args["year"] - 1, 12, 25)
        end = dt.datetime(args["year"], 12, 24, 23, 59, 59)

        period = {
            "start_timestamp": start.timestamp(),
            "start": start.isoformat(),
            "end": end.isoformat(),
            "end_timestamp": end.timestamp(),
            "year": end.year
        }
        return period, 200

get_year_current_doc = """
### Get **current** year period

Returns the economic period for the current year.

#### Privileges
- periods
- economy
"""

@api.route("/years/current")
class PeriodYearCurrentResource(Resource):

    @api.doc("periods_get_years_current", description=get_year_current_doc)
    @api.response(200, "Successfully returned period")
    @privilege_required("periods")
    @privilege_required("economy")
    def get(self):
        d = dt.datetime.today()
        start, end = get_dates_month_period(d)

        start = dt.datetime(end.year - 1, 12, 25)
        end = dt.datetime(end.year, 12, 24, 23, 59, 59)

        period = {
            "start_timestamp": start.timestamp(),
            "start": start.isoformat(),
            "end": end.isoformat(),
            "end_timestamp": end.timestamp(),
            "year": end.year
        }
        return period, 200