import socket
from _thread import *
from exam import solve
from log import TimePrint
import sys

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
        data = client_socket.recv(1024).decode("utf-8")
        TimePrint(f"Recived >> {data}")
        solved = solve(data)
        TimePrint(f"Solved >> {solved}")
        client_socket.send(solved.encode("utf-8"))


start_new_thread(recv_data, (client_socket,))
TimePrint(f"Connected server to {HOST}")

while True:
    message = input()
    if message == "quit":
        close_data = message
        break

    client_socket.send(message.encode("utf-8"))

client_socket.close()
