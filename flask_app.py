from flask import Flask
from flask_httpauth import HTTPBasicAuth
import config as config

app = Flask(__name__)
auth = HTTPBasicAuth()

import routes.greet

