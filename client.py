import socket
from _thread import *
from exam import solve
from log import TimePrint


HOST = "127.0.0.1"
PORT = 9999

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
TimePrint("Connected server")

while True:
    message = input()
    if message == "quit":
        close_data = message
        break

    client_socket.send(message.encode("utf-8"))

client_socket.close()
