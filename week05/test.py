import fakeredis
import redis  # 导入redis 模块
import time

client  = fakeredis.FakeStrictRedis()

WAIT_TIME = 60 #等待时间，测试设置为60秒
def sendsms(telephone_number: int, content: str, key=None, wait_time=WAIT_TIME):
    # 短信发送逻辑, 作业中可以使用 print 来代替
    # pass
    # 请实现每分钟相同手机号最多发送五次功能, 超过 5 次提示调用方,1 分钟后重试稍后
    if len(client.keys("%s_*" % telephone_number)) > 5:
        print('1 分钟后重试稍后')
        return

    currentTime = int(time.time())
    client.setex("%s_%s" % (telephone_number, currentTime), wait_time, currentTime)

    print("发送成功:", content)


if __name__ == '__main__':
    for i in range(6):
        sendsms(123, 'hello 123')
    time.sleep(5)
    sendsms(123,'hello 123')
