import time


def TimePrint(msg):
    now = time.ctime()
    msg = f"[{now}]{msg}"
    print(msg)
