import socket
import json

HOST = "127.0.0.1"
PORT = 3000


def get_action() -> int:
    try:
        action = int(input(
            """
    enter the action you want to do\n
    1. login
    2. register
    """))
        if action < 0 or action > 2:
            raise ValueError

        return action

    except:
        print("please enter a valid choice")


def do_login(conn):
    pass
    # name = input("user name: ")
    # password = input("password: ")
    # conn.sendall(json.dumps(
    #     {'user_name': name, 'password': password, "action": 1}).encode()
    # )
    # data = conn.recv(2048)
    # print(data)


def do_register(conn):
    name = input("user name: ")
    password = input("password: ")
    conn.sendall(json.dumps(
        {'user_name': name, 'password': password, "action": 2}).encode()
    )
    data = conn.recv(2048)
    print(data)


def do_action(conn, action):
    if action == 1:
        do_login(conn)
    if action == 2:
        do_register(conn)


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        connection.connect((HOST, PORT))
        action = get_action()
        do_action(connection, action)
