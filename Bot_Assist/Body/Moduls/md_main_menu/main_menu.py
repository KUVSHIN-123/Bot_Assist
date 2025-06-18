from aiogram import Router,types,F
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import Bot_Assist.Body.Moduls.keyboards as kb
from Bot_Assist.Head.db_manager import *
from Bot_Assist.Body.Moduls.function import *

main_menu_rt = Router()

@main_menu_rt.message(Command('main_menu'))
async def mm1(message: Message):
    await message.answer('Вы в главном меню',reply_markup=kb.ikb2)