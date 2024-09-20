import typing
from datetime import timezone, timedelta, date, datetime
from typing import Dict
import re

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope
from aiogram_dialog.widgets.kbd.calendar_kbd import CalendarScopeView, CalendarDaysView, CalendarMonthView, \
    CalendarYearsView, CalendarUserConfig

from bot.database.db_question import db_get_user, get_timezone_and_timedelta, db_check_title_in_tasks


class CustomCalendar(Calendar):
    def _init_views(self) -> Dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS:
                CalendarDaysView(self._item_callback_data, self.config),
            CalendarScope.MONTHS:
                CalendarMonthView(self._item_callback_data, self.config),
            CalendarScope.YEARS:
                CalendarYearsView(self._item_callback_data, self.config),
        }
    async def _get_user_config(
            self,
            data: Dict,
            dialog_manager: DialogManager,
    ) -> CalendarUserConfig:
        user = db_get_user(dialog_manager.event.from_user.id)
        user_timezone, user_timedelta = get_timezone_and_timedelta(user)
        dialog_manager.dialog_data['user_timezone'] = user_timezone
        dialog_manager.dialog_data['user_timedelta'] = user_timedelta
        return CalendarUserConfig(
            timezone=timezone(timedelta(hours=user_timedelta), user_timezone),
        )

async def check_title_validation(text: str, dialog_manager: DialogManager) -> bool:
    if len(text) > 15:
        await dialog_manager.event.answer(f'You are sending a long title, your size title is {len(text)}')
        return False
    elif db_check_title_in_tasks(telegram_id=dialog_manager.event.from_user.id,
                                 title=text):
        await dialog_manager.event.answer('A task with that name already exists')
        return False
    else:
        return True

async def check_description_validation(text: str, dialog_manager: DialogManager) -> bool:
    if len(text) > 3500:
        await dialog_manager.event.answer(f'You are sending a long description, your size description is {len(text)}')
        return False
    else:
        return True

async def check_date_validation(selected_date: date, dialog_manager: DialogManager) -> bool:
    if selected_date < (datetime.now() + timedelta(hours=dialog_manager.dialog_data['user_timedelta'])).date():
        await dialog_manager.event.answer(text='Choose a date no later than today', show_alert=True)
        return False
    else:
        return True

async def check_time_validation(text: str, dialog_manager: DialogManager) -> typing.Union[datetime, None]:
    regexp = re.compile('(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])')
    if (bool(regexp.match(text))):
        selected_date = dialog_manager.dialog_data.get('selected_date')
        selected_datetime = datetime.combine(datetime.strptime(selected_date, '%Y-%m-%d').date(), datetime.strptime(text, '%H:%M').time())
        if selected_datetime < datetime.now() + timedelta(hours=dialog_manager.dialog_data['user_timedelta']):
            await dialog_manager.event.answer(text='You have sent an outdated date', show_alert=True)
            return None
        else:
            return selected_datetime
