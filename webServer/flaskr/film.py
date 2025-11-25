import socket

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sk.connect(("localhost", 2160))
sk.sendall("test.txt\n".encode())


message = None
while True:
    buffer = sk.recv(4096)
    if not buffer:
        break
    if message:
        message = message + buffer
    else:
        message = buffer
print(message.decode())