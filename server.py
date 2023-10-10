import socket
from _thread import *
import exam
from log import *
import time
from clock import Clock
import random
from threading import Thread
import os

client_sockets = []

minuteLimit = 1
secondlimit = minuteLimit * 60


HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

clock = Clock()
log = Log("Server.txt")

result = 0


def client_name(client_socket):
    return f"Client{client_sockets.index(client_socket)+1}"


def threaded(client_socket, addr):
    global result

    name = client_name(client_socket)
    log.write(
        TimePrint(
            f"Connected by {addr[0]} ({name})",
            clock.get(),
        )
    )
    client_socket.send(f"Name: {name}".encode())
    log.write(TimePrint(f"{addr[0]} name: {name}", clock.get()))
    log.write()
    print()

    problem = exam.problem()
    log.write(
        TimePrint(
            f'Send problem "{problem}" to {addr[0]} ({name})',
            clock.get(),
        )
    )
    client_socket.send(problem.encode("utf-8"))

    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                log.write(
                    TimePrint(
                        f"Disconnected by {addr[0]} ({name})",
                        clock.get(),
                    )
                )
                break
            log.write(
                TimePrint(
                    f"Received from {addr[0]} ({name}) >> {data.decode('utf-8')}",
                    clock.get(),
                )
            )

            answer = exam.solve(problem)
            solved = data.decode("utf-8")
            result += int(str(solved))

            if answer == solved:
                log.write(
                    TimePrint(f"Correct {addr[0]} ({name})", clock.get())
                )
                problem = exam.problem()
            else:
                log.write(
                    TimePrint(
                        f"Incorrect {addr[0]} ({name})", clock.get()
                    )
                )
            log.write(
                TimePrint(
                    f'Send problem "{problem}" to {addr[0]} ({name})',
                    clock.get(),
                )
            )
            delay = random.randrange(1, 5)
            time.sleep(delay)
            client_socket.send(problem.encode())

        except ConnectionResetError as e:
            log.write(
                TimePrint(
                    f"Disconnected by {addr[0]} ({name})",
                    clock.get(),
                )
            )
            client_socket.close()
            break
        except ConnectionAbortedError as e:
            break


def server():
    log.write(TimePrint(f"Server start at {HOST}", clock.get()))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    log.write(TimePrint("Wait join client", clock.get()))
    print()
    log.write()
    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)
            client_thread = Thread(target=threaded, args=(client_socket, addr))
            client_thread.daemon = True
            client_thread.start()

    except Exception as e:
        log.write(TimePrint(f"Error: {e}", clock.get()))


def close():
    clock.stop()
    for client in client_sockets:
        client.close()
    log.write(TimePrint(f"Result: {result}", clock.get()))
    log.write(TimePrint("Server stopping...", clock.get()))
    log.save()
    os._exit(0)


def limit():
    while clock.get() < secondlimit:
        time.sleep(0.001)
    close()


clock.start()
t = Thread(target=limit)
t.daemon = True
t.start()
server()
close()
