import time


def TimePrint(msg):
    """
    출력 예시: [Sat Sep 23 17:50:36 2023]msg
    """
    now = time.ctime()
    msg = f"[{now}]{msg}"
    print(msg)
