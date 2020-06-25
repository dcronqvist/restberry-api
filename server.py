from flask_app import app

app.config["JSON_AS_ASCII"] = False

app.run(debug=True)