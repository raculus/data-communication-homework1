import datetime


def TimePrint(msg, upTime=-1):
    """
    출력 예시: [2023-09-26 22:26:12 001s]msg or [2023-09-26 22:26:12]msg
    """
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    if upTime >= 0:
        msg = f"[{now} {upTime:03d}s]{msg}"
    else:
        msg = f"[{now}]{msg}"
    print(msg)
    return msg


class Log:
    def __init__(self, filename):
        self.f = open(filename, "w")

    def write(self, txt=""):
        self.f.write(txt)
        self.f.write("\n")

    def save(self):
        self.f.close
