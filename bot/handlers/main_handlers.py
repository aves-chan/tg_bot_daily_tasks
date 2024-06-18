from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from bot.states import MainSG
from bot.keyboards.main_keyboards import kb_main, kb_profile

main_router = Router()

@main_router.message(CommandStart())
@main_router.callback_query(StateFilter(MainSG.profile), F.data == 'back')
async def start(message: types.Message, state: FSMContext):
    await state.set_state(MainSG.main)
    await message.answer(text='Main menu', reply_markup=kb_main())

@main_router.callback_query(StateFilter(MainSG.profile), F.data == 'profile')
async def profile(cd: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainSG.profile)
    text = f"""
firstname: {cd.from_user.first_name}
lastname: {cd.from_user.last_name}
username: {cd.from_user.username}
"""
    await cd.message.edit_text(text=text, reply_markup=kb_profile())

@main_router.callback_query(StateFilter(MainSG.profile), F.data == 'back')
async def profile_back(cd: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainSG.main)
    await cd.message.edit_text(text='Main menu', reply_markup=kb_main())