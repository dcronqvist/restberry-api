from flask import Blueprint, request
from flask_restx import Api
import config as config
from models.users.users import user_client

# Check if user has privilege to use part of API
def privilege_required(privilege):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if privilege and config.get_setting("authorization-enabled", True):
                author = request.headers.get("Authorization")
                if author:
                    succ, username = user_client.get_username_from_token(author)
                    succ, tokens = user_client.validate_token_for_user(username, author)
                    has_priv = user_client.token_has_privilege(author, privilege)
                    
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

from api_v1.namespaces.auth import api as auth
from api_v1.namespaces.pihole import api as pihole
from api_v1.namespaces.periods import api as periods
from api_v1.namespaces.accounts import api as accounts
from api_v1.namespaces.transactions import api as transactions
from api_v1.namespaces.ai import api as ai

blueprint = Blueprint("apiv1", __name__, url_prefix="/v1")

authorizations = {
    'token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api_doc = """
**API Documentation**

v1.0.0: First release of API. Only pihole, period and account endpoints.
v1.1.0: Added transactions namespace.
v1.2.0: Added AI namespace.
v1.3.0: Added basic GraphQL section of API. available at /v1/graphql.
"""

api = Api(blueprint, title="restberry-api", version="1.3.0", description=api_doc, authorizations=authorizations, security=["token"])

api.add_namespace(auth)
api.add_namespace(pihole)
api.add_namespace(periods)
api.add_namespace(accounts)
api.add_namespace(transactions)
api.add_namespace(ai)