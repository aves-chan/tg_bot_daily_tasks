import datetime
import asyncio
from logging.handlers import RotatingFileHandler

from aiogram.fsm.storage.base import KeyBuilder, DefaultKeyBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from redis import asyncio as redis_asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from aiogram_dialog import (DialogManager, setup_dialogs, StartMode, ShowMode)

from bot.database.db_config import Base, db_engine
from bot.database.db_question import db_get_all_tasks_for_remind, db_set_completed_remind, db_check_user
from bot.dialog.all_tasks.all_tasks_dialog import all_tasks_dialog
from bot.dialog.main_dialog import main_dialog
from bot.dialog.new_task.new_task_dialog import new_task_dialog
from bot.dialog.profile.profile_dialog import profile_dialog
from bot.states import MainSG
from config import BOT_TOKEN, REDIS_PORT, REDIS_PASSWORD, REDIS_HOST

import logging

def kb_back() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Hide the reminder', callback_data='hide the reminder')
    return kb.as_markup()


async def update_remind() -> None:
    while True:
        result = db_get_all_tasks_for_remind()
        remind_times = [[task.datetime, task] for task in result]
        remind_times = [[datetime.datetime.strptime(remind_time[0], '%Y-%m-%d %H:%M:%S'), remind_time] for remind_time in remind_times]
        if len(remind_times) > 0:
            min_time = min(remind_times, key=lambda x: x[0])
            if min_time[0] < datetime.datetime.now():
                await bot.send_message(chat_id=min_time[1][1].telegram_id,
                                       text=f'<b>{min_time[1][1].title}</b>\n\n{min_time[1][1].description}',
                                       reply_markup=kb_back(),
                                       parse_mode='HTML')
                db_set_completed_remind(min_time[1][1].telegram_id, min_time[1][1].title)
        await asyncio.sleep(0.5)


storage = redis_asyncio.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=RedisStorage(redis=storage, key_builder=DefaultKeyBuilder(with_destiny=True)))
dp.include_routers(main_dialog, new_task_dialog, all_tasks_dialog, profile_dialog)
setup_dialogs(dp)
 
@dp.message(Command('start'))
async def start(message: Message, dialog_manager: DialogManager):
    db_check_user(telegram_id=message.from_user.id,
                  username=str(message.from_user.username),
                  first_name=str(message.from_user.first_name),
                  last_name=str(message.from_user.last_name))
    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)

@dp.callback_query(F.data == 'hide the reminder')
async def handler_hide_the_reminder(cd: CallbackQuery, dialog_manager: DialogManager):
    await cd.message.delete()
    await cd.answer()

async def main():
    Base.metadata.create_all(bind=db_engine)
    asyncio.ensure_future(update_remind())
    handler = RotatingFileHandler('tg_bot.log')
    logging.basicConfig(level=logging.INFO, handlers=[handler])
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
