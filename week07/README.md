**作业一：**

区分以下类型哪些是容器序列哪些是扁平序列，哪些是可变序列哪些是不可变序列：

- list
- tuple
- str
- dict
- collections.deque

```tex
扁平序列: str
可变序列: list, dict, collections.deque
不可变序列: tuple, str   
```

**作业二：**
自定义一个 python 函数，实现 map() 函数的功能。

```python
def my_map(func, *iterables):
    """
    :param func:
    :param iterables:
    :return:
    """
    m = len(iterables)
    try:
        n = len(iterables[0])
    except TypeError as e:
        raise TypeError('please input iterables')
    for i in range(n):
        args = []
        for j in range(m):
            args.append(iterables[j][i])
        yield func(*args)

        
##################################   
def my_map2(func, *iterables):
    """
	采用 yield from 更加简洁, 但是这个句法是历史遗留不推荐
    :param func:
    :param iterables:
    :return:
    """
    for iterable in iterables:
        yield from func(iterable)     
```

**作业三：**
实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。

```python
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

```