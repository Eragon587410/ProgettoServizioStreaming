from flask import Flask
import sqlalchemy
import db
import auth


app = Flask(__name__)

app.register_blueprint(auth.bp)

db.init_app(app)

@app.route("/")
def homepage():
    return "Hello Arsen"

@app.route("/<name>")
def hallo(name):
    return name