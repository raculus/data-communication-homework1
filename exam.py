import random


def RandomOperator():
    num = random.randrange(0, 3)
    if num == 0:
        return "+"
    elif num == 1:
        return "-"
    elif num == 2:
        return "*"
    else:
        return "/"


def solve(problem):
    """
    문제 풀이
    """
    try:
        result = eval(problem)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def problem(numCount=3):
    """
    랜덤 문제 문자열 출력
    예시: 1+2-3
    """
    if numCount < 2:
        numCount = 2

    numList = [random.randrange(1, 100) for _ in range(numCount)]
    operatorList = [RandomOperator() for _ in range(numCount - 1)]
    return "".join(f"{numList[i]}{operatorList[i]}" for i in range(numCount - 1)) + str(
        numList[-1]
    )
