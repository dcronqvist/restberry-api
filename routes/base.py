from flask import make_response, jsonify
import json
from flask_app import app, auth
import config as config
import users as users

def privilege_required(privilege):
	def decorator(func):
		def wrapper(*args, **kwargs):
			working_user = auth.username()
			if users.has_privilege(working_user, privilege):
				return func(*args, **kwargs)
			else:
				return unauthorized("Unauthorized Access")
		wrapper.__name__ = func.__name__
		return wrapper
	return decorator

@auth.verify_password
def verify(username, password):
	succ = users.validate_user(username, password)
	return succ

@auth.error_handler
def unauthorized(mess="Unauthorized Access"):
    return make_response(jsonify(mess), 401)

@app.before_request
@auth.login_required
def before():
    pass

@app.after_request
def after(response):
	ret = {
		"status_code": response.status_code,
		"status": response.status,
		"response": response.get_json()
	}
	return make_response(jsonify(ret), ret["status_code"])