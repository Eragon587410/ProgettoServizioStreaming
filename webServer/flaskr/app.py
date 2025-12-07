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



HLS_FOLDER = "hls"
os.makedirs(HLS_FOLDER, exist_ok=True)

@app.route("/stream")
def stream_from_java():
    java_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    java_sock.connect(("host.docker.internal", 2160))
    java_sock.sendall("esempio.ts\n".encode())

    # FFmpeg: legge dalla pipe di Java e crea HLS
   # ffmpeg = subprocess.Popen([
    #    "ffmpeg",
    #    "-i", "pipe:0",            # legge dalla stdin
    #    "-c:v", "copy",
    #    "-c:a", "copy",
    #    "-f", "hls",
    #    "-hls_time", "4",
    #    "-hls_list_size", "5",
    #    "-hls_flags", "delete_segments",
    #    os.path.join(HLS_FOLDER, "stream.m3u8")
    #], stdin=subprocess.PIPE)
    ffmpeg = subprocess.Popen([
        "ffmpeg",
        "-i", "pipe:0",
        "-c:v", "libx264",        # ricodifica per PTS coerenti
        "-preset", "veryfast",
        "-c:a", "aac",            # ricodifica audio
        "-b:a", "128k",
        "-f", "hls",
        "-hls_time", "2",
        "-hls_list_size", "0",
        "-hls_flags", "append_list+independent_segments",
        os.path.join(HLS_FOLDER, "stream.m3u8")
    ], stdin=subprocess.PIPE)
    # Thread: forward dati da Java → FFmpeg
    def forward():
        while True:
            data = java_sock.recv(8192)
            if not data:
                break
            ffmpeg.stdin.write(data)
        ffmpeg.stdin.close()
        java_sock.close()

    threading.Thread(target=forward, daemon=True).start()

    return "Streaming avviato"


# Serve i segmenti HLS
@app.route("/hls/<path:filename>")
def hls(filename):
    return send_from_directory(HLS_FOLDER, filename)


# Player HTML
@app.route("/view")
def view_stream():
    return """
<!DOCTYPE html>
<html>
<body>
  <h1>Streaming Live</h1>
  <video id="video" controls autoplay width="800">
    <source src="/hls/stream.m3u8" type="application/x-mpegURL">
  </video>
</body>
</html>
"""
