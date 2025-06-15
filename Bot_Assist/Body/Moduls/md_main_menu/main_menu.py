from aiogram import Router,types,F
from aiogram.types import Message
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
import Bot_Assist.Body.Moduls.keyboards as kb
from Bot_Assist.Head.db_manager import data_base_writer,data_base_reader_con1

main_menu_rt = Router()