from datetime import date, datetime, timedelta

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bot.database.db_config import CompletionColumn, RemindColumn
from bot.database.db_question import (db_set_complete, db_delete_task, db_get_tasks_by_id, db_get_task,
                                      db_edit_title, db_edit_description, db_edit_reminder, db_get_count_tasks,
                                      db_delete_all_tasks)
from bot.dialog.handler_utils import check_title_validation, check_description_validation, check_date_validation, \
    check_time_validation
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
    await dialog_manager.switch_to(state=AllTasks.about_task)

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
        await dialog_manager.switch_to(state=AllTasks.delete_all_tasks)

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
    if await check_title_validation(text=message.text, dialog_manager=dialog_manager):
        db_edit_title(telegram_id=dialog_manager.event.from_user.id,
                      title=dialog_manager.dialog_data.get('title'),
                      new_title=message.text)
        dialog_manager.dialog_data['title'] = dialog_manager.event.text
        await dialog_manager.switch_to(AllTasks.about_task)

async def handler_edit_description(message: Message,
                                   message_input: MessageInput,
                                   dialog_manager: DialogManager
                                   ) -> None:
    if await check_description_validation(text=message.text, dialog_manager=dialog_manager):
        db_edit_description(telegram_id=dialog_manager.event.from_user.id,
                            title=dialog_manager.dialog_data.get('title'),
                            new_description=dialog_manager.event.text)
        await dialog_manager.switch_to(AllTasks.about_task)

async def on_click_edit_date(callback_query: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager,
                             selected_date: date
                             ) -> None:
    if await check_date_validation(selected_date=selected_date, dialog_manager=dialog_manager):
        dialog_manager.dialog_data['selected_date'] = str(selected_date)
        await dialog_manager.switch_to(state=AllTasks.edit_time)

async def handler_edit_time(message: Message,
                            button: Button,
                            dialog_manager: DialogManager
                            ) -> None:
    result = await check_time_validation(text=message.text, dialog_manager=dialog_manager)
    if isinstance(result, datetime):
        db_edit_reminder(telegram_id=dialog_manager.event.from_user.id,
                         title=dialog_manager.dialog_data.get('title'),
                         date_time=result - timedelta(hours=dialog_manager.dialog_data['user_timedelta']),
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
