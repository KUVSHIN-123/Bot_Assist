from aiogram import Router
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import Body.Moduls.keyboards as kb
from Body.Moduls.keyboards import *
from Head.db_manager import *
from Body.Moduls.function import *
from TOKEN import id_super_user

main_menu_rt = Router()

class Check_tasks(StatesGroup):
    list_tasks = State()
    choice_task = State()

# ОБРАБОТЧИК КОМАНДЫ ГЛАВНОЕ МЕНЮ
@main_menu_rt.message(Command('main_menu'))
async def mm1(message: Message, state: FSMContext):
    await state.clear()
    id = message.from_user.id                                                                   # ПОЛУЧАЕМ ID ПОЛЬЗОВАТЕЛЯ КОТОРЫЙ ИСПОЛЬЗОВАЛ КОМАНДУ
    id_users = db_users_check('id')                                                             # ПОЛУЧАЕМ СПИСОК ВСЕХ ЗАРАГИСТРИРОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ
    if id_users != []:                                                                          # ЕСЛИ СПИСОК ПОЛЬЗОВАТЕЛЕЙ НЕ ПУСТ
        if id in id_users:                                                                      # ЕСЛИ ID ПОЛЬЗОВАТЕЛЯ ЕСТЬ В СПИСКЕ ЗАРЕГИСТРИРОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ
            await message.answer('Вы в главном меню', reply_markup=kb.ikb2)
            await state.set_state(Check_tasks.list_tasks)
        else:
            await message.answer("Пройдите регистрацию /registration")
    else:
        await message.answer("Пройдите регистрацию /registration")

# ВЫВОД СПИСКА ЗАДАНИЙ ПОЛЬЗОВАТЕЛЯ
@main_menu_rt.callback_query(Check_tasks.list_tasks)
async def mm1(callback: CallbackQuery, state: FSMContext):
    list_tasks = db_user_task_check([callback.from_user.id], info='active')             # ПРИНИМАЕМ ВСЕ АКТИВНЫЕ ЗАДАНИЯ ПОЛЬЗОВАТЕЛЯ
    await delete_message(callback.from_user.id, callback.message.message_id)                     # УДАЛЯЕМ ПОСЛЕДНЕЕ СООБЩЕНИЕ
    messages_id = []
    if list_tasks == []:                                                                         # ЕСЛИ СПИСОК ЗАДАНИЙ ПУСТ
        await callback.message.answer('У вас нет активных заданий', reply_markup=None)
    else:
        for i in range(len(list_tasks)):                                                         # ПЕРЕБИРАЕМ СПИСОК ЗАДАНИЙ ПО ДЛИНЕ, ДЛЯ КАЖДОГО ЗАДАНИЯ ИЗ СПИСКА МЫ СОЗДАЕМ СВОЕ СООБЩЕНИЕ И СВОЮ КНОПКУ
            message_id = await callback.message.answer(f'Задание номер: {i+1} \n'           # УКАЗЫВАЕМ НОМЕР ЗАДАНИЯ
                                             f'Название: {list_tasks[i][1]} \n'                  # УКАЗЫВАЕМ НАЗВАНИЕ
                                             f'Описание: {list_tasks[i][2]} \n'                  # УКАЗЫВАЕМ ОПИСАНИЕ
                                             f'Срок выполнения: {list_tasks[i][3]}',             # УКАЗЫВАЕМ СРОК ВЫПОЛНЕНИЯ
                                            reply_markup=builder_list_tasks(list_tasks[i][-2]))  # ИСПОЛЬЗУЕМ БИЛДЕР ДЛЯ СОЗДАНИЯ КНОПОК ДЛЯ КАЖДОГО СООБЩЕНИЯ, callback.data ДЛЯ КНОПОК ЭТО id_task
            messages_id.append(message_id.message_id)                                            # СОХРАНЯЕМ ID КАЖДОГО СООБЩЕНИЯ
        await state.update_data(messages_id=messages_id)                                         # СОХРАНЯЕМ СПИСОК С ID СООБЩЕНИЙ В ПАМЯТЬ
    print(db_user_task_check([callback.from_user.id], 'all'))                      # ВЫВОД ВСЕХ ЗАДАНИЙ ПОЛЬЗОВАТЕЛЯ
    await state.set_state(Check_tasks.choice_task)

# ОБРАБОТЧИК ЗАВЕРШЕНИЯ ЗАДАНИЯ
@main_menu_rt.callback_query(Check_tasks.choice_task)
async def mm1(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()                                                                           # ИЗВЛЕКАЕМ СПИСОК ID СООБЩЕНИЙ ИЗ ПАМЯТИ
    messages_id = data['messages_id']                                                                       # И ПРИСВАИВАЕМ ЭТОТ СПИСОК ПЕРЕМЕННОЙ
    callback_id = callback.message.message_id                                                               # ПРИНИМАЕМ ID СООБЩЕНИЕ КНОПКА КОТОРОГО БЫЛА НАЖАТА
    print(messages_id,callback_id)
    active_tasks = db_user_task_check([callback.from_user.id], info='active')                       # ПРИНИМАЕМ ВСЕ АКТИВНЫЕ ЗАДАНИЯ ПОЛЬЗОВАТЕЛЯ
    for i in messages_id:                                                                                   # ПЕРЕБИРАЕМ КАЖДЫЙ ID СООБЩЕНИЯ
        if i == callback_id:                                                                                # КОГДА НАХОДИМ ID СООБЩЕНИЯ КНОПКА КОТОРОГО БЫЛА НАЖАТА, ТО ПРОПУСКАЕМ ЕГО
            pass
        else:
            await delete_message(chat_id=callback.from_user.id, message_id=i)                               # ВСЕ ОСТАЛЬНЫЕ СООБЩЕНИЯ УДАЛЯЕМ

    id_users = db_users_check('id')                                                                         # ПРИНИМАЕМ ID ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
    if db_user_task_edit(id_users, callback.data) == 1:                                                     # ИСПОЛЬЗУЕМ ФУНКЦИЮ ИЗМЕНЕНИЯ СТАТУСА ЗАДАНИЯ, ОТПРАВЛЯЕМ В НЕГО ID ВСЕХ ПОЛЬЗОВАТЕЛЕЙ И callback.data ТОИСТЬ ID ЗАДАНИЯ
        await callback.message.edit_text('Задание завершено', reply_markup=None)
        for i in active_tasks:                                                                              # НАХОДИМ ЗАДАНИЕ КОТОРОЕ БЫЛО ЗАВЕРШЕНО ПОЛЬЗОВАТЕЛЕМ
            if i[-2] == callback.data:
                await sending_message_admin(id_admin=id_super_user, text=f'Задание: {i[1]}, выполнено!')    # И ОТПРАВЛЯЕМ УВЕДОМЛЕНИЕ АДМИНИСТРАЦИИ О ЗАВЕРШЕНИИ ЗАДАНИЯ