import typing

from sqlalchemy import create_engine, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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

ALL_TIME_ZONE = {
    'UTC': 'UTC+0',
    'KALT': 'KALT+2',
    'MSK': 'MSK+3',
    'SAMT': 'SAMT+4',
    'YEKT': 'YEKT+5',
    'OMST': 'OMST+6',
    'KRAT': 'KRAT+7',
    'IRKT': 'IRKT+8',
    'YAKT': 'YAKT+9',
    'VLAT': 'VLAT+10',
    'MAGT': 'MAGT+11',
    'PETT': 'PETT+12'
}


class UsersDB(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[typing.Optional[str]]
    last_name: Mapped[typing.Optional[str]]
    timezone: Mapped[str] = mapped_column(String, default=ALL_TIME_ZONE['UTC'])

class TasksDB(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer,
                                             ForeignKey('users.telegram_id',
                                                        ondelete='CASCADE',
                                                        onupdate='CASCADE'),
                                             nullable=False)
    completion: Mapped[str] = mapped_column(String, default=CompletionColumn.not_completed)
    title: Mapped[str] = mapped_column(String(length=15), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(length=3500), nullable=False)
    datetime: Mapped[str] = mapped_column(String, nullable=False)
    remind: Mapped[str] = mapped_column(String, default=RemindColumn.not_remind)
