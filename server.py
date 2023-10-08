import socket
from _thread import *
import exam
from log import *
import time
from clock import Clock
import random
from threading import Thread
import sys

client_sockets = []

minuteLimit = 1
secondlimit = minuteLimit * 60

secondlimit = 10

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

clock = Clock()
log = Log("Server.txt")


def client_name(client_socket):
    return f"Client{client_sockets.index(client_socket)+1}"


def addrToStr(addr):
    return f"{addr[0]}"


def threaded(client_socket, addr):
    name = client_name(client_socket)
    log.write(
        TimePrint(
            f"Connected by {addrToStr(addr)} ({name})",
            clock.get_clock(),
        )
    )
    client_socket.send(f"Name: {name}".encode())

    problem = exam.problem()
    log.write(
        TimePrint(
            f'Send problem "{problem}" to {addrToStr(addr)} ({name})',
            clock.get_clock(),
        )
    )
    client_socket.send(problem.encode("utf-8"))

    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                log.write(
                    TimePrint(
                        f"Disconnected by {addrToStr(addr)} ({name})",
                        clock.get_clock(),
                    )
                )
                break
            log.write(
                TimePrint(
                    f"Received from {addrToStr(addr)} ({name}) >> {data.decode('utf-8')}",
                    clock.get_clock(),
                )
            )

            answer = exam.solve(problem)
            solved = data.decode("utf-8")

            if answer == solved:
                log.write(
                    TimePrint(f"Correct {addrToStr(addr)} ({name})", clock.get_clock())
                )
                problem = exam.problem()
            else:
                log.write(
                    TimePrint(
                        f"Incorrect {addrToStr(addr)} ({name})", clock.get_clock()
                    )
                )
            log.write(
                TimePrint(
                    f'Send problem "{problem}" to {addrToStr(addr)} ({name})',
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
                    f"Disconnected by {addrToStr(addr)} ({name})",
                    clock.get_clock(),
                )
            )
            break
        except Exception as e:
            client_socket.close()
            pass


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
            client_thread = Thread(target=threaded, args=(client_socket, addr))
            client_thread.daemon = True
            client_thread.start()
            # start_new_thread(threaded, (client_socket, addr))
        close()

    except Exception as e:
        log.write(TimePrint(f"Error: {e}", clock.get_clock()))


def close():
    for client in client_sockets:
        client.close()
    log.write(TimePrint("Server stopping...", clock.get_clock()))
    log.save()
    sys.exit()


def limit():
    while clock.get_clock() <= secondlimit:
        time.sleep(0.001)
    close()


clock.start_clock()
t = Thread(target=limit)
t.daemon = True
t.start()
server()
close()
