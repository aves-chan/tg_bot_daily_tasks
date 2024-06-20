from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.dialog import ChatEvent
from aiogram_dialog.widgets.kbd import Button, Back, Row, SwitchTo, Cancel
from aiogram_dialog.widgets.text import Const

from bot.states import AllTasks, EditTask

edit_task_dialog = Dialog(
    Window(
        Const('choose what you will change'),
        Row(
            SwitchTo(Const('title'), id='e_title', state=EditTask.edit_title),
            SwitchTo(Const('description'), id='e_description', state=EditTask.edit_description),
        ),
        Cancel(),
        state=EditTask.choose_edit
    ),
    Window(
        Const(''),
    )
)