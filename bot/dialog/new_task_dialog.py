import re

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Row, Cancel, Calendar
from aiogram_dialog.widgets.text import Const, Format

from bot.database.db_question import db_set_task, db_check_title_in_tasks
from bot.states import NewTask, MainSG

from datetime import date

async def handler_title(message: Message,
                        message_input: MessageInput,
                        dialog_manager: DialogManager
                        ) -> None:
    if len(message.text) <= 15:
        if db_check_title_in_tasks(telegram_id=dialog_manager.event.from_user.id, title=message.text):
            await dialog_manager.event.answer('a task with that name already exists')
        else:
            dialog_manager.dialog_data['title'] = message.text
            await dialog_manager.next()
    else:
        await dialog_manager.event.answer(f'you are sending a long title, your size title is {len(message.text)}')

async def handler_description(message: Message,
                              message_input: MessageInput,
                              dialog_manager: DialogManager
                              ) -> None:
    if len(message.text) <= 3500:
        dialog_manager.dialog_data['description'] = message.text
        await dialog_manager.next()
    else:
        await dialog_manager.event.answer(f'you are sending a long description, your size description is {len(message.text)}')


async def on_click_date(callback_query: CallbackQuery,
                        button: Button,
                        dialog_manager: DialogManager
                        ) -> None:
    if (callback_query.data == 'yes'):
        await dialog_manager.next()
    elif (callback_query.data == 'no'):
        dialog_manager.dialog_data['date'] = 'No'
        dialog_manager.dialog_data['time'] = 'No'
        await dialog_manager.switch_to(state=NewTask.confirm)

async def handler_time(message: Message,
                       button: Button,
                       dialog_manager: DialogManager
                       ) -> None:
    text = message.text
    regexp = re.compile("(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])")
    if (bool(regexp.match(text))):
        dialog_manager.dialog_data['time'] = text
        dialog_manager.dialog_data['remind'] = True
        await dialog_manager.next()

async def on_click_chose_date(callback_query: CallbackQuery,
                              button: Button,
                              dialog_manager: DialogManager,
                              selected_date: date
                              ) -> None:
    dialog_manager.dialog_data['date'] = selected_date
    await dialog_manager.next()

async def on_click_edit_task(callback_query: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager,
                             ) -> None:
    data = callback_query.data
    if data == 'no':
        if dialog_manager.dialog_data['date'] == 'No' and dialog_manager.dialog_data['time'] == 'No':
            await dialog_manager.switch_to(NewTask.set_description)
        else:
            await dialog_manager.back()

async def on_click_set_task(callback_query: CallbackQuery,
                            button: Button,
                            dialog_manager: DialogManager,
                            ) -> None:
    result = db_set_task(telegram_id=callback_query.from_user.id,
                         title=dialog_manager.dialog_data.get('title'),
                         description=dialog_manager.dialog_data.get('description'),
                         date=dialog_manager.dialog_data.get('date'),
                         time=dialog_manager.dialog_data.get('time'),
                         remind=dialog_manager.dialog_data.get('remind'))
    if (result):
        await callback_query.answer(text='successfully!')
        await dialog_manager.start(MainSG.main)
    else:
        await callback_query.answer(text='ops, try again(', show_alert=True)
        await dialog_manager.start(MainSG.main)
def generate_time_menu() -> list:
    buttons = []
    for i in range(24):
        i = str(i)
        buttons.append(Button(Const(i), id=i))
    return buttons

async def get_task(dialog_manager: DialogManager, **kwargs) -> dict:
    return {
        'title': dialog_manager.dialog_data.get('title'),
        'description': dialog_manager.dialog_data.get('description'),
        'date': dialog_manager.dialog_data.get('date'),
        'time': dialog_manager.dialog_data.get('time'),
    }


new_task_dialog = Dialog(
    Window(
        Const('send title please, maximum of 15 characters'),
        MessageInput(func=handler_title, content_types=ContentType.TEXT),
        Cancel(),
        state=NewTask.set_title
    ),
    Window(
        Const('send description please, maximum of 3500 characters'),
        MessageInput(func=handler_description, content_types=ContentType.TEXT),
        Back(),
        state=NewTask.set_description
    ),
    Window(
        Const('should I remind you?'),
        Row(
            Button(Const('Yes'), id='yes', on_click=on_click_date),
            Button(Const('No'), id='no', on_click=on_click_date),
        ),
        Back(),
        state=NewTask.date_remind_choose
    ),
    Window(
        Const('choose date'),
        Calendar(id='calendar', on_click=on_click_chose_date),
        Back(),
        state=NewTask.choose_date,
    ),
    Window(
        Const('send time like this 22:22 please'),
        MessageInput(func=handler_time, content_types=ContentType.TEXT),
        Back(),
        state=NewTask.choose_time
    ),
    Window(
        Const('right?'),
        Format('title: <b>{title}</b>\n\ndescription: <b>{description}</b>\n\nremind: <b>{date} {time}</b>'),
        Row(
            Button(Const('Yes'), id='yes', on_click=on_click_set_task),
            Button(Const('No'), id='no', on_click=on_click_edit_task),
        ),
        getter=get_task,
        parse_mode='HTML',
        state=NewTask.confirm
    )
)