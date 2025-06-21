from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import Body.Moduls.keyboards as kb
from Head.db_manager import *
from Body.Moduls.function import *
from TOKEN import id_super_user
from Body.Moduls.keyboards import *

super_main_menu_rt = Router()


class Super_main_menu(StatesGroup):
    choosing_option = State()
    list_tasks = State()
    wait_name_task = State()
    accept_name_task = State()
    wait_description_task = State()
    accept_description_task = State()
    wait_deadline = State()
    accept_deadline = State()
    wait_performer = State()
    accept_performer = State()
    total_amount = State()


@super_main_menu_rt.message(Command('super_main_menu'))
async def smm(message: Message, state: FSMContext):
    await state.clear()
    id = message.from_user.id
    id_users = db_users_check('id')
    if id_users != []:
        if id in id_users:
            if message.from_user.id in id_super_user:
                await message.answer('Вы в главном меню, выберите один из пунктов ниже', reply_markup=kb.ikb3)
                await state.set_state(Super_main_menu.choosing_option)
            else:
                await message.answer('Вам не доступно это меню, выберите /main_menu')
        else:
            await message.answer(f"Пройдите регистрацию /registration")
    else:
        await message.answer(f"Пройдите регистрацию /registration")


@super_main_menu_rt.callback_query(Super_main_menu.choosing_option)
async def smm1(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'give tasks':
        await callback.message.edit_text('Укажите название задания', reply_markup=None)
        await state.set_state(Super_main_menu.wait_name_task)
    if callback.data == 'check tasks':
        list_users = db_users_check('name_id')

        await callback.message.edit_text('Выберите человека для просмотра заданий:',
                                         reply_markup=builder_list_users(list_users))
        await state.set_state(Super_main_menu.list_tasks)


@super_main_menu_rt.callback_query(Super_main_menu.list_tasks)
async def smm1(callback: CallbackQuery, state: FSMContext):
    id_users = db_users_check('id')
    for i in id_users:
        if i == int(callback.data):
            tasks_list = db_user_task_check([i], 'active')
    await delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    if tasks_list == []:
        await callback.message.answer('У пользователя нет активных заданий',reply_markup=None)
    else:
        for i in range(len(tasks_list)):
            await callback.message.answer(f'Задание номер: {i+1} \n'
                                          f'Название: {tasks_list[i][1]} \n'
                                          f'Описание: {tasks_list[i][2]} \n'
                                          f'Срок выполнения: {tasks_list[i][3]}', reply_markup=None)
@super_main_menu_rt.message(Super_main_menu.wait_name_task)
async def smm2(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f'Подтвердите название: \n {message.text}', reply_markup=kb.ikb5)
    await state.set_state(Super_main_menu.accept_name_task)


@super_main_menu_rt.callback_query(Super_main_menu.accept_name_task)
async def smm1(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'accept':
        await callback.message.edit_text('Добавьте описание к заданию', reply_markup=None)
        await state.set_state(Super_main_menu.wait_description_task)
    if callback.data == 'edit':
        await callback.message.edit_text(f'Укажите название заново \n')
        await state.set_state(Super_main_menu.wait_name_task)


@super_main_menu_rt.message(Super_main_menu.wait_description_task)
async def smm2(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(f'Подтвердите описание: \n {message.text}', reply_markup=kb.ikb5)
    await state.set_state(Super_main_menu.accept_description_task)


@super_main_menu_rt.callback_query(Super_main_menu.accept_description_task)
async def smm3(callback: CallbackQuery, state: FSMContext):
    if callback.data == "accept":
        await callback.message.edit_text('Укажите срок выполнения по следующему примеру:\n'
                                         'ГГГГ/ММ/ЧЧ/ ЧАС \n'
                                         'Например: 2025/06/20 15', reply_markup=None)
        await state.set_state(Super_main_menu.wait_deadline)
    elif callback.data == "edit":
        await callback.message.edit_text('Напишите описание заново', reply_markup=None)
        await state.set_state(Super_main_menu.wait_description_task)


@super_main_menu_rt.message(Super_main_menu.wait_deadline)
async def smm4(message: Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    await message.answer(f'Подтвердите срок выполнения: \n {message.text}', reply_markup=kb.ikb5)
    await state.set_state(Super_main_menu.accept_deadline)


@super_main_menu_rt.callback_query(Super_main_menu.accept_deadline)
async def smm5(callback: CallbackQuery, state: FSMContext):
    if callback.data == "accept":
        user_num_name = db_users_check('num_name')
        table = 'Список пользователей: \n'
        for i in range(len(user_num_name)):
            table += f'{user_num_name[i][0]}. {user_num_name[i][1]} {user_num_name[i][2]} \n'
        await callback.message.answer(f'{table}')
        await callback.message.edit_text('Выберите исполнителя/лей из списка по следующему примеру: \n'
                                         'номер/номер/номер и тд.', reply_markup=None)
        await state.set_state(Super_main_menu.wait_performer)
    elif callback.data == "edit":
        await callback.message.edit_text('Укажите срок выполнения заново', reply_markup=None)
        await state.set_state(Super_main_menu.wait_deadline)


@super_main_menu_rt.message(Super_main_menu.wait_performer)
async def smm6(message: Message, state: FSMContext):
    await state.update_data(performer=message.text)
    await message.answer(f'Подтвердите выбор: \n {message.text}', reply_markup=kb.ikb5)
    await state.set_state(Super_main_menu.accept_performer)


@super_main_menu_rt.callback_query(Super_main_menu.accept_performer)
async def smm7(callback: CallbackQuery, state: FSMContext):
    if callback.data == "accept":
        data = await state.get_data()
        name = data['name']
        description = data['description']
        deadline = data['deadline']
        num_performer = data['performer']
        name_performer = db_user_num_to_id(num_performer=num_performer)
        table = ''
        for i in range(len(name_performer)):
            table += f'{i + 1}. {name_performer[i][0]} {name_performer[i][1]} \n'
        await callback.message.edit_text('Подтвердите отправку задания: \n'
                                         f'Название: {name} \n'
                                         f'Описание: {description} \n'
                                         f'Срок выполнения: {deadline} \n'
                                         f'Ответственный: {table}'
                                         , reply_markup=kb.ikb6)
        await state.set_state(Super_main_menu.total_amount)
    elif callback.data == "edit":
        await callback.message.edit_text('Укажите исполнителя/ей заново', reply_markup=None)
        await state.set_state(Super_main_menu.wait_performer)


@super_main_menu_rt.callback_query(Super_main_menu.total_amount)
async def smm6(callback: CallbackQuery, state: FSMContext):
    if callback.data == "sending accept":
        data = await state.get_data()
        task = []
        task.append(data['name'])
        task.append(data['description'])
        task.append(data['deadline'])
        num_performer = data['performer']
        id_performer = db_user_num_to_id(num_performer=num_performer, id=1)
        id_task = build_id_task()
        task.append(id_performer)
        task.append(num_performer)
        task.append(id_task)
        if db_user_task_add(task) == 1:
            await callback.message.edit_text('Задание отправлено.', reply_markup=None)
            text = (f'У вас новое задание: \n'
                    f'Название: {task[0]} \n'
                    f'Описание: {task[1]} \n'
                    f'Срок выполнения: {task[2]}')
            await sending_message(id_performer=id_performer, text=text)
            print(db_user_task_check(id_performer, 'all'))
            await state.clear()
    elif callback.data == "cancel sending":
        await callback.message.edit_text('Вы в главном меню, выберите один из пунктов ниже', reply_markup=kb.ikb3)
        await state.set_state(Super_main_menu.choosing_option)
