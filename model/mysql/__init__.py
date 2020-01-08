from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String, DATETIME, Text, ForeignKey, Index, Table, and_, or_, func
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from conf import conf
from util.datetime import now

engine = create_engine(
    conf.mysql.url,
    max_overflow=30,  # 超过连接池大小外最多创建的连接
    pool_size=10,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=1200, # 多久之后对线程池中的线程进行一次连接的回收（重置）
    pool_pre_ping=True,
    # echo=True  # 显示执行的所有SQL语句
)
Session = sessionmaker(bind=engine)
Base = declarative_base()  # 声明基类


class BaseModel(Base):
    __abstract__ = True  # 定义BaseModel为抽象类
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DATETIME, nullable=False, default=now)
    updated_at = Column(DATETIME, default=None)
    deleted_at = Column(DATETIME, default=None)

    def __str__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.id)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


@contextmanager
def session_cxt():
    s = Session()
    try:
        yield s
        s.commit()
    except Exception as ex:
        s.rollback()
        print(ex)  # todo: 日志，输出详细sql错误
    finally:
        s.expunge_all()
        s.close()
