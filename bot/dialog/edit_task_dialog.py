from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.dialog import ChatEvent
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Row, SwitchTo, Cancel
from aiogram_dialog.widgets.text import Const

from bot.database.db_question import db_check_title_in_tasks, db_edit_title, db_edit_description
from bot.states import AllTasks, EditTask

async def handler_edit_title(message: Message,
                             message_input: MessageInput,
                             dialog_manager: DialogManager
                             ) -> None:
    if len(message.text) <= 15:
        if db_check_title_in_tasks(telegram_id=dialog_manager.event.from_user.id,
                                   title=message.text):
            await dialog_manager.event.answer('a task with that name already exists')
        else:
            db_edit_title(telegram_id=dialog_manager.event.from_user.id,
                          title=dialog_manager.dialog_data.get('title'))
            await dialog_manager.done()
    else:
        await dialog_manager.event.answer(f'you are sending a long title, your size title is {len(message.text)}')

async def handler_edit_description(message: Message,
                                   message_input: MessageInput,
                                   dialog_manager: DialogManager
                                   ) -> None:
    if len(message.text) <= 3500:
        db_edit_description(telegram_id=dialog_manager.event.from_user.id,
                            title=dialog_manager.dialog_data.get('title'),
                            description=dialog_manager.event.text)
        await dialog_manager.done()
    else:
        await dialog_manager.event.answer(f'you are sending a long description, your size description is {len(message.text)}')


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
        Const('send title please, maximum of 15 characters'),
        MessageInput(func=handler_edit_title, content_types=ContentType.TEXT),
        SwitchTo(Const('Back'), id='t_back', state=EditTask.choose_edit),
        state=EditTask.edit_title
    ),
    Window(
        Const('send description please, maximum of 3500 characters'),
        MessageInput(func=handler_edit_description, content_types=ContentType.TEXT),
        SwitchTo(Const('Back'), id='t_back', state=EditTask.choose_edit),
        state=EditTask.edit_description
    ),
)