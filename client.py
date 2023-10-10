import socket
from _thread import *
from exam import solve
from log import *
import sys
import random
import time

HOST = "10.100.133.211"
if(len(sys.argv) == 2):
    HOST = sys.argv[1]
PORT = 9999

arg = sys.argv
if len(arg) == 2:
    HOST = arg[1]
elif len(arg) == 3:
    HOST = arg[1]
    PORT = arg[2]


printList = []

p = TimePrint(f"Try connection to {HOST}:{PORT}")
printList.append(p)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

p = TimePrint(f"Connected server to {HOST}")
p = ""
printList.append(p)
name: str
log: Log


def recv_data(client_socket):
    global log
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            if str(data).__contains__("Name:"):
                p = TimePrint(f"Recived >> {data}")
                printList.append(p)
                name = data.split(": ")[1]
                log = Log(name + ".txt")
                for p in printList:
                    log.write(p)
                printList.clear()
                print()
                log.write()
            else:
                log.write(TimePrint(f"Recived >> {data}"))
                solved = solve(data)
                delay = random.randrange(1, 5)
                time.sleep(delay)
                client_socket.send(solved.encode())
                log.write(TimePrint(f"Solved >> {solved}"))
                print()
                log.write()
        except Exception as e:
            client_socket.close()
            break


recv_data(client_socket)
log.write(TimePrint(f"Server stopped"))
log.save()
exit()
