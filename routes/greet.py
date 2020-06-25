from flask import make_response, jsonify
from flask_app import app, auth
import config as config
import routes.base as base

# Base route to greet user for using api successfully.
@app.route('/')
def hello_world():
    return make_response(jsonify(config.get_setting("greet-home", "Home")), 200)

