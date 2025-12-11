from functools import wraps
from flask import Flask, render_template, session, redirect, url_for, g, Response, stream_with_context, send_from_directory
import sqlalchemy
import db
import auth
import subprocess
import socket
import threading
import requests
import os
import streaming
from _common import *

app = Flask(__name__)
app.secret_key = "DEV"

#test
app.register_blueprint(auth.bp)
app.register_blueprint(streaming.bp)


db.init_app(app)




#@app.before_request
def load_films():
    db.get_films()
    if session.get("films"):
        g.films = session['films']

@app.route("/")
def homepage():
    return "Hello Arsen"


@app.route("/films")
@login_required
def films():
    load_films()
    return render_template('films/homepage.html')


@app.before_request
def load_user():
    if session.get("user"):
        g.user = session['user']
    else:
        g.user = None








