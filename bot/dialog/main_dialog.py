from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const

from bot.states import AllTasks, NewTask, MainSG, PofileSG

main_dialog = Dialog(
    Window(
        Const('Main menu'),
        Row(
            Start(Const('My tasks'), id='my_tasks', state=AllTasks.all_tasks),
            Start(Const('New tasks'), id='new_tasks', state=NewTask.set_title)
        ),
        Start(Const('Profile'), id='profile', state=PofileSG.profile),
        state=MainSG.main
    ),
)
