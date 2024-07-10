import sqlite3
import typing

from sqlalchemy import and_
from sqlalchemy.orm import Session

from bot.database.db_config import db_engine, UsersDB, TasksDB
from config import DB_PATH


def db_check_user(telegram_id: int, username: str, first_name: str, last_name: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        result = session.query(UsersDB).filter(UsersDB.telegram_id == telegram_id).first()
        if result == None:
            new_user = UsersDB(telegram_id=telegram_id,
                               username=username,
                               first_name=first_name,
                               last_name=last_name)
            session.add(new_user)
            session.commit()

def db_check_title_in_tasks(telegram_id: int, title: str) -> bool:
    with Session(autoflush=True, bind=db_engine) as session:
        result = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        if result == None:
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
        except Exception as e:
            print(e)
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

def db_get_tasks(telegram_id: int) -> typing.List[TasksDB]:
    with Session(autoflush=True, bind=db_engine) as session:
        tasks = session.query(TasksDB).filter(TasksDB.telegram_id == telegram_id).all()
        return tasks

def db_get_task(telegram_id: int, title: str) -> list:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM Tasks WHERE telegram_id = {telegram_id} AND title = '{title}'")
    task = cur.fetchone()
    con.commit()
    con.close()
    return task

def db_get_count_task(telegram_id: int) -> int:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM Tasks WHERE telegram_id = {telegram_id}")
    count_tasks = len(cur.fetchall())
    con.commit()
    con.close()
    return count_tasks

def get_all_tasks() -> list:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM Tasks WHERE remind = 'True'")
    result = cur.fetchall()
    con.commit()
    con.close()
    return result

def completed_remind(telegram_id: int, title: str) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"UPDATE Tasks SET remind = 'Completed' WHERE telegram_id = '{telegram_id}' AND title = '{title}'")
    con.commit()
    con.close()

def set_complete(telegram_id: int, title: str, completion: str) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"UPDATE Tasks SET completion = '{completion}' WHERE telegram_id = '{telegram_id}' AND title = '{title}'")
    con.commit()
    con.close()