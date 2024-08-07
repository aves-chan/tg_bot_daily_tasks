import re

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from datetime import date, datetime, timedelta

from bot.database.db_config import RemindColumn
from bot.database.db_question import db_check_title_in_tasks, db_set_task
from bot.states import NewTask, MainSG


async def handler_title(message: Message,
                        message_input: MessageInput,
                        dialog_manager: DialogManager
                        ) -> None:
    if len(message.text) <= 15:
        if db_check_title_in_tasks(telegram_id=dialog_manager.event.from_user.id, title=message.text):
            await dialog_manager.event.answer('A task with that name already exists')
        else:
            dialog_manager.dialog_data['title'] = message.text
            await dialog_manager.next()
    else:
        await dialog_manager.event.answer(f'You are sending a long title, your size title is {len(message.text)}')

async def handler_description(message: Message,
                              message_input: MessageInput,
                              dialog_manager: DialogManager
                              ) -> None:
    if len(message.text) <= 3500:
        dialog_manager.dialog_data['description'] = message.text
        await dialog_manager.next()
    else:
        await dialog_manager.event.answer(f'You are sending a long description, your size description is {len(message.text)}')


async def on_click_date(callback_query: CallbackQuery,
                        button: Button,
                        dialog_manager: DialogManager
                        ) -> None:
    if (callback_query.data == 'yes'):
        dialog_manager.dialog_data['remind'] = RemindColumn.remind
        await dialog_manager.next()
    elif (callback_query.data == 'no'):
        dialog_manager.dialog_data['remind'] = RemindColumn.not_remind
        await dialog_manager.switch_to(state=NewTask.confirm)

async def on_click_chose_date(callback_query: CallbackQuery,
                              button: Button,
                              dialog_manager: DialogManager,
                              selected_date: date
                              ) -> None:
    if selected_date >= (datetime.now() + timedelta(hours=dialog_manager.dialog_data['user_timedelta'])).date():
        dialog_manager.dialog_data['selected_date'] = selected_date
        await dialog_manager.next()
    else:
        await dialog_manager.event.answer(text='Choose a date no later than today', show_alert=True)

async def handler_time(message: Message,
                       button: Button,
                       dialog_manager: DialogManager
                       ) -> None:
    regexp = re.compile("(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])")
    if (bool(regexp.match(message.text))):
        selected_datetime = datetime.combine(dialog_manager.dialog_data.get('selected_date'), datetime.strptime(message.text, '%H:%M').time())
        if selected_datetime < datetime.now() + timedelta(hours=dialog_manager.dialog_data['user_timedelta']):
            await dialog_manager.event.answer(text='You have sent an outdated date', show_alert=True)
        else:
            dialog_manager.dialog_data['selected_datetime'] = selected_datetime
            await dialog_manager.next()

async def on_click_edit_task(callback_query: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager,
                             ) -> None:
    if dialog_manager.dialog_data['remind'] == RemindColumn.not_remind:
        await dialog_manager.switch_to(NewTask.set_description)
    else:
        await dialog_manager.back()

async def get_task(dialog_manager: DialogManager, **kwargs) -> dict:
    if dialog_manager.dialog_data.get('remind') == RemindColumn.not_remind:
        selected_datetime = 'Do not remind'
    else:
        selected_datetime = dialog_manager.dialog_data.get('selected_datetime')
    return {
        'title': dialog_manager.dialog_data.get('title'),
        'description': dialog_manager.dialog_data.get('description'),
        'selected_datetime': selected_datetime
    }

async def on_click_set_task(callback_query: CallbackQuery,
                            button: Button,
                            dialog_manager: DialogManager,
                            ) -> None:
    if dialog_manager.dialog_data['remind'] == RemindColumn.remind:
        date_time = dialog_manager.dialog_data.get('selected_datetime') - timedelta(
                        hours=dialog_manager.dialog_data.get('user_timedelta'))
    else:
        date_time = RemindColumn.not_remind
    if (db_set_task(telegram_id=callback_query.from_user.id,
                    title=dialog_manager.dialog_data.get('title'),
                    description=dialog_manager.dialog_data.get('description'),
                    date_time=date_time,
                    remind=dialog_manager.dialog_data.get('remind'))):
        await callback_query.answer(text='Successfully!')
        await dialog_manager.start(MainSG.main)
    else:
        await callback_query.answer(text='Ops, try again(', show_alert=True)
        await dialog_manager.start(MainSG.main)
