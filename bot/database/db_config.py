from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import DeclarativeBase

from config import DB_PATH

db_engine = create_engine(f'sqlite:///{DB_PATH}')

class Base(DeclarativeBase):
    pass

class CompletionColumn:
    not_completed = 'not_completed'
    completed = 'completed'

class RemindColumn:
    not_remind = 'not_remind'
    remind = 'remind'
    reminder_completed = 'reminder_completed'

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
    completion = Column(Text, default=CompletionColumn.not_completed)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Text, default='False')
    time = Column(Text, default='False')
    remind = Column(Text, default=RemindColumn.not_remind)

Base.metadata.create_all(bind=db_engine)



