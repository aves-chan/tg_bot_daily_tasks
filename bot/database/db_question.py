import typing
import datetime

from sqlalchemy import and_, update
from sqlalchemy.orm import Session

from bot.database.db_config import db_engine, UsersDB, TasksDB, CompletionColumn, RemindColumn

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

def db_set_task(telegram_id: int, title: str, description: str, date_time: datetime.datetime, remind: str) -> bool:
    with Session(autoflush=True, bind=db_engine) as session:
        try:
            task = TasksDB(telegram_id=telegram_id,
                           title=title,
                           description=description,
                           datetime=str(date_time),
                           remind=remind)
            session.add(task)
            session.commit()
            return True
        except:
            return False

def db_set_complete(telegram_id: int, title: str, completion: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        task.completion = completion
        session.commit()

def db_set_completed_remind(telegram_id: int, title: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        task.remind = CompletionColumn.completed
        session.commit()

def db_edit_timezone(telegram_id: int, timezone: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        session.execute(update(UsersDB).where(and_(UsersDB.telegram_id == telegram_id)).values(timezone=timezone))
        session.commit()

def db_edit_reminder(telegram_id: int, title: str, remind: str, date_time: typing.Union[datetime.datetime, RemindColumn.not_remind]) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        task.datetime = str(date_time)
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

def db_get_tasks_by_id(telegram_id: int) -> typing.List[typing.Type[TasksDB]]:
    with Session(autoflush=True, bind=db_engine) as session:
        tasks = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id)).all()
        return tasks

def db_get_task(telegram_id: int, title: str) -> typing.Tuple[typing.Optional[TasksDB], str, int]:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        user = session.query(UsersDB).filter(and_(UsersDB.telegram_id == telegram_id)).first()

        timezone, timedelta = get_timezone_and_timedelta(user)

        return task, timezone, timedelta

def db_get_user(telegram_id: int) -> typing.Optional[UsersDB]:
    with Session(autoflush=True, bind=db_engine) as session:
        user = session.query(UsersDB).filter(and_(UsersDB.telegram_id == telegram_id)).first()
        return user

def db_get_all_tasks_for_remind() -> typing.List[typing.Type[TasksDB]]:
    with Session(autoflush=True, bind=db_engine) as session:
        tasks = session.query(TasksDB).filter(and_(TasksDB.remind == RemindColumn.remind)).all()
        return tasks

def db_delete_task(telegram_id: int, title: str) -> None:
    with Session(autoflush=True, bind=db_engine) as session:
        task = session.query(TasksDB).filter(and_(TasksDB.telegram_id == telegram_id, TasksDB.title == title)).first()
        session.delete(task)
        session.commit()

def get_timezone_and_timedelta(user: UsersDB) -> typing.Tuple[str, int]:
    sign = 1 if '+' in user.timezone else -1
    result = user.timezone.split('+') if sign == 1 else user.timezone.split('-')

    offset = int(result[1]) * sign if len(result) > 1 else 0

    return result[0], offset
