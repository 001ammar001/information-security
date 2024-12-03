import socket
import threading
from models import User
import json
from asymmetric_crypt import encrypt,decrypt
from dotenv import load_dotenv
from uuid import uuid4
import os
load_dotenv()

users_keys= { }

def client_exchange_key(client:socket.socket, data: dict):
    session = str(uuid4())
    users_keys[session] = {"public_key": data["personal"], "user_id": None}
    data = {
        "session_id": session, "server_key": os.environ.get("RSA_PUBLIC_KEY")
    }
    client.sendall(json.dumps(data).encode())


def client_login(client_socket: socket.socket, data: dict):
    result = User.login(
        user_name=data.get("user_name"),
        password=data.get("password"),
    )
    if result["status"] == "success":
        users_keys[data.get("session_id")]["user_id"] = int(result["user_id"])
    result = json.dumps(result)
    result = encrypt(users_keys[data["session_id"]]["public_key"].encode(),result.encode())
    client_socket.sendall(result)


def client_register(client_socket: socket.socket, data: dict):
    user = User(
        user_name=data.get("user_name"),
        password=data.get("password"),
        balance="0"
    )
    result = User.create_user(user)
    result = json.dumps(result)
    result = encrypt(users_keys[data["session_id"]]["public_key"].encode(),result.encode())
    client_socket.sendall(result)


def client_deposit(client_socket: socket.socket, data: dict):
    result = User.deposit(users_keys[data.get("session_id")]["user_id"], float(data.get("amount")))
    result = json.dumps(result)
    result = encrypt(users_keys[data["session_id"]]["public_key"].encode(),result.encode())
    client_socket.sendall(result)


def client_withdraw(client_socket: socket.socket, data: dict):
    result = User.withdraw(users_keys[data.get("session_id")]["user_id"], float(data.get("amount")))
    result = json.dumps(result)
    result = encrypt(users_keys[data["session_id"]]["public_key"].encode(),result.encode())
    client_socket.sendall(result)

def get_client_balance(client_socket: socket.socket, data: dict):
    result = User.get_balance(users_keys[data.get("session_id")]["user_id"])
    result = json.dumps(result)
    result = encrypt(users_keys[data["session_id"]]["public_key"].encode(),result.encode())
    client_socket.sendall(result)


def handle_client(client_socket: socket.socket):
    with client_socket:
        print(f"Connected by {client_socket.getpeername()}")
        data = client_socket.recv(2048)
        
        try:
            data = json.loads(data)
        except ValueError:
            data = decrypt(
                private_key=os.environ.get("RSA_PRIVATE_KEY").encode(),
                message= data
                )
            data = json.loads(data)
            
        action = data.get("action")
        print("action: ", action," data: ",data)
        if (action == 0):
            client_exchange_key(client_socket,data)
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
    # keys = generate_rsa_key_pair()
    # key = keys[1].decode()
    # users_keys["amr"] = key
    # message = json.dumps({"message": "hi there","status": "success", "name":"amro"})
    # enc = encrypt_with_user_key(message,"amr")
    # print(enc)
    start_server()
