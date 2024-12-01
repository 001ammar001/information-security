import socket
import json
from time import sleep
HOST = "127.0.0.1" 
PORT = 3000

data = b""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(b"RSA")
        data += s.recv(1024)
        data += s.recv(1024)
        data += s.recv(1024)

print(f"Received {data!r}")