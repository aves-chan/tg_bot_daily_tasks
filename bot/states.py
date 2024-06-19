from aiogram.filters.state import State, StatesGroup


class MainSG(StatesGroup):
    main = State()
    profile = State()

class NewTask(StatesGroup):
    set_title = State()
    set_description = State()
    date_remind_choose = State()
    choose_date = State()
    choose_time = State()
    confirm = State()

class AllTasks(StatesGroup):
    choose_task = State()
    about_task = State()



