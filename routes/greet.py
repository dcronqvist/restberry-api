from flask_app import app, auth
import config as config
import routes.base as base

@app.route('/')
def hello_world():
    return config.get_setting("greet-home", "Home")

