import socket
import threading
from models import User
from database import DataBaseHandeler


def handle_client(client_socket):
    with client_socket:
        print(f"Connected by {client_socket.getpeername()}")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            new_user = User(user_name='john_doe',
                            password='securepassword', balance=100.0
                            )
            DataBaseHandeler.get_session().add(new_user)
            client_socket.sendall(data)
            DataBaseHandeler.get_session().commit()
            
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
