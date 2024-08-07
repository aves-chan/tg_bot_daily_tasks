import operator

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Row, Cancel, Select, ScrollingGroup, SwitchTo, Calendar
from aiogram_dialog.widgets.text import Const, Format

from bot.dialog.all_tasks.all_tasks_handlers import on_clicked_task, get_tasks_by_id, on_clicked_completion_task, \
    get_task, delete_task, handler_edit_title, handler_edit_description, handler_edit_time, on_click_edit_date, \
    remove_remind, get_count_tasks, handler_delete_all_tasks, on_clicked_delete_all_tasks
from bot.dialog.handler_utils import CustomCalendar
from bot.states import AllTasks

all_tasks_dialog = Dialog(
    Window(
        Const('All tasks'),
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
        Button(Const('Delete all tasks'), id='DelAllTasks', on_click=on_clicked_delete_all_tasks),
        Cancel(),
        getter=get_tasks_by_id,
        state=AllTasks.all_tasks
    ),
    Window(
        Const('Are you sure you want to delete all task?'),
        SwitchTo(Const('Delete all task'), id='DelAllTasks', state=AllTasks.confirmation_of_deletion_of_all_tasks),
        Back(),
        state=AllTasks.delete_all_tasks
    ),
    Window(
        Format('Send me "I want to delete all tasks", you have {count_tasks} tasks'),
        MessageInput(func=handler_delete_all_tasks, content_types=ContentType.TEXT),
        Back(),
        getter=get_count_tasks,
        state=AllTasks.confirmation_of_deletion_of_all_tasks
    ),
    Window(
        Format('<b>{title}</b>\n\n<b>{description}</b>\n\nRemind: <b>{datetime}</b>'),
        Button(Format('{completion}'), id='compl', on_click=on_clicked_completion_task),
        Row(
            SwitchTo(Const('Edit reminder'), id='edit_reminder', state=AllTasks.choose_edit_remind),
            SwitchTo(Const('Edit task'), id='edit_task', state=AllTasks.choose_edit_title_or_description)
        ),
        SwitchTo(Const('Delete task'), id='delete_task', state=AllTasks.delete_task),
        SwitchTo(Const('Back'), id='Back', state=AllTasks.all_tasks),
        getter=get_task,
        parse_mode='HTML',
        state=AllTasks.about_task
    ),
    Window(
        Const('Are you sure you want to delete the task?'),
        Button(Const('Yes'), id='yes', on_click=delete_task),
        Back(),
        state=AllTasks.delete_task
    ),
    Window(
        Const('Choose what you will change'),
        Row(
            SwitchTo(Const('Title'), id='e_title', state=AllTasks.edit_title),
            SwitchTo(Const('Description'), id='e_description', state=AllTasks.edit_description),
        ),
        SwitchTo(Const('Back'), id='c_back', state=AllTasks.about_task),
        state=AllTasks.choose_edit_title_or_description
    ),
    Window(
        Const('Send title please, maximum of 15 characters'),
        MessageInput(func=handler_edit_title, content_types=ContentType.TEXT),
        SwitchTo(Const('Back'), id='t_back', state=AllTasks.choose_edit_title_or_description),
        state=AllTasks.edit_title
    ),
    Window(
        Const('Send description please, maximum of 3500 characters'),
        MessageInput(func=handler_edit_description, content_types=ContentType.TEXT),
        SwitchTo(Const('Back'), id='t_back', state=AllTasks.choose_edit_title_or_description),
        state=AllTasks.edit_description
    ),
    Window(
        Const('Choose what you will change'),
        Row(
            SwitchTo(Const('Edit reminder'), id='e_edit', state=AllTasks.edit_date),
            SwitchTo(Const('Remove'), id='e_remove', state=AllTasks.remove_remind),
        ),
        SwitchTo(Const('Back'), id='c_back', state=AllTasks.about_task),
        state=AllTasks.choose_edit_remind
    ),
    Window(
        Const('Choose date'),
        CustomCalendar(id='calendar', on_click=on_click_edit_date),
        SwitchTo(Const('Back'), id='e_back', state=AllTasks.choose_edit_remind),
        state=AllTasks.edit_date,
    ),
    Window(
        Const('Send time like this 22:22 please'),
        MessageInput(func=handler_edit_time, content_types=ContentType.TEXT),
        SwitchTo(Const('Back'), id='e_back', state=AllTasks.edit_date),
        state=AllTasks.edit_time
    ),
    Window(
        Const('Are you sure you want to remove the reminder'),
        Row(
            SwitchTo(Const('Yes'), id='yes', state=AllTasks.about_task, on_click=remove_remind),
            SwitchTo(Const('Back'), id='back', state=AllTasks.about_task)
        ),
        state=AllTasks.remove_remind
    )
)
