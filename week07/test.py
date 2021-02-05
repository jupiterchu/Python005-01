import aiohttp
import asyncio

url = 'http://httpbin.org/get'

async def fetch(client, url):
    # get 方式请求url
    async with client.get(url) as resp:
        assert resp.status == 200
        return await resp.text()

async def main():
    # 获取session对象
    async with aiohttp.ClientSession() as client:
        html = await fetch(client, url)
        print(html)

if __name__ == '__main__':
    asyncio.new_event_loop()
    loop = asyncio.get_event_loop()
    # loop = asyncio.get_event_loop() # 创建事件循环
    task = loop.create_task(main()) # 创建任务
    loop.run_until_complete(task) # 开始所有任务
    # Zero-sleep 让底层连接得到关闭的缓冲时间
    loop.run_until_complete(asyncio.sleep(0))
    loop.close()