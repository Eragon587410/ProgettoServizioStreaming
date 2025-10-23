from functools import wraps
from flask import Flask, render_template, session, redirect, url_for, g
import sqlalchemy
import db
import auth


app = Flask(__name__)
app.secret_key = "DEV"

#test
app.register_blueprint(auth.bp)

db.init_app(app)


def login_required(func):
    @wraps(func)  #mantiene il nome, il docstring e l’endpoint della funzione originale. Senza questo, Flask registra wrapper invece di films, e non funziona il redirect.
    def wrapper():
        out = None
        if g.user:
            out = func()
        else:
            out = redirect(url_for('auth.login'))
        return out
    return wrapper

@app.route("/")
def homepage():
    return "Hello Arsen"


@app.route("/films")
@login_required
def films():
    return render_template('films/homepage.html')


@app.before_request
def load_user():
    if session.get("user"):
        g.user = session['user']
    else:
        g.user = None

@app.before_request
def load_films():
    db.get_films()
    if session.get("films"):
        g.films = session['films']
