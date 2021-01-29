from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from werkzeug.datastructures import ImmutableMultiDict
import users
import config as config
from pytechecker import check

app = Flask(__name__)
CORS(app)

# Check if user has privilege to use part of API
def privilege_required(privilege):
	def decorator(func):
		def wrapper(*args, **kwargs):
			if privilege:
				working_user = request.args["username"]
				if users.has_privilege(working_user, privilege.lower()):
					return func(*args, **kwargs)
				else:
					return make_response(jsonify([f"ERROR: Insufficient privileges, resource requires '{privilege.lower()}' for access."]), 403)
			else:
				return func(*args, **kwargs)
		wrapper.__name__ = func.__name__
		return wrapper
	return decorator

@app.before_request
def before():
	if "users/login" not in request.url and "endpoints" not in request.url and "minecraft/serverinfo" not in request.url:
		d = request.args.to_dict(flat=True)
		if "token" in d and "username" in d:
			# Validate token
			succ, tokens = users.validate_token_for_user(d["username"], d["token"])	
			if not succ:
				return make_response(jsonify(["ERROR: Expired or invalid token."]), 401)
			del d["token"]
			request.args = ImmutableMultiDict(d)
		else:
			sample = {
				"token": {
					"required": True,
					"allowed_types": [str]
				},
				"username": {
					"required": True,
					"allowed_types": [str]
				}
			}
			succ, errors = check(sample, d)
			return make_response(jsonify(errors), 401)
		

# Send the response in an appropriate format
@app.after_request
def after(response):
	ret = {
		"status_code": response.status_code,
		"status": response.status,
		"response": response.get_json()
	}
	return make_response(jsonify(ret), ret["status_code"])

import api.routes.economy.accounts
import api.routes.economy.transactions
import api.routes.economy.periods
import api.routes.endpoints
import api.routes.minecraft
import api.routes.users
