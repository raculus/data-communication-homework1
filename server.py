import socket
from _thread import *
import exam
from log import *
import time
from clock import Clock
import random
import threading
from send import *

client_sockets = []

minuteLimit = 1
secondlimit = minuteLimit * 60
secondlimit = 10

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

clock = Clock()
log = Log("Server.txt")


def addrToStr(addr, client_socket):
    return f"{addr[0]} (Client {client_sockets.index(client_socket)+1})"


def threaded(client_socket, addr):
    log.write(
        TimePrint(
            f"Connected by {addrToStr(addr,client_socket)}",
            clock.get_clock(),
        )
    )
    problem = exam.problem()
    log.write(
        TimePrint(
            f'Send problem "{problem}" to {addrToStr(addr,client_socket)}',
            clock.get_clock(),
        )
    )
    client_socket.send(problem.encode("utf-8"))

    while clock.get_clock() <= secondlimit:
        try:
            data = client_socket.recv(1024)

            if not data:
                log.write(
                    TimePrint(
                        f"Disconnected by {addrToStr(addr,client_socket)}",
                        clock.get_clock(),
                    )
                )
                break
            log.write(
                TimePrint(
                    f"Received from {addrToStr(addr,client_socket)} >> {data.decode('utf-8')}",
                    clock.get_clock(),
                )
            )

            answer = exam.solve(problem)
            solved = data.decode("utf-8")

            if answer == solved:
                log.write(
                    TimePrint(
                        f"Correct {addrToStr(addr, client_socket)}", clock.get_clock()
                    )
                )
                problem = exam.problem()
            else:
                log.write(
                    TimePrint(
                        f"Incorrect {addrToStr(addr, client_socket)}", clock.get_clock()
                    )
                )
            log.write(
                TimePrint(
                    f'Send problem "{problem}" to {addrToStr(addr,client_socket)}',
                    clock.get_clock(),
                )
            )
            delay = random.uniform(0.1, 5.0)
            time.sleep(delay)
            client_socket.send(problem.encode())
            print()
            log.write()

        except ConnectionResetError as e:
            log.write(
                TimePrint(
                    f"Disconnected by {addrToStr(addr,client_socket)}",
                    clock.get_clock(),
                )
            )
            break
    log.save()
    client_socket.close()
    exit()


def server():
    log.write(TimePrint(f"Server start at {HOST}", clock.get_clock()))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    try:
        # TODO: 서버 안꺼짐
        while clock.get_clock() <= secondlimit:
            log.write(TimePrint("Wait join client", clock.get_clock()))

            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)
            start_new_thread(threaded, (client_socket, addr))

    except Exception as e:
        log.write(TimePrint(f"Error: {e}", clock.get_clock()))


clock.start_clock()
server()
log.write(TimePrint("Server stopping...", clock.get_clock()))
log.save()
