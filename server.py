from api import app

app.config["JSON_AS_ASCII"] = False

app.run(debug=True, port=5251)
