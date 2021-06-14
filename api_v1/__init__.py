from flask import Blueprint, request
from flask_restx import Api
# from flask_cors import CORS
# from werkzeug.datastructures import ImmutableMultiDict
import users
# import config as config
# from pytechecker import check

# Check if user has privilege to use part of API
def privilege_required(privilege):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if privilege:
                author = request.headers.get("Authorization")
                if author:
                    succ, username = users.get_username_from_token(author)
                    succ, tokens = users.validate_token_for_user(username, author)
                    has_priv = users.token_has_privilege(author, privilege)
                    
                    if has_priv and succ:
                        return func(*args, **kwargs)
                    elif not has_priv:
                        return { "error": f"Insufficient privileges, resource requires '{privilege.lower()}' for access."}, 403
                    elif not succ:
                        return { "error": f"Invalid token." }, 401
                else:
                    return { "error": f"Must specify 'Authorization' header with token."}, 401
            return func(*args, **kwargs)    
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


# # Send the response in an appropriate format
# @app.after_request
# def after(response):
# 	ret = {
# 		"status_code": response.status_code,
# 		"status": response.status,
# 		"response": response.get_json()
# 	}
# 	return make_response(jsonify(ret), ret["status_code"])

# @app.route("/")
# def base():
# 	return make_response(jsonify(config.get_setting("greet-home", "Hello World!")), 200)

# import api.routes.economy.accounts
# import api.routes.economy.transactions
# import api.routes.economy.periods
# import api.routes.endpoints
# import api.routes.minecraft
# import api.routes.users

from api_v1.namespaces.auth import api as auth
from api_v1.namespaces.pihole import api as pihole

blueprint = Blueprint("apiv1", __name__, url_prefix="/v1")

authorizations = {
    'token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(blueprint, title="restberry-api", version="1.0", description="a dani api", authorizations=authorizations, security=["token"])

api.add_namespace(auth)
api.add_namespace(pihole)