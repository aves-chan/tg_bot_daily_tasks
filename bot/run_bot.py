from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from aiogram_dialog import (DialogManager, setup_dialogs, StartMode)

from bot.database.db_question import db_check_user
from bot.dialog.all_tasks import all_tasks
from bot.dialog.main_dialog_and_profile import main_dialog
from bot.dialog.new_task_dialog import new_task_dialog
from bot.states import MainSG
from config import BOT_TOKEN

import logging


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
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot, skip_updates=True)