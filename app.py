from flask import Flask, Blueprint, request, render_template
from flask_restx import Resource, Api, fields
import config
from api_v1 import blueprint as apiv1

app = Flask(__name__)

main = Blueprint("main", __name__, url_prefix="/")

@main.route("/")
def hello():
    return render_template("main.html")

app.register_blueprint(apiv1)
app.register_blueprint(main)

app.run(debug=True, port=config.get_setting("listen-port", 5251), host="0.0.0.0")