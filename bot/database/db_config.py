from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

db_engine = create_engine('sqlite:///database.db')

class Base(DeclarativeBase):
    pass

class UsersDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)

class TasksDB(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    completion = Column(String, default='False')
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date = Column(String, default='False')
    time = Column(String, default='False')
    remind = Column(String, default='False')

Base.metadata.create_all(bind=db_engine)



