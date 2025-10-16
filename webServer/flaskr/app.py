from flask import Flask, session, redirect, url_for
import sqlalchemy
import db
import auth


app = Flask(__name__)

app.register_blueprint(auth.bp)

db.init_app(app)


def login_required(func):
    def wrapper():
        out = None
        if session.get("user"):
            out = func()
        else:
            out = redirect(url_for('auth.login'))
        return out
    return wrapper

@app.route("/")
def homepage():
    return "Hello Arsen"


@app.route("/nicola")
@login_required
def hallo():
    return "name"

