from flask import Flask
import sqlalchemy

app = Flask(__name__)
import auth
app.register_blueprint(auth.bp)

@app.route("/")
def homepage():
    return "Hello Arsen"

@app.route("/<name>")
def hallo(name):
    return name