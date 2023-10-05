import threading
import random
import time


def send_thread(client_socket, problem):
    def send_with_delay():
        delay = random.uniform(0.1, 5.0)
        time.sleep(delay)
        client_socket.send(problem.encode())

    thread = threading.Thread(target=send_with_delay)
    thread.start()
    return thread
