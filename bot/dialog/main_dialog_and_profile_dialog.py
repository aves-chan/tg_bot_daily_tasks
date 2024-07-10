from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Row, Start
from aiogram_dialog.widgets.text import Const, Format

from bot.database.db_question import db_get_count_task
from bot.states import MainSG, AllTasks, NewTask

async def get_profile(dialog_manager: DialogManager, **kwargs):
    count_task = db_get_count_task(telegram_id=dialog_manager.event.from_user.id)
    return {
        'id': dialog_manager.event.from_user.id,
        'firstname': dialog_manager.event.from_user.first_name,
        'lastname': dialog_manager.event.from_user.last_name,
        'username': dialog_manager.event.from_user.username,
        'count_task': count_task,
    }

main_dialog = Dialog(
    Window(
        Const('Main menu'),
        Row(
            Start(Const('My tasks'), id='my_tasks', state=AllTasks.all_tasks),
            Start(Const('New tasks'), id='new_tasks', state=NewTask.set_title)
        ),
        Start(Const('Profile'), id='profile', state=MainSG.profile),
        state=MainSG.main
    ),
    Window(
        Format('id: <tg-spoiler>{id}</tg-spoiler>\nfirstname: <b>{firstname}</b>\nlastname: <b>{lastname}</b>\nusername: <b>{username}</b>\ncount task: <b>{count_task}</b>'),
        Back(),
        getter=get_profile,
        parse_mode='HTML',
        state=MainSG.profile
    )
)
