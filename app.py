from flask import Flask, Blueprint, request, render_template
from flask_restx import Resource, Api, fields
from flask_cors import CORS
import config
from api_v1 import blueprint as apiv1
from api_v1.graphql import graphql_schema
from flask_graphql import GraphQLView

app = Flask(__name__)

main = Blueprint("main", __name__, url_prefix="/")

@main.route("/")
def hello():
    return render_template("main.html")

app.register_blueprint(apiv1)
app.register_blueprint(main)

app.add_url_rule("/v1/graphql", view_func=GraphQLView.as_view("graphql", schema=graphql_schema, graphiql=config.get_setting("dev-user", None)))

CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

app.run(debug=True, port=config.get_setting("listen-port", 5251))
