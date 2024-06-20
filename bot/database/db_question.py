import sqlite3

from config import DB_PATH


def db_check_user(telegram_id: int, username: str, firstname: str, lastname: str) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM Users WHERE telegram_id = {telegram_id}")
    if cur.fetchone() == None:
        cur.execute(f"INSERT INTO Users (telegram_id, username, firstname, lastname) VALUES ({telegram_id}, '{username}', '{firstname}', '{lastname}')")
    con.commit()
    con.close()

def db_check_title_in_tasks(telegram_id: int, title: str) -> bool:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM Tasks WHERE telegram_id = {telegram_id} AND title = '{title}'")
    result = cur.fetchone()
    con.commit()
    con.close()
    if result == None:
        return False
    else:
        return True

def db_set_task(telegram_id: int, title: str, description: str, date: str, time: str, remind: bool) -> bool:
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute(f"INSERT INTO Tasks (telegram_id, title, description, date, time, remind) VALUES ({telegram_id}, '{title}', '{description}', '{date}', '{time}', '{remind}')")
        con.commit()
        con.close()
        return True
    except:
        return False

def db_edit_title(telegram_id: int, title: str) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"UPDATE Tasks SET title = '{title}' WHERE telegram_id = {telegram_id} AND title = '{title}'")
    con.commit()
    con.close()

def db_edit_description(telegram_id: int, title: str, description: str) -> None:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"UPDATE Tasks SET description = '{description}' WHERE telegram_id = {telegram_id} AND title = '{title}'")
    con.commit()
    con.close()

def db_delete_task(telegram_id: int, title: str) -> bool:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"DELETE FROM Tasks WHERE telegram_id = {telegram_id} AND title = '{title}'")
    con.commit()
    con.close()

def db_task_completed(telegram_id: int, title: str) -> bool:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM Tasks WHERE telegram_id = {telegram_id} AND title = '{title}'")
    result = cur.fetchone()
    con.commit()
    con.close()
    if result == None:
        return False
    else:
        return True

def db_get_tasks(telegram_id: int) -> list:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM Tasks WHERE telegram_id = {telegram_id}")
    tasks = cur.fetchall()
    con.commit()
    con.close()
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
