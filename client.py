import socket
import json
from key_generate import generate_rsa_key_pair
from asymmetric_crypt import decrypt,encrypt
HOST = "127.0.0.1"
PORT = 3000

def get_valid_number(message: str):
    while True:
        try:
            amount = float(input(message))
            return amount
        except ValueError:
            print("Enter a valid number")


class Client:
    SESSION_ID = None
    IS_LOGGEDIN = False
    SERVER_KEY = ""
    PERSONAL_KEYS = {}

    @staticmethod
    def get_auth_actions() -> int:
        try:
            action = int(input(
                """
enter the action you want to do
1. login
2. register
"""))
            if action < 0 or action > 2:
                raise ValueError

            return action

        except:
            print("please enter a valid choice")

    @staticmethod
    def get_actions() -> int:
        try:
            action = int(input(
                """
enter the action you want to do
1. deposit
2. withdraw
3. show balance
"""))
            if action < 0 or action > 3:
                raise ValueError

            return action + 2

        except:
            print("please enter a valid choice")

    @staticmethod
    def get_response(conn: socket.socket):
        data = conn.recv(2048)
        dec_data = decrypt(Client.PERSONAL_KEYS["private"], data)
        print("Response",dec_data := json.loads(dec_data))
        return dec_data

    @staticmethod
    def key_exchange(conn: socket.socket):
        private, public = generate_rsa_key_pair()
        Client.PERSONAL_KEYS["private"],Client.PERSONAL_KEYS["public"] = private.decode(), public.decode()
        conn.sendall(json.dumps({
            "action": 0,
            "personal": Client.PERSONAL_KEYS["public"] 
        }).encode())
        data = conn.recv(2048)
        data = json.loads(data)
        Client.SESSION_ID = data["session_id"]
        Client.SERVER_KEY = data["server_key"]

    @staticmethod
    def login(conn: socket.socket):
        name = input("user name: ")
        password = input("password: ")
        data = encrypt(Client.SERVER_KEY.encode(),json.dumps({
            'user_name': name, 'password': password, "action": 1,"session_id": Client.SESSION_ID
        }).encode())
        conn.sendall(data)

        response = Client.get_response(conn)
        
        if (response.get("status") == "success"):
            Client.IS_LOGGEDIN = True

    @staticmethod
    def register(conn: socket.socket):
        name = input("user name: ")
        password = input("password: ")
        data = encrypt(Client.SERVER_KEY.encode(),json.dumps({
            'user_name': name, 'password': password, "action": 2,"session_id": Client.SESSION_ID
        }).encode())
        conn.sendall(data)
        Client.get_response(conn)

    @staticmethod
    def deposit(conn: socket.socket):
        amount = get_valid_number("enter the amount you want to deposit: ")
        data = encrypt(Client.SERVER_KEY.encode(),json.dumps({
            'amount': amount, "action": 3, "session_id": Client.SESSION_ID
            }).encode())
        
        conn.sendall(data)
        Client.get_response(conn)

    @staticmethod
    def withdraw(conn: socket.socket):
        amount = get_valid_number("enter the amount you want to withdraw: ")
        data = encrypt(Client.SERVER_KEY.encode(),json.dumps({
            'amount': amount, "action": 4, "session_id": Client.SESSION_ID
            }).encode())
        
        conn.sendall(data)
        Client.get_response(conn)


    @staticmethod
    def show_balance(conn: socket.socket):
        data = encrypt(Client.SERVER_KEY.encode(),json.dumps({
            "action": 5, "session_id": Client.SESSION_ID
            }).encode())
        
        conn.sendall(data)
        Client.get_response(conn)

    @staticmethod
    def perform_action(conn, action):
        if action == 1:
            Client.login(conn)
        if action == 2:
            Client.register(conn)

        if action > 2 and not Client.IS_LOGGEDIN:
            print("Method not allowd")
            return

        if action == 3:
            Client.deposit(conn)
        if action == 4:
            Client.withdraw(conn)
        if action == 5:
            Client.show_balance(conn)

    @staticmethod
    def start():
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
                connection.connect((HOST, PORT))
                if not Client.PERSONAL_KEYS or not Client.SERVER_KEY:
                    Client.key_exchange(connection) 
                    continue
                    
                if Client.IS_LOGGEDIN:
                    action = Client.get_actions()
                else:
                    action = Client.get_auth_actions()
                Client.perform_action(connection, action)


Client.start()

