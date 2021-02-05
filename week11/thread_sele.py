"""
第二题，selenium 多线程爬取拉钩，并存入数据库
"""
import re
import time
from multiprocessing import Process
from random import choice

import pymysql
from bs4 import BeautifulSoup
from pymysql.err import IntegrityError
from selenium import webdriver

PROXY = ["58.220.95.86:9401", "220.174.236.211:8091", "221.182.31.54:8080", "183.220.145.3:80", ]
WEBDRIVER_PATH = r"chromedriver.exe"


class Lagou(Process):
    def __init__(self, url, city):
        super().__init__()
        self.city = city
        self.url = url
        self.chrome_option = webdriver.ChromeOptions()
        self.chrome_option.add_argument('--proxy-server={0}'.format(choice(PROXY)))
        self.chrome_option.add_argument("disable-blink-features=AutomationControlled")
        self.db = pymysql.connect('localhost', 'root', '123456', 'jove_class')

    def run(self):
        """由于 webdriver 不可序列化故放在 run 里面进行初始化"""
        self.browser = webdriver.Chrome(executable_path=WEBDRIVER_PATH, chrome_options=self.chrome_option)
        with open("stealth.min.js", "r", encoding="utf-8") as f:
            js_code = f.read()
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js_code
        })
        self.browser.get(self.url)
        self.crawl()
        self.browser.close()

    def parse(self, html):
        result = []
        soup = BeautifulSoup(html, 'lxml')
        itemlist = soup.select("li[class='con_list_item default_list']")
        for item in itemlist:
            salary = item.attrs['data-salary']
            salary = re.match(r'(\d*)k-(\d*)k', salary)
            salary = int(salary.group(1)) + int(salary.group(2))  # 提起平均薪资

            position = item.attrs['data-positionname'].title()
            company = item.attrs['data-company']
            unique = hash(self.city + position + salary)  # 额外添加一个由城市、职位和薪资组成的哈希值的唯一索引

            result.append([salary >> 1, position, company, unique, self.city])

        self.storage_data(result)

    def storage_data(self, data):
        """存储到 MySQL，额外添加一个由城市、职位和薪资组成的哈希值的唯一索引，当有重复值时捕获唯一异常跳过"""
        print(data)
        cursor = self.db.cursor()
        sql = """INSERT INTO `lagou` (`salary`, `position`, `company`, `unique`, `city`) VALUES (%s, %s, %s, %s, %s)"""
        for _ in data:
            try:
                cursor.execute(sql, data)
                self.db.commit()
            except IntegrityError:
                pass

    def crawl(self):
        """爬虫逻辑"""
        self.browser.switch_to.window(self.browser.current_window_handle)

        for _ in range(7):
            html = self.browser.page_source
            self.parse(html)
            self.cancel_hongbao()
            search_button = self.browser.find_element_by_css_selector('.next')
            search_button.click()
            time.sleep(20)

    def cancel_hongbao(self):
        """取消开始屏幕红包弹窗"""
        self.browser.execute_script("""$('div[class="body-container showData"]').remove()""")


if __name__ == '__main__':
    p = Lagou("https://www.lagou.com/jobs/list_Python/p-city_2?px=default#filterBox", '北京')
    p2 = Lagou("https://www.lagou.com/jobs/list_Python/p-city_3?px=default#filterBox", '上海')
    p3 = Lagou("https://www.lagou.com/jobs/list_Python/p-city_215?px=default#filterBox", '深圳')
    p4 = Lagou("https://www.lagou.com/jobs/list_Python/p-city_213?px=default#filterBox", '广州')

    p.start()
    p2.start()
    p3.start()
    p4.start()

    p.join()
    p2.join()
    p3.join()
    p4.join()
