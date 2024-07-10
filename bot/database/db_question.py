import sqlite3
import typing

from sqlalchemy import and_
from sqlalchemy.orm import Session

from bot.database.db_config import db_engine, UsersDB, TasksDB
from config import DB_PATH


def db_check_user(telegram_id: int, username: str, first_name: str, last_name: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        result = session.query(UsersDB).filter(and_(UsersDB.telegram_id == telegram_id)).first()
        if result is None:
            new_user = UsersDB(telegram_id=telegram_id,
                               username=username,
                               first_name=first_name,
                               last_name=last_name)
            session.add(new_user)
            session.commit()

def db_check_title_in_tasks(telegram_id: int, title: str) -> bool:
    with Session(autoflush=True, bind=db_engine) as session:
        result = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        if result is None:
            return False
        else:
            return True

def db_set_task(telegram_id: int, title: str, description: str, date: str, time: str, remind: str) -> bool:
    with Session(autoflush=True, bind=db_engine) as session:
        try:
            task = TasksDB(telegram_id=telegram_id,
                           title=title,
                           description=description,
                           date=date,
                           time=time,
                           remind=remind)
            session.add(task)
            session.commit()
            return True
        except:
            return False

def db_edit_reminder(telegram_id: int, title: str, date: str, time: str, remind: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        task.date = date
        task.time = time
        task.remind = remind
        session.commit()

def db_edit_title(telegram_id: int, title: str, new_title: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        task.title = new_title
        session.commit()

def db_edit_description(telegram_id: int, title: str, new_description: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        task.description = new_description
        session.commit()

def db_delete_task(telegram_id: int, title: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        session.delete(task)
        session.commit()

def db_get_tasks_by_id(telegram_id: int) -> typing.List[typing.Type[TasksDB]]:
    with Session(autoflush=True, bind=db_engine) as session:
        tasks = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id)).all()
        return tasks

def db_get_task(telegram_id: int, title: str) -> typing.Optional[TasksDB]:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        return task

def db_get_count_task(telegram_id: int) -> int:
    with Session(autoflush=True, bind=db_engine) as session:
        count = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id)).count()
        return count

def get_all_tasks() -> typing.List[typing.Type[TasksDB]]:
    with Session(autoflush=True, bind=db_engine) as session:
        tasks = session.query(TasksDB).filter(and_(TasksDB.remind == 'True')).all()
        return tasks

def completed_remind(telegram_id: int, title: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        task.remind = 'Completed'
        session.commit()

def set_complete(telegram_id: int, title: str, completion: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        task.complete = completion
        session.commit()