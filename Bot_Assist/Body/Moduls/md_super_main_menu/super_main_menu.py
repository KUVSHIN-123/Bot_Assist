from aiogram import Router,types,F
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import Bot_Assist.Body.Moduls.keyboards as kb
from Bot_Assist.Head.db_manager import data_base_writer,data_base_reader_con2
super_main_menu_rt = Router()

id_super_user = [5132538999]

class Super_main_menu(StatesGroup):
    choosing_option=State()
    wait_task = State()
    accept_task = State()
    wait_deadline = State()
    accept_deadline = State()
    wait_performer = State()
    accept_performer = State()
    total_amount = State()

@super_main_menu_rt.message(Command('super_main_menu'))
async def smm(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id in id_super_user:
        await message.answer('Вы в главном меню, выберите один из пунктов ниже.',reply_markup=kb.ikb3)
        await state.set_state(Super_main_menu.choosing_option)
    else:
        await message.answer('Вам не доступно это меню, выберите /main_menu')

@super_main_menu_rt.callback_query(Super_main_menu.choosing_option)
async def smm1(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'give tasks':
        await callback.message.edit_text('Напишите задание',reply_markup=None)
        await state.set_state(Super_main_menu.wait_task)
    if callback.data == 'check tasks':
        await callback.message.edit_text(f'Выберите человека для просмотра заданий: \n')

@super_main_menu_rt.message(Super_main_menu.wait_task)
async def smm2(message: Message, state: FSMContext):
    await message.answer(f'Подтвердите задание: \n {message.text}', reply_markup=kb.ikb5)
    await state.set_state(Super_main_menu.accept_task)

@super_main_menu_rt.callback_query(Super_main_menu.accept_task)
async def smm3(callback: CallbackQuery, state: FSMContext):
    if callback.data == "task accept":
        await callback.message.edit_text('Укажите срок выполнения по следующему примеру:\n'
                                         'ГГГГ/ММ/ЧЧ',reply_markup=None)
        await state.set_state(Super_main_menu.wait_deadline)
    elif callback.data == "task rewrite" or callback.data == "fill task again":
        await callback.message.edit_text('Напишите задание заново',reply_markup=None)
        await state.set_state(Super_main_menu.wait_task)

@super_main_menu_rt.message(Super_main_menu.wait_deadline)
async def smm4(message: Message, state: FSMContext):
    await message.answer(f'Подтвердите срок выполнения: \n {message.text}', reply_markup=kb.ikb6)
    await state.set_state(Super_main_menu.accept_deadline)

@super_main_menu_rt.callback_query(Super_main_menu.accept_deadline)
async def smm5(callback: CallbackQuery, state: FSMContext):
    if callback.data == "accept":
        await callback.message.edit_text('Выберите исполнителя/лей из списка по следующему примеру: \n'
                                         'id/id/id и тд.',reply_markup=None)
        await state.set_state(Super_main_menu.wait_performer)
    elif callback.data == "edit":
        await callback.message.edit_text('Укажите срок выполнения заново',reply_markup=None)
        await state.set_state(Super_main_menu.wait_deadline)

@super_main_menu_rt.message(Super_main_menu.wait_performer)
async def smm6(message: Message, state: FSMContext):
    await message.answer(f'Подтвердите выбор: \n {message.text}', reply_markup=kb.ikb7)
    await state.set_state(Super_main_menu.accept_performer)

@super_main_menu_rt.callback_query(Super_main_menu.accept_performer)
async def smm7(callback: CallbackQuery, state: FSMContext):
    if callback.data == "choice accept":
        await callback.message.edit_text('Подтвердите отправку задания:',reply_markup=kb.ikb8)
        await state.set_state(Super_main_menu.total_amount)
    elif callback.data == "choice edit":
        await callback.message.edit_text('Укажите исполнителя/ей заново',reply_markup=None)
        await state.set_state(Super_main_menu.wait_performer)

@super_main_menu_rt.callback_query(Super_main_menu.total_amount)
async def smm6(callback: CallbackQuery, state: FSMContext):
    if callback.data == "sending accept":
        await callback.message.edit_text('Задание отправлено.', reply_markup=None)
        await state.clear()
    elif callback.data == "cancel sending":
        await callback.message.edit_text('Вы в главном меню, выберите один из пунктов ниже.',reply_markup=kb.ikb3)
        await state.set_state(Super_main_menu.choosing_option)