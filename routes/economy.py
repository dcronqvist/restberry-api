import config, users, sheets
from flask_app import app, auth
from flask import make_response, jsonify, request, render_template
import requests
import datetime

service = sheets.refresh_token()
economy_sheet = config.get_setting("economy_sheet")

def get_month():
    cats = sheets.get_values(service, economy_sheet, "Översikt Akt. Mån!D6:D7", "FORMATTED_VALUE")
    new = [cat[0] for cat in cats]
    return new


def get_categories():
	cats = sheets.get_values(service, economy_sheet, "UniqueKortUtCategories", "FORMATTED_VALUE")
	new = [cat[0] for cat in cats]
	return new

def get_outcome_row_category(category):
	rows = sheets.get_values(service, economy_sheet, "Översikt Akt. Mån!C14:K35", "UNFORMATTED_VALUE")
	row = sheets.get_row_from_first_c(rows, category)
	return row

def get_outcome(category):
	row = get_outcome_row_category(category)
	if row:
		result = "{:.2f}".format(row[1], 2)
		budget = "{:.2f}".format(row[3], 2)
		average = "{:.2f}".format(row[5], 2)
		balance = "{:.2f}".format(row[8], 2)
		return {"type": {"category" : category }, "result": result, "budget": budget, "average": average, "balance": balance}
	return None

def get_guessed_categories(amount):
	sheets.set_values(service, economy_sheet, "AVGUtgiftTransaktion!E24", amount)
	result = sheets.get_values(service, economy_sheet, "AVGUtgiftTransaktion!G23:G45", "FORMATTED_VALUE")
	cats = [cat[0] for cat in result]
	return cats

@app.route("/econ/categories/findall")
def api_get_categories():
	cats = get_categories()
	return make_response(jsonify(cats), 200)

@app.route("/econ/categories/register/<string:category>")
def api_register_category(category):
	res = sheets.register_outcome(datetime.datetime.now().date().isoformat(), category, "New category", 0)
	return make_response(jsonify({"success": res, "category": category}), 200)

@app.route("/econ/outcomes/month/<string:category>")
def api_get_outcome_category(category):
	print(category)
	row = get_outcome(category)
	if row:
		return make_response(jsonify(row), 200)
	else:
		return make_response(jsonify("No such category"), 404)

@app.route("/econ/outcomes/month")
def api_get_outcome_month():
    rowOut = get_outcome_row_category("Totalt Ut")
    month = get_month()
    res = {"type": {"month-r": month[0], "month-c": month[1] }, "result": "{:.2f}".format(rowOut[1]), "budget": "{:.2f}".format(rowOut[3]), "average": "{:.2f}".format(rowOut[5]), "balance": "{:.2f}".format(rowOut[8])}
    return make_response(jsonify(res), 200)

@app.route("/econ/categories/guess/<string:amount>")
def api_get_category_recomendation(amount):
	cats = get_guessed_categories(amount)
	return make_response(jsonify(cats), 200)

@app.route("/econ/outcomes/register/<string:date>/<string:category>/<string:description>/<string:amount>")
def api_register_outcome(date, category, description, amount):
	res = sheets.register_outcome(date, category, description, amount)
	outcome = get_outcome(category)
	return make_response(jsonify(outcome), 200)
