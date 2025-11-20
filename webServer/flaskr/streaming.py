import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect():
    client_socket.connect(("localhost", 2160))

def send_title(title: str):
    client_socket.sendall(f"{title}\n".encode())