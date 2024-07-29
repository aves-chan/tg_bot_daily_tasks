from datetime import timezone, timedelta
from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope
from aiogram_dialog.widgets.kbd.calendar_kbd import CalendarScopeView, CalendarDaysView, CalendarMonthView, \
    CalendarYearsView, CalendarUserConfig

from bot.database.db_question import db_get_user, get_timezone_and_timedelta


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
