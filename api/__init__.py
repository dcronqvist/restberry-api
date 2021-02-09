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
				args = request.args.to_dict(flat=True)
				succ, errors = check(sample, args, allow_overflow=True)
				if not succ:
					return make_response(jsonify(["ERROR: Missing token and/or username url parameter."]), 401)
				succ, tokens = users.validate_token_for_user(args["username"], args["token"])	
				if not succ:
					return make_response(jsonify(["ERROR: Expired or invalid token."]), 401)
				del args["token"]
				print(args)
				request.args = ImmutableMultiDict(args)
				working_user = args["username"]
				if users.has_privilege(working_user, privilege.lower()):
					return func()
				else:
					return make_response(jsonify([f"ERROR: Insufficient privileges, resource requires '{privilege.lower()}' for access."]), 403)
			else:
				return func()
		wrapper.__name__ = func.__name__
		return wrapper
	return decorator
		

# Send the response in an appropriate format
@app.after_request
def after(response):
	ret = {
		"status_code": response.status_code,
		"status": response.status,
		"response": response.get_json()
	}
	return make_response(jsonify(ret), ret["status_code"])

@app.route("/")
def base():
	return make_response(jsonify(config.get_setting("greet-home", "Hello World!")), 200)

import api.routes.economy.accounts
import api.routes.economy.transactions
import api.routes.economy.periods
import api.routes.endpoints
import api.routes.minecraft
import api.routes.users
