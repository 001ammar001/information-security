import socket
import threading
from models import User
import json


def handle_client(client_socket: socket.socket):
    with client_socket:
        print(f"Connected by {client_socket.getpeername()}")
        data = client_socket.recv(2048)
        data = json.loads(data)
        if (data.get("action") == 2):
            user = User(
                user_name=data.get("user_name"),
                password=data.get("password"),
                balance=0
            )
            result = User.create_user(user)
            client_socket.sendall(result.encode())

        print(f"Connection closed by {client_socket.getpeername()}")


def start_server(host='127.0.0.1', port=3000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    
    start_server()
