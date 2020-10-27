import config
import users
import sheets
from flask_app import app, auth
from flask import abort, make_response, jsonify, request, render_template
import requests
import datetime
import re

from routes.base import privilege_required

# Make sure that the token for using the Sheets API is up to date
service = sheets.refresh_token()
economy_sheet = config.get_setting("economy_sheet")

# Get which month we are in right now
def get_month():
    cats = sheets.get_values(service, economy_sheet, "Översikt Akt. Mån!D6:D7", "FORMATTED_VALUE")
    new = [cat[0] for cat in cats]
    return new

# Get all available categories for outcomes
def get_outcome_categories():
	cats = sheets.get_values(service, economy_sheet, "UniqueKortUtCategories", "FORMATTED_VALUE")
	new = [cat[0] for cat in cats]
	return new

# Get all available categories for outcomes
def get_income_categories():
	cats = sheets.get_values(service, economy_sheet, "UniqueKortInCategories", "FORMATTED_VALUE")
	new = [cat[0] for cat in cats]
	return new

# Get overview of all categories this current month, aswell as the balance, result and average of this month
def get_outcome_row_category(category):
	rows = sheets.get_values(service, economy_sheet, "Översikt Akt. Mån!C14:K36", "UNFORMATTED_VALUE")
	row = sheets.get_row_from_first_c(rows, category)
	return row

# Get info about specific category, result, budget, average and balance
def get_outcome(category):
	row = get_outcome_row_category(category)
	if row:
		result = "{:.2f}".format(row[1])
		budget = "{:.2f}".format(row[3])
		average = "{:.2f}".format(row[5])
		balance = "{:.2f}".format(row[8])
		return {"type": {"category" : category }, "result": result, "budget": budget, "average": average, "balance": balance}
	return None

# Let spreadsheet "guess" which category this might be, from the specified amount
def get_guessed_categories(amount):
	sheets.set_values(service, economy_sheet, "AVGUtgiftTransaktion!E24", amount)
	result = sheets.get_values(service, economy_sheet, "AVGUtgiftTransaktion!G23:G50", "FORMATTED_VALUE")
	cats = [cat[0] for cat in result]
	return cats

def get_searched_categories(search):
	cats = get_outcome_categories()
	print(search)
	s = list()
	for category in cats:
		if(search.lower() in category.lower()):
			s.append(category)
	return s


# API Endpoint for getting all possible outcome categories
@app.route("/econ/outcomes/categories/findall")
@privilege_required("ECON_OUT")
def api_get_categories():
	cats = get_outcome_categories()
	return make_response(jsonify(cats), 200)

# API Endpoint for registering new outcome category
@app.route("/econ/outcomes/categories/register/<string:category>")
@privilege_required("ECON_REG")
def api_register_category(category):
	res = sheets.register_outcome(datetime.datetime.now().date().isoformat(), category, "New category", 0)
	return make_response(jsonify({"success": res, "category": category}), 200)

# API Endpoint for guessing which category a certain amount might be
@app.route("/econ/outcomes/categories/guess/<string:amount>")
@privilege_required("ECON_OUT")
def api_get_category_recomendation(amount):
	cats = get_guessed_categories(amount)
	return make_response(jsonify(cats), 200)

# API Endpoint for searching which category that matches this string
@app.route("/econ/outcomes/categories/search/<string:search>")
@privilege_required("ECON_OUT")
def api_get_category_by_search(search):
	cats = get_searched_categories(search)
	return make_response(jsonify(cats), 200)

# API Endpoint for getting this month's stats for a specific category
@app.route("/econ/outcomes/month/<string:category>")
@privilege_required("ECON_OUT")
def api_get_outcome_category(category):
	print(category)
	row = get_outcome(category)
	if row:
		return make_response(jsonify(row), 200)
	else:
		return make_response(jsonify("No such category"), 404)

# API Endpoint for getting this month's stats
@app.route("/econ/outcomes/month")
@privilege_required("ECON_OUT")
def api_get_outcome_month():
    rowOut = get_outcome_row_category("Totalt Ut")
    month = get_month()
    res = {"type": {"month-r": month[0], "month-c": month[1] }, "result": "{:.2f}".format(rowOut[1]), "budget": "{:.2f}".format(rowOut[3]), "average": "{:.2f}".format(rowOut[5]), "balance": "{:.2f}".format(rowOut[8])}
    return make_response(jsonify(res), 200)

# API Endpoint for registering outcome
@app.route("/econ/outcomes/register", methods=["POST"])
@privilege_required("ECON_REG")
def api_register_outcome():
	if not request.json or not 'date' in request.json:
		abort(400)
	date = request.json['date']
	category = request.json['category']
	description = request.json['description']
	amount = request.json['amount']
	res = sheets.register_outcome(date, category, description, amount)
	outcome = get_outcome(category)
	return make_response(jsonify(outcome), 200)

######################### BELOW IS INCOME RELATED ENDPOINTS ##############################

# API Endpoint for getting all available categories for incomes
@app.route("/econ/incomes/categories/findall")
@privilege_required("ECON_IN")
def api_get_income_categories():
	cats = get_income_categories()
	return make_response(jsonify(cats), 200)

# API Endpoint for getting this month's stats regarding incomes
@app.route("/econ/incomes/month")
@privilege_required("ECON_IN")
def api_get_income_month():
	rowIn = get_outcome_row_category("Totalt In")
	month = get_month()
	res = {"type": {"month-r": month[0], "month-c": month[1] }, "result": "{:.2f}".format(rowIn[1]), "budget": "{:.2f}".format(rowIn[3]), "balance": "{:.2f}".format(rowIn[8])}
	return make_response(jsonify(res), 200)

# API Endpoint for registering income
@app.route("/econ/incomes/register", methods=["POST"])
@privilege_required("ECON_REG")
def api_register_income():
	if not request.json or not 'date' in request.json:
		abort(400)
	date = request.json['date']
	category = request.json['category']
	description = request.json['description']
	amount = request.json['amount']
	res = sheets.register_income(date, category, description, amount)
	return make_response(jsonify(res), 200)
