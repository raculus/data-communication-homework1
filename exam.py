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
    try:
        result = eval(problem)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def problem():
    numList = [random.randrange(1, 100) for _ in range(3)]
    operatorList = [RandomOperator() for _ in range(2)]
    return f"{numList[0]}{operatorList[0]}{numList[1]}{operatorList[1]}{numList[2]}"


p = problem()
s = solve(p)
print(p)
print("= " + s)
