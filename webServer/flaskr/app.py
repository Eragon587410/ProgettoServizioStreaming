from flask import Flask
import sqlalchemy
import db
    


app = Flask(__name__)
import auth
app.register_blueprint(auth.bp)

db.init_app(app)

@app.route("/")
def homepage():
    return "Hello Arsen"

@app.route("/<name>")
def hallo(name):
    return name