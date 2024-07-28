import re
from datetime import date, datetime, timedelta

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bot.database.db_config import CompletionColumn, RemindColumn
from bot.database.db_question import db_set_complete, db_delete_task, db_get_tasks_by_id, db_get_task, \
    db_check_title_in_tasks, db_edit_title, db_edit_description, db_edit_reminder, db_get_user, db_get_count_tasks, \
    db_delete_all_tasks
from bot.states import AllTasks

async def get_tasks_by_id(dialog_manager: DialogManager, **kwargs) -> dict:
    tasks = db_get_tasks_by_id(telegram_id=dialog_manager.event.from_user.id)
    buttons = []
    i = 0
    for task in tasks:
        buttons.append((task.title, str(i)))
        i += 1
    return {
        'buttons': buttons,
        'count': len(buttons)
    }

async def get_count_tasks(dialog_manager: DialogManager, **kwargs) -> dict:
    return {
        'count_tasks': dialog_manager.dialog_data.get('count_tasks')
    }

async def on_clicked_task(callback_query: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager,
                          item_id: str) -> None:
    dialog_manager.dialog_data['title'] = item_id
    await dialog_manager.next()

async def on_clicked_completion_task(callback_query: CallbackQuery,
                                     button: Button,
                                     dialog_manager: DialogManager) -> None:
    if dialog_manager.dialog_data.get('completion') == CompletionColumn.completed:
        result = CompletionColumn.not_completed
    else:
        result = CompletionColumn.completed
    dialog_manager.dialog_data['completion'] = result
    db_set_complete(telegram_id=dialog_manager.event.from_user.id,
                    title=dialog_manager.dialog_data.get('title'),
                    completion=result)

async def delete_task(callback_query: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager) -> None:
    db_delete_task(telegram_id=dialog_manager.event.from_user.id,
                   title=dialog_manager.dialog_data.get('title'))
    await dialog_manager.event.answer(text='Task deleted')
    await dialog_manager.switch_to(AllTasks.all_tasks)

async def on_clicked_delete_all_tasks(message: Message,
                                      message_input: MessageInput,
                                      dialog_manager: DialogManager
                                      ) -> None:
    count = db_get_count_tasks(dialog_manager.event.from_user.id)
    if count == 0:
        await dialog_manager.event.answer(text='You have 0 tasks', show_alert=True)
    else:
        dialog_manager.dialog_data['count_tasks'] = count
        await dialog_manager.switch_to(state=AllTasks.confirmation_of_deletion_of_all_tasks)

async def handler_delete_all_tasks(message: Message,
                                   message_input: MessageInput,
                                   dialog_manager: DialogManager
                                   ) -> None:
    if message.text != 'I want to delete all tasks':
        await dialog_manager.event.answer(text='You wrote it wrong')
    else:
        db_delete_all_tasks(telegram_id=dialog_manager.event.from_user.id)
        await dialog_manager.event.answer(text='You deleted all tasks', show_alert=True)
        await dialog_manager.done()


async def get_task(dialog_manager: DialogManager, **kwargs) -> dict:
    task, user_timezone, user_timedelta = db_get_task(telegram_id=dialog_manager.event.from_user.id,
                                                      title=dialog_manager.dialog_data.get('title'))
    completion = '...'
    if task is None:
        await dialog_manager.event.answer(text='Task not found', show_alert=True)
    elif task.completion == CompletionColumn.completed:
        completion = 'completed✅'
    else:
        completion = 'completed❌'
    dialog_manager.dialog_data['completion'] = task.completion
    if task.datetime == RemindColumn.not_remind:
        date_time = 'Do not remind'
    else:
        date_time = str(datetime.strptime(task.datetime, '%Y-%m-%d %H:%M:%S') + timedelta(hours=user_timedelta))
    return {
        'completion': completion,
        'title': task.title,
        'description': task.description,
        'datetime': date_time
    }

async def handler_edit_title(message: Message,
                             message_input: MessageInput,
                             dialog_manager: DialogManager
                             ) -> None:
    if len(message.text) <= 15:
        if db_check_title_in_tasks(telegram_id=dialog_manager.event.from_user.id,
                                   title=message.text):
            await dialog_manager.event.answer('A task with that name already exists')
        else:
            db_edit_title(telegram_id=dialog_manager.event.from_user.id,
                          title=dialog_manager.dialog_data.get('title'),
                          new_title=message.text)
            dialog_manager.dialog_data['title'] = dialog_manager.event.text
            await dialog_manager.switch_to(AllTasks.about_task)
    else:
        await dialog_manager.event.answer(f'You are sending a long title, your size title is {len(message.text)}')

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
        await dialog_manager.event.answer(f'You are sending a long description, your size description is {len(message.text)}')

async def on_click_edit_date(callback_query: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager,
                             selected_date: date
                             ) -> None:
    if selected_date >= (datetime.now() + timedelta(hours=dialog_manager.dialog_data.get('user_timedelta'))).date():
        dialog_manager.dialog_data['selected_date'] = selected_date
        await dialog_manager.switch_to(state=AllTasks.edit_time)
    else:
        await dialog_manager.event.answer(text='Choose a date no later than today', show_alert=True)

async def handler_edit_time(message: Message,
                            button: Button,
                            dialog_manager: DialogManager
                            ) -> None:
    regexp = re.compile("(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])")
    if (bool(regexp.match(message.text))):
        selected_datetime = datetime.combine(dialog_manager.dialog_data.get('selected_date'),
                                             datetime.strptime(message.text, '%H:%M').time())
        if selected_datetime < datetime.now() + timedelta(hours=dialog_manager.dialog_data['user_timedelta']):
            await dialog_manager.event.answer(text='You have sent an outdated date', show_alert=True)
        else:
            db_edit_reminder(telegram_id=dialog_manager.event.from_user.id,
                             title=dialog_manager.dialog_data.get('title'),
                             date_time=selected_datetime - timedelta(hours=dialog_manager.dialog_data['user_timedelta']),
                             remind=RemindColumn.remind)
            await dialog_manager.switch_to(state=AllTasks.about_task)

async def remove_remind(callback_query: CallbackQuery,
                        button: Button,
                        dialog_manager: DialogManager,
                        ) -> None:
    db_edit_reminder(telegram_id=dialog_manager.event.from_user.id,
                     title=dialog_manager.dialog_data.get('title'),
                     date_time=RemindColumn.not_remind,
                     remind=RemindColumn.not_remind)
