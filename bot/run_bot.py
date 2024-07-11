import datetime
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from aiogram_dialog import (DialogManager, setup_dialogs, StartMode)

from bot import db_check_user, get_all_tasks_for_remind, set_completed_remind
from bot import all_tasks
from bot import main_dialog
from bot import new_task_dialog
from bot import MainSG
from config import BOT_TOKEN

import logging

# def kb_back() -> InlineKeyboardMarkup:
#     kb = InlineKeyboardBuilder()
#     kb.button(text='main menu', callback_data='main menu')
#     return kb.as_markup()


def return_first_index(result: list) -> list:
    return result[0]

async def update_remind() -> None:
    while True:
        result = get_all_tasks_for_remind()
        remind_times = [[task.date + ' ' + task.time, task] for task in result]
        remind_times = [[datetime.datetime.strptime(remind_time[0], '%Y-%m-%d %H:%M'), remind_time] for remind_time in remind_times]
        if len(remind_times) > 0:
            min_time = min(remind_times, key=return_first_index)
            if min_time[0] < datetime.datetime.now():
                await bot.send_message(chat_id=min_time[1][1].telegram_id,
                                       text=f'<b>{min_time[1][1].title}</b>\n\n{min_time[1][1].description}',
                                       # reply_markup=kb_back(),
                                       parse_mode='HTML')
                set_completed_remind(min_time[1][1].telegram_id, min_time[1][1].title)
        await asyncio.sleep(0.5)

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)
dp.include_routers(main_dialog, new_task_dialog, all_tasks)
setup_dialogs(dp)
 
@dp.message(Command('start'))
async def start(message: Message, dialog_manager: DialogManager):
    db_check_user(telegram_id=message.from_user.id,
                  username=message.from_user.username,
                  first_name=message.from_user.first_name,
                  last_name=message.from_user.last_name)
    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)

# @dp.callback_query(F.data == 'main menu')
# async def start(cd: CallbackQuery, dialog_manager: DialogManager):
#     await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)

async def main():
    asyncio.ensure_future(update_remind())
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
