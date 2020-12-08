from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

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
        return f'id={self.uid}, name={self.name}, age={self.age}, ' \
               f'birthday={self.birthday}, sex={self.sex}, edu={self.edu}, ' \
               f'create_on={self.create_on}, update_on={self.update_on}'


dburl="mysql+pymysql://root:123456@localhost:3306/jove_class?charset=utf8mb4"
engine=create_engine(dburl, echo=True, encoding="utf-8")

SessionClass = sessionmaker(bind=engine)
session = SessionClass()
# Base.metadata.create_all(engine)


student = Student_table(name='Jove',
                        age=18,
                        birthday=datetime(2002, 1, 1),
                        sex=True,
                        edu="本科",
                        )
# session.add(student)
result = session.query(Student_table).filter(Student_table.name=='Jove').all()
print(result)
session.commit()

# SELECT DISTINCT player_id, player_name, count(*) as num   # 5
# FROM player JOIN team ON player.team_id = team.team_id    # 1
# WHERE height > 1.80                                       # 2
# GROUP BY player.team_id                                   # 3
# HAVING num > 2                                            # 4
# ORDER BY num DESC                                         # 6
# LIMIT 2                                                   # 7


# create index id_name on student (id, name)

