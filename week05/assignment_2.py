from functools import wraps
from threading import Thread
from time import sleep, time

import fakeredis

r = fakeredis.FakeStrictRedis()


def send_times(times):
    def decorate(func):
        @wraps(func)
        def wrapper(telephone_number, content, times=5, key=None):
            con_len = len(content)
            if con_len < 70:
                if r.llen(telephone_number) < times:
                    func(telephone_number, content)
                elif dump(telephone_number, times, True):
                    func(telephone_number, content)
                else:
                    print('操作频繁，1 分钟后重试')

            else:
                if r.llen(telephone_number) < times-1:
                    func(telephone_number, content[:con_len>>2])
                    func(telephone_number, content[con_len>>2:])

                elif dump(telephone_number, times, True) and \
                        dump(telephone_number, times, True):
                    func(telephone_number, content[:con_len >> 2])
                    func(telephone_number, content[con_len >> 2:])
                else:
                    print('超过70字符，剩余次数不足，稍后再试！')
        return wrapper
    return decorate

@send_times(times=5)
def sendsms2(telephone_number, content, key=None):
    r.rpush(telephone_number, time())
    print('发送成功')


def dump(telephone_number, limit,  double=False, wait=5):
    last = r.lrange(telephone_number, -limit, -limit)
    last = float(last[0].decode())
    now = time()

    if now - last >= wait:
        r.rpop(telephone_number)
        return True
    return False

if __name__ == '__main__':
    for i in range(6):
        sendsms2(123, 'hello 123')
    sleep(5)
    sendsms2(123,'hello 123')

