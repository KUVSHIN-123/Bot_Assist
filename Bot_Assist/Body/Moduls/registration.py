from aiogram import Router,types
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from Body.Moduls import keyboards as kb
from Head.db_manager import *
from TOKEN import id_super_user

registration_rt = Router()

class Registration(StatesGroup):
    waiting_data_reg = State()
    confirming_data_reg = State()

#ОБРАБОТЧИК КОМАНДЫ РЕГИСТРАЦИЯ
@registration_rt.message(Command('registration'))
async def registr(message: Message, state: FSMContext):
    id = message.from_user.id                   #ПОЛУЧАЕМ ID ПОЛЬЗОВАТЕЛЯ КОТОРЫЙ ИСПОЛЬЗОВАЛ КОМАНДУ
    id_users = db_users_check('id')             #ПОЛУЧАЕМ СПИСОК ВСЕХ ЗАРАГИСТРИРОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ
    if id_users != []:                          #ЕСЛИ СПИСОК ПОЛЬЗОВАТЕЛЕЙ НЕ ПУСТ
        if id in id_users:                      #ЕСЛИ ID ПОЛЬЗОВАТЕЛЯ ЕСТЬ В СПИСКЕ ЗАРЕГИСТРИРОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ
            if id in id_super_user:             #ЕСЛИ ID ПОЛЬЗОВАТЕЛЕЯ ЕСТЬ В СПИСКЕ СУПЕО ПОЛЬЗОВАТЕЛЕЙ
                await message.answer("Вы уже зарегистрированы, выберите меню /super_main_menu  /main_menu")
                await state.clear()
            else:
                await message.answer("Вы уже зарегистрированы, выберите меню /main_menu")
                await state.clear()
        else:
            await message.answer("Введите данные: Фамилию Имя Отчество",
            reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(Registration.waiting_data_reg)
    else:
        await message.answer("Введите данные: Фамилию Имя Отчество",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Registration.waiting_data_reg)

#ОБРАБОТЧИК ДЛЯ ПРОВЕРКИ ВВЕДЕННЫХ ДАННЫХ
@registration_rt.message(Registration.waiting_data_reg)
async def wait_data(message: Message, state: FSMContext):
    await state.update_data(data_reg=message.text)          #ДОБАВЛЯЕМ ДАННЫЕ ВВЕДЕННЫЕ ПОЛЬЗОВАТЕЛЕМ В ПАМЯТЬ
    await message.answer(f"Проверьте ваши данные: {message.text}, всё верно?", reply_markup=kb.ikb4)
    await state.set_state(Registration.confirming_data_reg)

#ОБРАБОТЧИК ДЛЯ ДОБАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯ В БД ИЛИ ВВЕДЕНИЯ ДАННЫХ ЗАНОВО
@registration_rt.callback_query(Registration.confirming_data_reg)
async def confirm_data(callback: CallbackQuery, state: FSMContext):
    if callback.data == "data accept":                      #ЕСЛИ ПОЛЬЗОВАТЕЛЬ ПОДТВЕРДИЛ ДАННЫЕ
        data = await state.get_data()                       #ВОЗВРАЩАЕМ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ ИЗ ПАМЯТИ
        reg_info = data['data_reg']                         #ПОЛУЧАЕМ ЭТИ ДАННЫЕ
        username = callback.from_user.username              #ПОЛУЧАЕМ USERNAME ПОЛЬЗОВАТЕЛЯ
        id_user = callback.from_user.id                     #ПОЛУЧАЕМ ID ПОЛЬЗОВАТЕЛЯ
        if db_users_add(id_user, reg_info, username) == 1:  #ВЫЗЫВАЕМ ФУНКЦИЮ ЗАПИСИ ПОЛЬЗОВАТЕЛЯ В БД
            if callback.from_user.id in id_super_user:      #ЕСЛИ ID ПОЛЬЗОВАТЕЛЕЯ ЕСТЬ В СПИСКЕ СУПЕО ПОЛЬЗОВАТЕЛЕЙ
                await callback.message.edit_text("Данные подтверждены, регистрация прошла успешно! Выберите меню /super_main_menu  /main_menu")
            else:
                await callback.message.edit_text("Данные подтверждены, регистрация прошла успешно! Выберите меню /main_menu")
        await state.clear()

    elif callback.data == "data incorrect":                 #ЕСЛИ ПОЛЬЗОВАТЕЛЬ ОТКЛОНИЛ ДАННЫЕ
        await callback.message.edit_text("Введите данные заново")
        await state.set_state(Registration.waiting_data_reg)