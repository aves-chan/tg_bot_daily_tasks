import operator

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Row, Cancel, Checkbox, Select, ScrollingGroup, SwitchTo, Calendar
from aiogram_dialog.widgets.text import Const, Format

from bot.dialog.all_tasks.all_tasks_handlers import on_clicked_task, get_tasks_by_id, \
    delete_task, handler_edit_title, handler_edit_description, on_click_edit_date, remove_remind, handler_edit_time, \
    on_clicked_completion_task
from bot.dialog.all_tasks.all_tasks_handlers import get_task
from bot.states import AllTasks


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
        getter=get_tasks_by_id,
        state=AllTasks.all_tasks
    ),
    Window(
        Format('<b>{title}</b>\n\n<b>{description}</b>\n\nremind: <b>{date} {time}</b>'),
        Button(Format('{completion}'), id='compl', on_click=on_clicked_completion_task),
        Row(
            SwitchTo(Const('edit reminder'), id='edit_reminder', state=AllTasks.choose_edit_remind),
            SwitchTo(Const('edit task'), id='edit_task', state=AllTasks.choose_edit_title_or_description)
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
        SwitchTo(Const('Back'), id='c_back', state=AllTasks.about_task),
        state=AllTasks.choose_edit_title_or_description
    ),
    Window(
        Const('send title please, maximum of 15 characters'),
        MessageInput(func=handler_edit_title, content_types=ContentType.TEXT),
        SwitchTo(Const('Back'), id='t_back', state=AllTasks.choose_edit_title_or_description),
        state=AllTasks.edit_title
    ),
    Window(
        Const('send description please, maximum of 3500 characters'),
        MessageInput(func=handler_edit_description, content_types=ContentType.TEXT),
        SwitchTo(Const('Back'), id='t_back', state=AllTasks.choose_edit_title_or_description),
        state=AllTasks.edit_description
    ),
    Window(
        Const('choose what you will change'),
        Row(
            SwitchTo(Const('edit'), id='e_edit', state=AllTasks.edit_date),
            SwitchTo(Const('remove'), id='e_remove', state=AllTasks.remove_remind),
        ),
        SwitchTo(Const('Back'), id='c_back', state=AllTasks.about_task),
        state=AllTasks.choose_edit_remind
    ),
    Window(
        Const('choose date'),
        Calendar(id='calendar', on_click=on_click_edit_date),
        SwitchTo(Const('Back'), id='e_back', state=AllTasks.choose_edit_remind),
        state=AllTasks.edit_date,
    ),
    Window(
        Const('send time like this 22:22 please'),
        MessageInput(func=handler_edit_time, content_types=ContentType.TEXT),
        SwitchTo(Const('Back'), id='e_back', state=AllTasks.edit_date),
        state=AllTasks.edit_time
    ),
    Window(
        Const('are you sure you want to remove the reminder'),
        Row(
            SwitchTo(Const('Yes'), id='yes', state=AllTasks.about_task, on_click=remove_remind),
            SwitchTo(Const('Back'), id='back', state=AllTasks.about_task)
        ),
        state=AllTasks.remove_remind
    )
)
