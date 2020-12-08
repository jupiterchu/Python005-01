from datetime import datetime

import pymysql

db = pymysql.connect('localhost', 'root', '123456', 'jove_class')

def insert_many():
    SQL = """INSERT INTO student (name, age, birthday, sex, edu, create_on, update_on)
    values (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        ('Peter', '22', datetime(1998,1,1), 1, '本科', datetime.now(), datetime.now()),
        ('Mary', '27', datetime(1993, 1, 1), 0, '硕士', datetime.now(), datetime.now()),
        ('Sor', '35', datetime(1985, 1, 1), 0, '博士', datetime.now(), datetime.now())
    )
    with db.cursor() as cursor:
        cursor.executemany(SQL, values)
    db.commit()

def read():
    SQL = """SELECT * FROM student WHERE name=%s"""
    with db.cursor() as cursor:
        cursor.execute(SQL, 'Peter')
        result = cursor.fetchall()
        print(result)
    db.commit()

if __name__ == '__main__':
    # insert_many()
    read()