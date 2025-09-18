from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage():
    return "Hello Arsen"

@app.route("/<name>")
def hallo(name):
    return name