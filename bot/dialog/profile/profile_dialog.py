import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Cancel, SwitchTo, Radio, Row, Group, Button
from aiogram_dialog.widgets.text import Const, Format

from bot.database.db_config import ALL_TIME_ZONE
from bot.dialog.profile.profile_handlers import get_profile, on_clicked_timezone
from bot.states import PofileSG


profile_dialog = Dialog(
    Window(
        Format('''
id: <tg-spoiler>{telegram_id}</tg-spoiler>

firstname: <b>{firstname}</b>

lastname: <b>{lastname}</b>

username: <b>{username}</b>

time zone: <b>{timezone}</b>

your date and time: <b>{user_datetime_now}</b>'''),
        SwitchTo(Const('Change the time zone'), id='C_TimeZone', state=PofileSG.change_timezone),
        Cancel(),
        getter=get_profile,
        parse_mode='HTML',
        state=PofileSG.profile
    ),
    Window(
        Const('Chose time zone. Selected time zone:'),
        Group(
            Button(Const(ALL_TIME_ZONE['UTC']), id='UTC', on_click=on_clicked_timezone),
            Button(Const(ALL_TIME_ZONE['KALT']), id='KALT', on_click=on_clicked_timezone),
            Button(Const(ALL_TIME_ZONE['MSK']), id='MSK', on_click=on_clicked_timezone),
            Button(Const(ALL_TIME_ZONE['SAMT']), id='SAMT', on_click=on_clicked_timezone),
            Button(Const(ALL_TIME_ZONE['YEKT']), id='YEKT', on_click=on_clicked_timezone),
            Button(Const(ALL_TIME_ZONE['OMST']), id='OMST', on_click=on_clicked_timezone),
            Button(Const(ALL_TIME_ZONE['KRAT']), id='KRAT', on_click=on_clicked_timezone),
            Button(Const(ALL_TIME_ZONE['IRKT']), id='IRKT', on_click=on_clicked_timezone),
            Button(Const(ALL_TIME_ZONE['YAKT']), id='YAKT', on_click=on_clicked_timezone),
            Button(Const(ALL_TIME_ZONE['VLAT']), id='VLAT', on_click=on_clicked_timezone),
            Button(Const(ALL_TIME_ZONE['MAGT']), id='MAGT', on_click=on_clicked_timezone),
            Button(Const(ALL_TIME_ZONE['PETT']), id='PETT', on_click=on_clicked_timezone),
            width=2
        ),
        Back(),
        state=PofileSG.change_timezone
    )
)
