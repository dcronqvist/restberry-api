from flask import Flask, Blueprint, request, render_template
from flask_restx import Resource, Api, fields
from flask_cors import CORS
import config
from api_v1 import blueprint as apiv1

app = Flask(__name__)

main = Blueprint("main", __name__, url_prefix="/")

@main.route("/")
def hello():
    return render_template("main.html")

app.register_blueprint(apiv1)
app.register_blueprint(main)

CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

app.run(port=config.get_setting("listen-port", 5251), host="0.0.0.0")
