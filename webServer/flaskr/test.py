import socket
import subprocess
from flask import Flask, Response

app = Flask(__name__)

@app.route("/stream")
def stream():
    # socket verso il server Java
    java_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    java_sock.connect(("java-server", 9000))

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
