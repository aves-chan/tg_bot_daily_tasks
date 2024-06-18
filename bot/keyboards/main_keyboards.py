from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

def kb_main() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='my tasks', callback_data='my tasks')
    keyboard.button(text='new task', callback_data='new task')
    keyboard.button(text='profile', callback_data='profile')
    keyboard.adjust(2, 1)
    return keyboard.as_markup()

def kb_profile() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='back', callback_data='back')
    return keyboard.as_markup()