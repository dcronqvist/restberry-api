from api import app
import config

app.config["JSON_AS_ASCII"] = False

app.run(debug=True, port=config.get_setting("listen-port", 5251))
