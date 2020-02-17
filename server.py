from api import app, config

port = config.get_setting("port", 5000)
ip = config.get_setting("host", "0.0.0.0")

app.run(debug=True, host=ip, port=port)