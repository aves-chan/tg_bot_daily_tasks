from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Row, Cancel, Calendar
from aiogram_dialog.widgets.text import Const, Format

from bot.dialog.new_task.new_task_handlers import handler_title, handler_description, on_click_date, \
    on_click_chose_date, handler_time, on_click_set_task, on_click_edit_task, get_task
from bot.states import NewTask

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