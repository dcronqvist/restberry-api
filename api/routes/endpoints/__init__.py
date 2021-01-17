import config
import users
from api import app, auth
from flask import make_response, jsonify, request, render_template
import requests
import datetime
import urllib

# Helper functions which lists all possible endpoints
def list_routes():
    return ['%s' % rule for rule in app.url_map.iter_rules()]

# Get all endpoints, where some are excluded
def get_all_endpoints():
    return sorted([route for route in list_routes() if "static" not in route])

# Search endpoints given input
def find_endpoints(s):
    return sorted([route for route in get_all_endpoints() if s in route])
        
# API Endpoint for all available endpoints
@app.route("/endpoints/all")
def api_get_all_endpoints():
    return make_response(jsonify(get_all_endpoints()), 200)

# API Endpoint for searching endpoint
@app.route("/endpoints/search/<string:search>")
def api_find_endpoints(search):
    return make_response(jsonify(find_endpoints(search)), 200)