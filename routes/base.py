from flask_app import app, auth
import config as config

# This function is not used for the moment.
#def privilege_required(privilege):
#	def decorator(func):
#		def wrapper(*args, **kwargs):
#			working_user = auth.username()
#			if users.has_privilege(working_user, privilege):
#				return func(*args, **kwargs)
#			else:
#				return unauthorized()
#		wrapper.__name__ = func.__name__
#		return wrapper
#	return decorator

@auth.verify_password
def verify(username, password):
    return True # Everyone is granted access for now, until user management is added.

@app.before_request
@auth.login_required
def before():
    pass