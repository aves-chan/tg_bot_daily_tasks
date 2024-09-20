from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from datetime import date, datetime, timedelta

from bot.database.db_config import RemindColumn
from bot.database.db_question import db_set_task
from bot.dialog.handler_utils import check_title_validation, check_description_validation, check_date_validation, \
    check_time_validation
from bot.states import NewTask, MainSG


async def handler_title(message: Message,
                        message_input: MessageInput,
                        dialog_manager: DialogManager
                        ) -> None:
    if await check_title_validation(text=message.text, dialog_manager=dialog_manager):
        dialog_manager.dialog_data['title'] = message.text
        await dialog_manager.next()

async def handler_description(message: Message,
                              message_input: MessageInput,
                              dialog_manager: DialogManager
                              ) -> None:
    if await check_description_validation(text=message.text, dialog_manager=dialog_manager):
        dialog_manager.dialog_data['description'] = message.text
        await dialog_manager.next()


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
    if await check_date_validation(selected_date=selected_date, dialog_manager=dialog_manager):
        dialog_manager.dialog_data['selected_date'] = str(selected_date)
        await dialog_manager.next()

async def handler_time(message: Message,
                       button: Button,
                       dialog_manager: DialogManager
                       ) -> None:
    result = await check_time_validation(text=message.text, dialog_manager=dialog_manager)
    if isinstance(result, datetime):
        dialog_manager.dialog_data['selected_datetime'] = str(result)
        await dialog_manager.next()

async def on_click_edit_task(callback_query: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager,
                             ) -> None:
    if dialog_manager.dialog_data['remind'] == RemindColumn.not_remind:
        await dialog_manager.switch_to(NewTask.set_description)
    else:
        await dialog_manager.back()

async def get_new_task(dialog_manager: DialogManager, **kwargs) -> dict:
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
        selected_datetime = datetime.strptime(dialog_manager.dialog_data.get('selected_datetime'), '%Y-%m-%d %H:%M:%S') - timedelta(
            hours=dialog_manager.dialog_data.get('user_timedelta'))
    else:
        selected_datetime = RemindColumn.not_remind
    if (db_set_task(telegram_id=callback_query.from_user.id,
                    title=dialog_manager.dialog_data.get('title'),
                    description=dialog_manager.dialog_data.get('description'),
                    date_time=selected_datetime,
                    remind=dialog_manager.dialog_data.get('remind'))):
        await callback_query.answer(text='Successfully!')
        await dialog_manager.start(MainSG.main)
    else:
        await callback_query.answer(text='Ops, try again(', show_alert=True)
        await dialog_manager.start(MainSG.main)
