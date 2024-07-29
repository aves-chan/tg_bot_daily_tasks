import typing
from datetime import datetime, timedelta

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.database.db_config import ALL_TIME_ZONE
from bot.database.db_question import db_get_user, db_edit_timezone, get_timezone_and_timedelta


async def get_profile(dialog_manager: DialogManager, **kwargs) -> typing.Dict:
    user = db_get_user(telegram_id=dialog_manager.event.from_user.id)
    user_timezone, user_timedelta = get_timezone_and_timedelta(user)
    return {
        'telegram_id': user.telegram_id,
        'username': user.username,
        'firstname': user.first_name,
        'lastname': user.last_name,
        'timezone': user.timezone,
        'user_datetime_now': (datetime.now() + timedelta(hours=user_timedelta)).strftime('%Y-%m-%d %H:%M'),
    }

async def on_clicked_timezone(callback_query: CallbackQuery,
                              button: Button,
                              dialog_manager: DialogManager,
                              ) -> None:
    db_edit_timezone(telegram_id=callback_query.from_user.id, timezone=ALL_TIME_ZONE[callback_query.data])
    await dialog_manager.back()
