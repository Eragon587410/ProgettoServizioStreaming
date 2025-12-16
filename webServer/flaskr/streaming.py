import requests
from _common import *

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory, Response, stream_with_context
)

bp = Blueprint('streaming', __name__, url_prefix='/streaming')

HLS_ADDRESS = "http://host.docker.internal:8080/hls/"
finito = False

#bp.route("/stream")
#def stream_from_java():
#    global finito
#    finito = False
#    if os.path.exists(HLS_FOLDER):
    #     shutil.rmtree(HLS_FOLDER)
    # os.makedirs(HLS_FOLDER, exist_ok=True)
    # java_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # java_sock.connect(("host.docker.internal", 2160))
    # java_sock.sendall("esempio.ts\n".encode())

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
    # ffmpeg = subprocess.Popen([
    #     "ffmpeg",
    #     "-i", "pipe:0",
    #     "-c:v", "libx264",        # ricodifica per PTS coerenti
    #     "-preset", "veryfast",
    #     "-c:a", "aac",            # ricodifica audio
    #     "-b:a", "128k",
    #     "-f", "hls",
    #     "-hls_time", "2",
    #     "-hls_list_size", "0",
    #     "-hls_flags", "append_list+independent_segments",
    #     os.path.join(HLS_FOLDER, "stream.m3u8")
    # ], stdin=subprocess.PIPE)
    # # Thread: forward dati da Java → FFmpeg
    # def forward():
    #     global finito
    #     while True:
    #         data = java_sock.recv(8192)
    #         if not data:
    #             break
    #         ffmpeg.stdin.write(data)
    #     finito = True
    #     ffmpeg.stdin.close()
    #     java_sock.close()

    # threading.Thread(target=forward, daemon=True).start()

    # return "Streaming avviato"


# Serve i segmenti HLS
@bp.route("/hls/<path:filename>")
@login_required
def hls(filename):
    response = requests.get(HLS_ADDRESS + filename)
    headers = {
        "Content-Type": response.headers.get("Content-Type", "application/octet-stream"),
        "Content-Length": response.headers.get("Content-Length")
    }

    # Restituisce il flusso direttamente al client
    return Response(
        stream_with_context(response.iter_content(chunk_size=4096)),
        headers=headers,
        status=response.status_code
    )
#   return send_from_directory(HLS_FOLDER, filename)


# Player HTML
@bp.route("/view")
@login_required
def view_stream():
    g.film = {"id" : "test", "title" : "S.L. EP. 1"}
#    stream_from_java()
    #while not finito == True:
    #    time.sleep(0.1)
    return render_template("films/videoplayer.html")

# <!DOCTYPE html>VECCHIO ESEMPIO
# <html>
# <body>
#   <h1>Streaming Live</h1>
#   <video id="video" controls autoplay width="800">
#     <source src="/streaming/hls/test/master.m3u8" type="application/x-mpegURL">
#   </video>
# </body>
# </html>
# """

@bp.route("/film/<film_id>") #<int:film_id>
def play_film(film_id):
    g.film = {"id" : film_id} 
    return render_template("films/videoplayer.html")#redirect(url_for('streaming.view_stream'))