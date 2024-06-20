import operator

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.dialog import ChatEvent
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Row, Start, Cancel, Checkbox, Select, ScrollingGroup, \
    ManagedCheckbox, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from bot.database.db_question import db_get_tasks, db_get_task, db_delete_task, db_check_title_in_tasks, db_edit_title, \
    db_edit_description

from bot.states import AllTasks

async def on_clicked_task(callback_query: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager,
                          item_id: str) -> None:
    dialog_manager.dialog_data['title'] = item_id
    await dialog_manager.next()

async def checkbox_completion_task(event: ChatEvent,
                                   checkbox: ManagedCheckbox,
                                   manager: DialogManager) -> None:
    print("Check status changed:", checkbox.is_checked())


async def delete_task(callback_query: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager) -> None:
    db_delete_task(telegram_id=dialog_manager.event.from_user.id,
                   title=dialog_manager.dialog_data.get('title'))
    await dialog_manager.event.answer(text='task deleted')
    await dialog_manager.switch_to(AllTasks.all_tasks)

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

async def get_task(dialog_manager: DialogManager, **kwargs) -> dict:
    task = db_get_task(telegram_id=dialog_manager.event.from_user.id,
                       title=dialog_manager.dialog_data.get('title'))
    return {
        'completion': task[1],
        'title': task[2],
        'description': task[3],
        'date': task[4],
        'time': task[5],
    }

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
                          title=dialog_manager.dialog_data.get('title'),
                          new_title=message.text)
            dialog_manager.dialog_data['title'] = dialog_manager.event.text
            await dialog_manager.switch_to(AllTasks.about_task)
    else:
        await dialog_manager.event.answer(f'you are sending a long title, your size title is {len(message.text)}')

async def handler_edit_description(message: Message,
                                   message_input: MessageInput,
                                   dialog_manager: DialogManager
                                   ) -> None:
    if len(message.text) <= 3500:
        db_edit_description(telegram_id=dialog_manager.event.from_user.id,
                            title=dialog_manager.dialog_data.get('title'),
                            new_description=dialog_manager.event.text)
        await dialog_manager.switch_to(AllTasks.about_task)
    else:
        await dialog_manager.event.answer(f'you are sending a long description, your size description is {len(message.text)}')


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
        state=AllTasks.all_tasks
    ),
    Window(
        Format('<b>{title}</b>\n\n<b>{description}</b>\n\nremind: <b>{date} {time}</b>'),
        Checkbox(
            Const('completed ✅'),
            Const('completed ❌'),
            id='s_completed',
            default=False,
            on_click=checkbox_completion_task
        ),
        Row(
            Button(Const('edit reminder'), id='edit_reminder'),
            SwitchTo(Const('edit task'), id='edit_task', state=AllTasks.choose_edit)
        ),
        SwitchTo(Const('delete task'), id='delete_task', state=AllTasks.delete_task),
        Back(),
        getter=get_task,
        parse_mode='HTML',
        state=AllTasks.about_task
    ),
    Window(
        Const('are you sure you want to delete the task?'),
        Button(Const('yes'), id='yes', on_click=delete_task),
        Back(),
        state=AllTasks.delete_task
    ),
    Window(
        Const('choose what you will change'),
        Row(
            SwitchTo(Const('title'), id='e_title', state=AllTasks.edit_title),
            SwitchTo(Const('description'), id='e_description', state=AllTasks.edit_description),
        ),
        Cancel(),
        state=AllTasks.choose_edit
    ),
    Window(
        Const('send title please, maximum of 15 characters'),
        MessageInput(func=handler_edit_title, content_types=ContentType.TEXT),
        SwitchTo(Const('Back'), id='t_back', state=AllTasks.choose_edit),
        state=AllTasks.edit_title
    ),
    Window(
        Const('send description please, maximum of 3500 characters'),
        MessageInput(func=handler_edit_description, content_types=ContentType.TEXT),
        SwitchTo(Const('Back'), id='t_back', state=AllTasks.choose_edit),
        state=AllTasks.edit_description
    )
)
