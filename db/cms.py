import datetime
from sqlalchemy import create_engine  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime, Boolean
from sqlalchemy.orm import sessionmaker,scoped_session

# DBSTR = 'sqlite:///:memory:'
DBSTR = 'sqlite:///mydata.db'
Base = declarative_base()

def db_init():
    engine = create_engine(DBSTR, echo=True)
    Base.metadata.create_all(engine)

def get_session():
    engine = create_engine(DBSTR, echo=True)
    Session = sessionmaker(bind=engine)
    # return Session()
    return scoped_session(Session)

ses = get_session()

class Level(Base):
    __tablename__ = 'levels'
    id = Column(Integer, Sequence('level_id_seq'), primary_key=True) 
    name = Column(String(20))
    r = Column(Integer,unique=True,nullable=False)
    c = Column(Integer,nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True) 
    name = Column(String(20),unique=True)
    password = Column(String(256))
    user_type = Column(Integer,default=1)
    power = Column(String)
    ##列表转换为字符串保存,以,分隔

class News(Base):
    __tablename__ = 'newses'
    id = Column(Integer, Sequence('news_id_seq'), primary_key=True) 
    title = Column(String(200),nullable=False)
    txt = Column(Text,nullable=False)
    author = Column(String(20))
    category = Column(Integer)
    releaser = Column(Integer)
    release_date = Column(DateTime,default=datetime.datetime.now())
    is_released = Column(Boolean,default=True)


class OrdUser(Base):
    __tablename__ = "orduser"
    id = Column(Integer, Sequence('orduser_id_seq'), primary_key=True) 
    name = Column(String(20),nullable=False)
    password = Column(String(256))