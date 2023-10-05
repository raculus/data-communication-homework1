import socket
from _thread import *
from exam import solve
from log import TimePrint
import sys
from send import *
import random
import time

HOST = "192.168.0.34"
PORT = 9999

arg = sys.argv
if len(arg) == 2:
    HOST = arg[1]
elif len(arg) == 3:
    HOST = arg[1]
    PORT = arg[2]


TimePrint(f"Try connection to {HOST}:{PORT}")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def recv_data(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            TimePrint(f"Recived >> {data}")
            solved = solve(data)
            delay = random.uniform(0.1, 5.0)
            time.sleep(delay)
            client_socket.send(solved.encode())
            TimePrint(f"Solved >> {solved}")
        except Exception as e:
            exit()


start_new_thread(recv_data, (client_socket,))
TimePrint(f"Connected server to {HOST}")

while True:
    message = input()
    if message == "quit":
        close_data = message
        break

    client_socket.send(message.encode("utf-8"))

client_socket.close()
