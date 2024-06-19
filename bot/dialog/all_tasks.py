import operator
import re

from aiogram import Dispatcher, Bot
from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Row, Start, Cancel, Calendar, Select, ScrollingGroup, Next
from aiogram_dialog.widgets.text import Const, Format, Multi

from bot.database.db_question import db_set_task, db_get_tasks, db_get_task
from bot.states import AllTasks, NewTask, MainSG

from datetime import date

async def get_all_tasks(dialog_manager: DialogManager, **kwargs) -> dict:
    tasks = db_get_tasks(telegram_id=dialog_manager.event.from_user.id)
    buttons = []
    i = 0
    for task in tasks:
        buttons.append((task[2], str(i)))
        i += 1
    return {
        'buttons': buttons,
        'count': len(buttons)
    }

async def on_clicked_task(callback_query: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager,
                          item_id: str) -> None:
    dialog_manager.dialog_data['item_id'] = item_id
    await dialog_manager.next()


async def get_task(dialog_manager: DialogManager, **kwargs) -> dict:
    task = db_get_task(telegram_id=dialog_manager.event.from_user.id,
                       title=dialog_manager.dialog_data.get('item_id'))
    return {
        'completion': task[1],
        'title': task[2],
        'description': task[3],
        'date': task[4],
        'time': task[5],
    }

all_tasks = Dialog(
    Window(
        Const('all tasks'),
        ScrollingGroup(
            Select(
                Format('{item[0]}'),
                id='s_tasks',
                item_id_getter=operator.itemgetter(0),
                items='buttons',
                on_click=on_clicked_task
            ),
            id='sg_tasks',
            width=3,
            height=3,
        ),
        Cancel(),
        getter=get_all_tasks,
        state=AllTasks.choose_task
    ),
    Window(
        Format('<b>{title}</b>\n\n<b>{description}</b>\n\nremind: <b>{date} {time}</b>'),
        Back(),
        getter=get_task,
        parse_mode='HTML',
        state=AllTasks.about_task
    )
)
