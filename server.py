import socket
from _thread import *
import exam
from log import TimePrint

client_sockets = []


HOST = "127.0.0.1"
PORT = 9999


def addrToStr(addr):
    return f"{addr[0]}:{addr[1]}"


def threaded(client_socket, addr):
    # TODO: 서버에서 보낸 문제와 클라이언트가 받은 문제가 다름

    TimePrint(f"Connected by {addrToStr(addr)}")
    problem = exam.problem()
    TimePrint(f'Send problem "{problem}" to {addrToStr(addr)}')
    client_socket.send(exam.problem().encode("utf-8"))

    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                TimePrint(f"Disconnected by {addrToStr(addr)}")
                break
            TimePrint(f"Received from {addrToStr(addr)} >> {data.decode('utf-8')}")

            answer = exam.solve(problem)
            solved = data.decode("utf-8")
            TimePrint(f"{problem}={answer}")
            if answer == solved:
                TimePrint(f"{answer} == {solved}")
            else:
                TimePrint(f"{answer} != {solved}")

            for client in client_sockets:
                if client != client_socket:
                    client.send(data)

        except ConnectionResetError as e:
            TimePrint(f"Disconnected by {addrToStr(addr)}")
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        TimePrint(f"Remove client list: {len(client_sockets)}")

    client_socket.close()


def server():
    TimePrint("Server start")
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


server()
