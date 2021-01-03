import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(func.__name__, f"执行了{time.time() - start}s")
        return res
    return wrapper

@timer
def foo(x):
    return x


if __name__ == '__main__':
    foo(1)
