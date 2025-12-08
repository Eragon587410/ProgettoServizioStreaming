import socket
import subprocess
import threading

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

sk.connect(("host.docker.internal", 2160))
sk.sendall("test.txt\n".encode())



while True:
    chunk = sk.recv(4096)
    if not chunk:
        break
    ffmpeg.stdin.write(chunk)
ffmpeg.stdin.close()

#test