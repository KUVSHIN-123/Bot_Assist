from aiogram import Router,types
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from Bot_Assist.Body.Moduls import keyboards as kb
from Bot_Assist.Head.db_manager import *

registration_rt = Router()

class Registration(StatesGroup):
    waiting_data_reg = State()
    confirming_data_reg = State()

@registration_rt.message(Command('registration'))
async def registr(message: Message, state: FSMContext):
    id = message.from_user.id
    id_users = db_users_check('id')
    if id_users != []:
        for i in id_users:
            if id == i:
                await message.answer("Вы уже зарегистрированы")
                await state.clear()
            else:
                await message.answer("Введите данные: Фамилию Имя Отчество",
                reply_markup=types.ReplyKeyboardRemove())
                await state.set_state(Registration.waiting_data_reg)
    else:
        await message.answer("Введите данные: Фамилию Имя Отчество",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Registration.waiting_data_reg)
@registration_rt.message(Registration.waiting_data_reg)
async def wait_data(message: Message, state: FSMContext):
    await state.update_data(data_reg=message.text)
    await message.answer(f"Проверьте ваши данные: {message.text}, всё верно?", reply_markup=kb.ikb4)
    await state.set_state(Registration.confirming_data_reg)

@registration_rt.callback_query(Registration.confirming_data_reg)
async def confirm_data(callback: CallbackQuery, state: FSMContext):
    if callback.data == "data accept":
        data = await state.get_data()
        reg_info = data['data_reg']
        username = callback.from_user.username
        id_user = callback.from_user.id
        if db_users_add(id_user, reg_info, username) == 1:
            await callback.message.edit_text("Данные подтверждены, регистрация прошла успешно!")
        await state.clear()

    elif callback.data == "data incorrect":
        await callback.message.edit_text("Введите данные заново")
        await state.set_state(Registration.waiting_data_reg)