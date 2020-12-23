**作业一：**使用 Python+redis 实现高并发的计数器功能
**需求描述:**
在社交类网站中，经常需要对文章、视频等元素进行计数统计功能，热点文章和视频多为高并发请求，因此采用 redis 做为文章阅读、视频播放的计数器。
请实现以下函数：


```python
def detail(request, mid, title):
	"""结合上次作业，展示访问人数"""
    movie = Movies.objects.filter(stars__gte=3, name=title).all()
    if len(movie):
        data = movie
    else:
        _crawl_movies(mid, title)
        data =  Movies.objects.filter(stars__gte=3, name=title).all()

    num = counter(mid)
    conn = get_redis_connection()
    if num is None:
        conn.set(mid, 1)
        num = 1 # 初始化为 1
    else:
        conn.incr(mid)
        num = int(num) + 1 # 当前访问算上
    return render(request, 'detail.html', locals())

def counter(hotspot_id: int):
    cache = get_redis_connection()
    counter_number = cache.get(hotspot_id)
    return counter_number
```

![image-20201221233606343](https://github.com/jupiterchu/Python005-01/blob/main/week05/%E5%9B%BE%E7%89%87/1.png)

**作业二：**在使用短信群发业务时，公司的短信接口限制接收短信的手机号，每分钟最多发送五次，请基于 Python 和 redis 实现如下的短信发送接口：
已知有如下函数：

```python
	def sendsms(telephone_number: int, content: string, key=None)：
    # 短信发送逻辑, 作业中可以使用 print 来代替
    pass
    # 请实现每分钟相同手机号最多发送五次功能, 超过 5 次提示调用方,1 分钟后重试稍后
    pass
    print("发送成功")
```

**选做：**
1.content 为短信内容，超过 70 个字自动拆分成两条发送
2.为 sendsms() 函数增加装饰器 send_times()，通过装饰器方式实现限制手机号最多发送次数

```python
r = fakeredis.FakeStrictRedis() # 测试 Redis

def send_times(times):
    def decorate(func):
        @wraps(func)
        def wrapper(telephone_number, content, times=5, key=None):
            con_len = len(content)
            if con_len < 70:
                if r.llen(telephone_number) < times:
                    func(telephone_number, content) # send
                elif dump(telephone_number, times, True): # 倾倒一次
                    func(telephone_number, content) 
                else:
                    print('操作频繁，1 分钟后重试')

            else:
                if r.llen(telephone_number) < times-1:
                    func(telephone_number, content[:con_len >> 2])
                    func(telephone_number, content[con_len >> 2:])

                elif dump(telephone_number, times) and \ # 尝试倾倒两次
                        dump(telephone_number, times - 1):
                    
                    func(telephone_number, content[:con_len >> 2])
                    func(telephone_number, content[con_len >> 2:])
                else:
                    print('超过70字符，剩余次数不足，稍后再试！')
        return wrapper
    return decorate


def dump(telephone_number, limit, wait=5):
    """尝试发送，并维护数组长度节约内存"""
    head = r.lrange(telephone_number, -limit, -limit) # 队头发送时间
    head = float(last[0].decode())
    now = time()
  
    if now - last >= wait:
        r.rpop(telephone_number)
        return True
    return False


@send_times(times=5)
def sendsms(telephone_number, content, key=None):
    r.rpush(telephone_number, time())
    print('发送成功')
```

**作业三：**请用自己的语言描述如下问题：

- 在你目前的工作场景中，哪个业务适合使用 rabbitmq？ 引入 rabbitmq 主要解决什么问题?（非相关工作可以以设计淘宝购物和结账功能为例来描述）

  ```txt
  用户在淘宝购买支付后，可以不必等待后台操作完成后再得到提示。
  rabbitmq 可以将后续流程分发到不同的队列对应的不同处理模块，使购物车清除、订单生成、收款确认等业务异步执行。
  ```

  

- 如何避免消息重复投递或重复消费？

  ```txt
  可以借鉴三次握手，消费者在接受后回 SYN + seq 给生产者，生产者收到后也返回一个 ACK，消费者收到后再返回一个 ACk，
  然后生产者收到后将消息删除。
  假如消息有唯一标识，消费者在处理前，先到数据库中查看是否有相同标识，没有再处理，反之忽略。
  ```

- 交换机 fanout、direct、topic 有什么区别？

  ```txt
  fanout: 没有匹配模式，直接将消息分发到所有连接的队列
  direct: 精确匹配模式，只将消息分发到对应名称的队列中
  topic:  模糊匹配模式，在 direct 的基础上支持模糊匹配
  ```

- 架构中引入消息队列是否利大于弊？你认为消息队列有哪些缺点？

  ```python
  如老师所说：没有最好的架构只有最合适的。
  引入消息队列固然可以提升整个服务的对消息处理的能力，但是过早的优化不如不优化。当能够驾驭消息队列特性带来的架构复杂化，应该引入。
  增加一层就增加一丝数据不一致的风险，同时对数据的写入效率有影响，增加了复杂度可能难以维护。
  ```

