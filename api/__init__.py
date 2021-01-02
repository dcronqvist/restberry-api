from flask import Flask, make_response, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
import users
import config as config

app = Flask(__name__)
CORS(app)

auth = HTTPBasicAuth()

# Check if user has privilege to use part of API
def privilege_required(privilege):
	def decorator(func):
		def wrapper(*args, **kwargs):
			working_user = auth.username()
			if users.has_privilege(working_user, privilege):
				return func(*args, **kwargs)
			else:
				return unauthorized(f"Unauthorized Access. Missing privilege: {privilege}")
		wrapper.__name__ = func.__name__
		return wrapper
	return decorator

# Verify password for user
@auth.verify_password
def verify(username, password):
	succ = users.validate_user(username, password)
	return succ

# Tell user that they have unauthorized access to this part of the API
@auth.error_handler
def unauthorized(mess="Unauthorized Access"):
    return make_response(jsonify(["ERROR: Unauthorized Access"]), 401)

# Do nothing special before request, but make sure that the user is logged in
@app.before_request
@auth.login_required
def before():
    pass

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
