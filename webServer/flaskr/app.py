from functools import wraps
from flask import Flask, render_template, session, redirect, url_for, g, Response, stream_with_context, send_from_directory, request, jsonify
import sqlalchemy
import db.models as models
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


#db.init_app(app)




#@app.before_request
#def load_films():
#    db.get_films()
#    if session.get("films"):
#        g.films = session['films']

def load_films(session):
    films = models.Film.get_films(session=session)
    g.films = films

@app.route("/")
def homepage():
    return "Hello Arsen"


@app.route("/films")
@login_required
def films():
    with models.Film.session() as session:
        load_films(session)
        return render_template('films/homepage.html')


@app.before_request
def load_user():
    if session.get("user"):
        g.user = session['user']
    else:
        g.user = None


@app.route("/search")
def search():
    query = request.args.get("q", "")
    films = models.Film.searchbar(query) if query else []
    return render_template("search_results.html", films=films, query=query)

@app.route("/autocomplete")
def autocomplete():
    term = request.args.get("term", "")
    if not term:
        return jsonify([])

    films = models.Film.searchbar(term)  # usa il tuo metodo già fatto
    # Prendi solo i titoli per i suggerimenti
    return jsonify(films)


@app.context_processor
def inject_globals():
    return {
        "genres": models.Genre.get_genres_names()
    }


@app.route("/genres/<name>")
@login_required
def genre(name):
    films = models.Film.get_most_popular_films(genre=name)
    return render_template('genres/genre.html', films=films)








