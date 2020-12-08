### 1. 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。

- 将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交

  ```mysql
  alter database testdb character set utf8mb4;
  ```

- 将增加远程用户的 SQL 语句作为作业内容提交

  ```sql
  CREATE USER 'testroot'@'%' IDENTIFIED BY 'testpass';
  GRANT ALL PRIVILEGES ON testdb.* TO 'root' @'%';
  ```

### 2. 使用 sqlalchemy ORM 方式创建如下表，使用 PyMySQL 对该表写入 3 条测试数据，并读取:

- 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间

- 将 ORM、插入、查询语句作为作业内容提交

  ```python
  class Student_table(Base):
      __tablename__ = 'student'
  
      uid = Column(Integer(), primary_key=True, autoincrement=True)
      name = Column(String(15), nullable=True)
      age = Column(Integer(), nullable=False)
      birthday = Column(DateTime())
      sex = Column(Boolean(), nullable=False)
      edu = Column(Enum("中学", "专科","本科", "硕士", "博士"))
      create_on = Column(DateTime(), default=datetime.now)
      update_on = Column(DateTime(), default=datetime.now,
                         onupdate=datetime.now)
  
      def __repr__(self):
          return f'id={self.id}, name={self.name}, age={self.age}, ' \
                 f'birthday={self.birthday}, sex={self.sex}, edu={self.edu}, ' \
                 f'create_on={self.create_on}, update_on={self.update_on}'
  
  ```

  ```python
  student = Student_table(name='Jove',
                          age=18,
                          birthday=datetime(2002, 1, 1),
                          sex=True,
                          edu="本科",
                          )
  session.add(student)
  result = session.query(Student_table).filter(Student_table.name=='Jove').all()
  print(result)
  session.commit()
  ```

  ```python
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
  ```

  

### 3. 为以下 sql 语句标注执行顺序：


```sql
SELECT DISTINCT player_id, player_name, count(*) as num   # 5
FROM player JOIN team ON player.team_id = team.team_id    # 1
WHERE height > 1.80                                       # 2
GROUP BY player.team_id                                   # 3
HAVING num > 2                                            # 4
ORDER BY num DESC                                         # 6
LIMIT 2                                                   # 7
```



### 4. 以下两张基于 id 列，分别使用 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果是什么?

**Table1**

id name

1 table1_table2

2 table1

**Table2**

id name

1 table1_table2

3 table2

举例: INNER JOIN

```SQL
SELECT Table1.id, Table1.name, Table2.id, Table2.name
FROM Table1
INNER JOIN Table2
ON Table1.id = Table2.id;
```

| Table1.id | Table1.name   | Table2.id | Table2.name   |
| --------- | ------------- | --------- | ------------- |
| 1         | table1_table2 | 1         | table1_table2 |

| Table1.id | Table1.name   | Table2.id | Table2.name   |
| --------- | ------------- | --------- | ------------- |
| 1         | table1_table2 | 1         | table1_table2 |
| 2         | table1        | None      | None          |

| Table1.id | Table1.name   | Table2.id | Table2.name   |
| --------- | ------------- | --------- | ------------- |
| 1         | table1_table2 | 1         | table1_table2 |
| None      | None          | 3         | table2        |

### 5. 使用 MySQL 官方文档，学习通过 sql 语句为上题中的 id 和 name 增加索引，并验证。根据执行时间，增加索引以后是否查询速度会增加？请论述原因，并思考什么样的场景下增加索引才有效。

```txt
会增加，索引通过 B+ 树类似于二分查找法，所以在命中索引时会很快。
比较频繁的作为查询字段、唯一性较高、更新不频繁的，应该建立索引。
```

### 6. 张三给李四通过网银转账 100 极客币，现有数据库中三张表：

一张为用户表，包含用户 ID 和用户名字，另一张为用户资产表，包含用户 ID 用户总资产，
第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。

- 请合理设计三张表的字段类型和表结构；
```python
class User_table(Base):
    __tablename__ = 'user'
    uid = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(15), nullable=True, unique=True)

class Asset_table(Base):
    __tablename__ = 'asset'
    uid = Column(Integer(), primary_key=True, nullable=True)
    asset = Column(DECIMAL(19, 4), nullable=True)

class Record_tabl(Base):
    __tablename__ = 'record'
    one_id = Column(Integer(), primary_key=True)
    other_id = Column(Integer(), primary_key=True)
    deal = Column(DECIMAL(19, 4), nullable=True)
    create_date = Column(DateTime(), nullable=True)
```
- 请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。

  ```python
  def deal(one, other, deal, session):
      # 获取转账者 ID
      one_id = session.query(User_table.uid).filter(User_table.name == one).one()[0]
      # 被转账者 ID
      other_id = session.query(User_table.uid).filter(User_table.name == other).one()[0]
      # 转账者账户余额
      one_mon = session.query(Asset_table.asset).filter(Asset_table.uid==one_id, Asset_table.asset>deal).one()[0]
      # 被转账者账户余额
      other_mon = session.query(Asset_table.asset).filter(Asset_table.uid==other_id).one()[0]
  
      one_mon -= deal
      other_mon += deal
      # 更新双方余额
      session.query(Asset_table.asset).filter(Asset_table.uid==one_id).update({Asset_table.asset: one_mon})
      session.query(Asset_table.asset).filter(Asset_table.uid == other_id).update({Asset_table.asset: other_mon})
      
      # 添加账单
      record = Record_tabl(one_id=one_id,
                           other_id=other_id,
                           create_date=datetime.now(),
                           deal=deal)
      session.add(record)
  ```

  
