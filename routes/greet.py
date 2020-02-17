from flask_app import app
import config as config

@app.route('/')
def hello_world():
    return config.get_setting("greet-home", "Home")