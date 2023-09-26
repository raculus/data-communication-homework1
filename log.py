import time


def TimePrint(msg):
    """
    출력 예시: [Sat Sep 23 17:50:36 2023]msg
    """
    now = time.ctime()
    msg = f"[{now}]{msg}"
    print(msg)


class Log:
    def __init__(self, filename):
        self.f = open(filename, "w")

    def write(self, txt):
        self.f.write(txt)
        self.f.write("\n")

    def save(self):
        self.f.close
