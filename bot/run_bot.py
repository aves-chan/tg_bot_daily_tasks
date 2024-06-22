import time
import datetime
import threading
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from aiogram_dialog import (DialogManager, setup_dialogs, StartMode)

from bot.database.db_question import db_check_user, get_all_tasks, delete_remind
from bot.dialog.all_tasks.all_tasks_dialog import all_tasks
from bot.dialog.main_dialog_and_profile_dialog import main_dialog
from bot.dialog.new_task.new_task_dialog import new_task_dialog
from bot.states import MainSG
from config import BOT_TOKEN

import logging
def return_first_index(result:list)->list:
    return result[0]
def update_remind() -> None:
    while True:
        result = get_all_tasks()
        remind_times = [[task[4] + " " + task[5], task] for task in result]
        print(remind_times, result)
        remind_times = [[datetime.datetime.strptime(remind_time[0], "%Y-%m-%d %H:%M"), remind_time] for remind_time in remind_times]
        min_time = min(remind_times, key = return_first_index)
        if min_time[0] < datetime.datetime.now():
            # send()
            delete_remind(min_time[1][1][0], min_time[1][1][2])
        time.sleep(5)

get_all_tasks()

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)
dp.include_routers(main_dialog, new_task_dialog, all_tasks)
setup_dialogs(dp)

@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    db_check_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    thread = threading.Thread(target=update_remind)
    thread.start()
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot, skip_updates=True)