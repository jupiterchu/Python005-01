def my_map(func, *iterables):
    """

    :param func:
    :param iterables:
    :return:
    """
    for iterable in iterables:
        yield from func(iterable)


def my_map2(func, *iterables):
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



def foo(x):
    return x

def mm(x):
    for i in x:
        print(i)


if __name__ == '__main__':
    b = my_map(foo, (1,2, [1,2,3]))
    a = map(foo, (1, 3))
    mm(a)
    mm(b)

