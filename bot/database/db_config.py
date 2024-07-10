from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import DeclarativeBase

db_engine = create_engine('sqlite:///database.db')

class Base(DeclarativeBase):
    pass

class UsersDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    username = Column(Text, nullable=False)
    first_name = Column(Text)
    last_name = Column(Text)

class TasksDB(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    completion = Column(Text, default='False')
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Text, default='False')
    time = Column(Text, default='False')
    remind = Column(Text, default='False')

Base.metadata.create_all(bind=db_engine)



