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
				return unauthorized()
		wrapper.__name__ = func.__name__
		return wrapper
	return decorator

@auth.verify_password
def verify(username, password):
    return users.validate_user(username, password)

@auth.error_handler
def unauthorized():
    return make_response(jsonify("Unauthorized access"), 401)

@app.before_request
@auth.login_required
def before():
    pass

@app.after_request
def after(response):
    return response
#	if response.response[0]:
#		a = response.response[0]
#		a = json.loads(a.decode("utf-8").replace("'",'"'))
#		ret = {
#			"status_code": response._status_code,
#			"status": response._status,
#			"response": a,
#		}
#		return make_response(jsonify(ret), ret["status_code"])
#	else:
#		ret = {
#			"status_code": response._status_code,
#			"status": response._status,
#			"response": None,
#		}
#		return make_response(jsonify(ret), ret["status_code"])

@app.route("/priv")
def has_priv():
    succ, user = users.find_user(auth.username())
    if succ:
        return make_response(jsonify({"privs" : user["privileges"], "has_super": users.has_privilege(auth.username(), "KEBAB")}), 200)