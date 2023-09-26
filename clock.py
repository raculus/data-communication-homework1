import threading
import time


class Clock:
    def __init__(self):
        self.clock = 0
        self.clock_thread = threading.Thread(target=self.update_clock)
        self.clock_thread.daemon = True
        self.running = False

    def update_clock(self):
        while self.running:
            self.clock += 1
            time.sleep(1)

    def increment_clock(self, second):
        self.clock += second

    def start_clock(self):
        if not self.running:
            self.running = True
            self.clock_thread.start()

    def stop_clock(self):
        if self.running:
            self.running = False
            self.clock_thread.join()

    def get_clock(self):
        return self.clock
