import re
from datetime import date, datetime, timedelta

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.dialog import ChatEvent
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, ManagedCheckbox

from bot.database.db_question import db_get_tasks, db_get_task, db_delete_task, db_check_title_in_tasks, db_edit_title, \
    db_edit_description, db_edit_reminder

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

async def on_click_edit_date(callback_query: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager,
                             selected_date: date
                             ) -> None:
    if selected_date >= datetime.now().date():
        dialog_manager.dialog_data['date'] = selected_date
        await dialog_manager.switch_to(state=AllTasks.edit_time)
    else:
        await dialog_manager.event.answer(text='choose a date no later than today', show_alert=True)

async def handler_time(message: Message,
                       button: Button,
                       dialog_manager: DialogManager
                       ) -> None:
    regexp = re.compile("(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])")
    if (bool(regexp.match(message.text))):
        result_date = dialog_manager.dialog_data['date']
        result_time = datetime.strptime(message.text, '%H:%M').time()
        if result_date == datetime.now().date() and result_time < (datetime.now() + timedelta(minutes=10)).time():
            await dialog_manager.event.answer(text='you have sent an outdated date', show_alert=True)
        else:
            db_edit_reminder(telegram_id=dialog_manager.event.from_user.id,
                             title=dialog_manager.dialog_data.get('title'),
                             date=dialog_manager.dialog_data.get('date'),
                             time=message.text,
                             remind=True)
            await dialog_manager.switch_to(state=AllTasks.about_task)

async def remove_remind(callback_query: CallbackQuery,
                        button: Button,
                        dialog_manager: DialogManager,
                        ) -> None:
    db_edit_reminder(telegram_id=dialog_manager.event.from_user.id,
                     title=dialog_manager.dialog_data.get('title'),
                     date='No',
                     time='No',
                     remind=False)