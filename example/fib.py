def fib(num):
    if num == 0:
        return 0
    elif num == 1 or num == 2:
        return 1
    else:
        return fib(num - 1) + fib(num - 2)
