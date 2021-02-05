"""
第三题，可视化数据
"""
import matplotlib
import pymysql
from matplotlib import pyplot as plt

db = pymysql.connect('localhost', 'root', '123456', 'jove_class')


def mysql_data(city):
    """提取数据到展示列表"""
    res = []
    cursor = db.cursor()
    SQLS = ["""SELECT count(1) FROM `lagou` WHERE salary < 5 and (%s)""",
            """SELECT count(1) FROM `lagou` WHERE (salary BETWEEN 5 and 10)  and city=(%s)""",
            """SELECT count(1) FROM `lagou` WHERE (salary BETWEEN 11 and 15) and city= (%s)""",
            """SELECT count(1) FROM `lagou` WHERE (salary BETWEEN 16 and 20) and city= (%s)""",
            """SELECT count(1) FROM `lagou` WHERE (salary BETWEEN 21 and 25) and city= (%s)""",
            """SELECT count(1) FROM `lagou` WHERE (salary BETWEEN 26 and 30) and city= (%s)"""]

    for SQL in SQLS:
        cursor.execute(SQL, city)
        res.append(cursor.fetchone()[0])
    return res


def run():
    """展示数据"""
    x = ['<5', '5-10', '11-15', '16-20', '21-25', '>25']
    plt.bar(x, mysql_data('北京'), color='blue', align='center')
    plt.bar(x, mysql_data('上海'), color='green', align='center')
    plt.bar(x, mysql_data('深圳'), color='yellow', align='center')
    plt.bar(x, mysql_data('广州'), color='orange', align='center')

    zhfont1 = matplotlib.font_manager.FontProperties(fname="SourceHanSansSC-Bold.otf")  # 可以使用中文
    plt.title("拉钩", fontproperties=zhfont1)
    plt.ylabel('数目', fontproperties=zhfont1)
    plt.xlabel('薪资', fontproperties=zhfont1)
    plt.show()


if __name__ == '__main__':
    run()
