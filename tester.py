from os import system
import threading


def test_client():
    system("python client.py")


for i in range(10):
    threading.Thread(target=test_client, args=()).start()
