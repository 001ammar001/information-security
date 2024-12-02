import socket
import threading
from models import User
import json


def client_login(client_socket: socket.socket, data: dict):
    result = User.login(
        user_name=data.get("user_name"),
        password=data.get("password"),
    )
    client_socket.sendall(result.encode())


def client_register(client_socket: socket.socket, data: dict):
    user = User(
        user_name=data.get("user_name"),
        password=data.get("password"),
        balance="0"
    )
    result = User.create_user(user)
    client_socket.sendall(result.encode())


def client_deposit(client_socket: socket.socket, data: dict):
    result = User.deposit(data.get("user_id"), float(data.get("amount")))
    client_socket.sendall(result.encode())


def client_withdraw(client_socket: socket.socket, data: dict):
    result = User.withdraw(data.get("user_id"), float(data.get("amount")))
    client_socket.sendall(result.encode())

def get_client_balance(client_socket: socket.socket, data: dict):
    result = User.get_balance(data.get("user_id"))
    client_socket.sendall(result.encode())


def handle_client(client_socket: socket.socket):
    with client_socket:
        print(f"Connected by {client_socket.getpeername()}")
        data = client_socket.recv(2048)
        data = json.loads(data)
        action = data.get("action")

        if (action == 1):
            client_login(client_socket, data)
        if (action == 2):
            client_register(client_socket, data)
        if (action == 3):
            client_deposit(client_socket, data)
        if (action == 4):
            client_withdraw(client_socket, data)
        if (action == 5):
            get_client_balance(client_socket, data)

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
