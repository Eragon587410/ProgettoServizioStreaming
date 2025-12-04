from functools import wraps
from flask import Flask, render_template, session, redirect, url_for, g, Response
import sqlalchemy
import db
import auth
import subprocess
import socket


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

@app.route("/film/<film_id>") #<int:film_id>
def play_film(film_id):
    return film_id



@app.route("/stream")
def stream():
    # socket verso il server Java
    java_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    java_sock.connect(("host.docker.internal", 2160))
    java_sock.sendall("test.txt\n".encode())

    # FFmpeg: input raw h264/h265 → output MPEG-TS
    ffmpeg = subprocess.Popen(
        [
            "ffmpeg",
            "-loglevel", "quiet",
            "-i", "pipe:0",         # input da stdin
            "-c:v", "copy",         # non ricodifica (usiamo il codec originale)
            "-f", "mpegts",         # container streamabile
            "pipe:1"                # output su stdout
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    # THREAD: riceve raw dal Java e li manda a FFmpeg
    def pump_input():
        while True:
            chunk = java_sock.recv(4096)
            if not chunk:
                break
            ffmpeg.stdin.write(chunk)
        ffmpeg.stdin.close()

    import threading
    threading.Thread(target=pump_input, daemon=True).start()

    # Generator del flusso MPEG-TS verso il browser
    def generate():
        while True:
            out = ffmpeg.stdout.read(4096)
            if not out:
                break
            yield out

    return Response(generate(), mimetype="video/mp2t")