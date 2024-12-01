import socket
import threading
from time import sleep
from models import User
from database import DataBaseHandeler


def handle_client(client_socket):
    with client_socket:
        print(f"Connected by {client_socket.getpeername()}")
        while True:
            data = client_socket.recv(1)
            if not data:
                break
            client_socket.sendall(data)

        new_user = User(user_name='john_doe',
                        password='securepassword', balance=100.0
                        )
        User.create_user(new_user)
        
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
