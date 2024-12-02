import socket
import json

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
    ISLOGED_IN = False

    @staticmethod
    def get_auth_actions() -> int:
        print(Client.ISLOGED_IN)
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
        print(Client.ISLOGED_IN)
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
        print(data)
        return json.loads(data)

    @staticmethod
    def login(conn: socket.socket):
        name = input("user name: ")
        password = input("password: ")
        conn.sendall(json.dumps(
            {'user_name': name, 'password': password, "action": 1}).encode()
        )
        data = Client.get_response(conn)
        if (data.get("status") == "success"):
            Client.ISLOGED_IN = True

    @staticmethod
    def register(conn: socket.socket):
        name = input("user name: ")
        password = input("password: ")
        conn.sendall(json.dumps(
            {'user_name': name, 'password': password, "action": 2}).encode()
        )
        Client.get_response(conn)

    @staticmethod
    def deposit(conn: socket.socket):
        amount = get_valid_number("enter the amount you want to deposit: ")
        # TODO: make user id dynamic
        user_id = 1
        conn.sendall(json.dumps(
            {'user_id': user_id, 'amount': amount, "action": 3}).encode()
        )
        Client.get_response(conn)

    @staticmethod
    def withdraw(conn: socket.socket):
        amount = get_valid_number("enter the amount you want to withdraw: ")
        user_id = 1
        conn.sendall(json.dumps(
            {'user_id': user_id, 'amount': amount, "action": 4}).encode()
        )
        Client.get_response(conn)


    @staticmethod
    def show_balance(conn: socket.socket):
        user_id = 1
        conn.sendall(json.dumps(
            {'user_id': user_id, "action": 5}).encode()
        )
        Client.get_response(conn)

    @staticmethod
    def perform_action(conn, action):
        if action == 1:
            Client.login(conn)
        if action == 2:
            Client.register(conn)

        if action > 2 and not Client.ISLOGED_IN:
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
                if Client.ISLOGED_IN:
                    action = Client.get_actions()
                else:
                    action = Client.get_auth_actions()
                Client.perform_action(connection, action)


Client.start()

