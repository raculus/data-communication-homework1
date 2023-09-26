import socket
from _thread import *
import exam
from log import TimePrint
import time
from clock import Clock

client_sockets = []


HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

clock = Clock()


def addrToStr(addr, client_socket):
    return f"{addr[0]} (Client {client_sockets.index(client_socket)+1})"


def threaded(client_socket, addr):
    TimePrint(f"Connected by {addrToStr(addr,client_socket)}", clock.get_clock())
    problem = exam.problem()
    TimePrint(f'Send problem "{problem}" to {addrToStr(addr,client_socket)}')
    client_socket.send(problem.encode("utf-8"))

    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                TimePrint(f"Disconnected by {addrToStr(addr,client_socket)}")
                break
            TimePrint(
                f"Received from {addrToStr(addr,client_socket)} >> {data.decode('utf-8')}"
            )

            answer = exam.solve(problem)
            solved = data.decode("utf-8")
            TimePrint(f"{problem}={answer}")
            if answer == solved:
                TimePrint(f"{answer} == {solved}")
                problem = exam.problem()
                client_socket.send(problem.encode("utf-8"))
            else:
                TimePrint(f"{answer} != {solved}")
                client_socket.send(problem.encode("utf-8"))

        except ConnectionResetError as e:
            TimePrint(f"Disconnected by {addrToStr(addr,client_socket)}")
            break
        print()
        time.sleep(5)

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        TimePrint(f"Remove client list: {len(client_sockets)}")

    client_socket.close()


def server():
    TimePrint(f"Server start at {HOST}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    try:
        while True:
            TimePrint("Wait join client")

            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)
            start_new_thread(threaded, (client_socket, addr))
            TimePrint(f"Client count: {len(client_sockets)}")
    except Exception as e:
        TimePrint(f"Error: {e}")

    finally:
        server_socket.close()


clock.start_clock()
server()
