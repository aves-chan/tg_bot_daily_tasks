from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Row, Cancel
from aiogram_dialog.widgets.text import Const, Format

from bot.dialog.handler_utils import CustomCalendar
from bot.dialog.new_task.new_task_handlers import handler_title, handler_description, on_click_date, \
    on_click_chose_date, handler_time, on_click_edit_task, get_task, on_click_set_task
from bot.states import NewTask

new_task_dialog = Dialog(
    Window(
        Const('Send title please, maximum of 15 characters'),
        MessageInput(func=handler_title, content_types=ContentType.TEXT),
        Cancel(),
        state=NewTask.set_title
    ),
    Window(
        Const('Send description please, maximum of 3500 characters'),
        MessageInput(func=handler_description, content_types=ContentType.TEXT),
        Back(),
        state=NewTask.set_description
    ),
    Window(
        Const('Should I remind you?'),
        Row(
            Button(Const('Yes'), id='yes', on_click=on_click_date),
            Button(Const('No'), id='no', on_click=on_click_date),
        ),
        Back(),
        state=NewTask.date_remind_choose
    ),
    Window(
        Const('Choose date'),
        CustomCalendar(id='calendar', on_click=on_click_chose_date),
        Back(),
        state=NewTask.choose_date,
    ),
    Window(
        Const('Send time like this 22:22 please'),
        MessageInput(func=handler_time, content_types=ContentType.TEXT),
        Back(),
        state=NewTask.choose_time
    ),
    Window(
        Const('Right?'),
        Format('Title: <b>{title}</b>\n\nDescription: <b>{description}</b>\n\nRemind: <b>{selected_datetime}</b>'),
        Row(
            Button(Const('Yes'), id='yes', on_click=on_click_set_task),
            Button(Const('No'), id='no', on_click=on_click_edit_task),
        ),
        getter=get_task,
        parse_mode='HTML',
        state=NewTask.confirm
    )
)