from aiogram.filters.state import State, StatesGroup


class MainSG(StatesGroup):
    main = State()

class PofileSG(StatesGroup):
    profile = State()
    change_timezone = State()

class NewTask(StatesGroup):
    set_title = State()
    set_description = State()
    date_remind_choose = State()
    choose_date = State()
    choose_time = State()
    confirm = State()

class AllTasks(StatesGroup):
    all_tasks = State()
    about_task = State()
    delete_task = State()
    choose_edit_title_or_description = State()
    edit_title = State()
    edit_description = State()
    choose_edit_remind = State()
    edit_time = State()
    edit_date = State()
    remove_remind = State()




