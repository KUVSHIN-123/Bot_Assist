from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from Bot_Assist.Head.db_manager import data_base_reader_con1

simple_handler_rt = Router()

@simple_handler_rt.message(Command('start'))
async def start(message: Message):
    id = message.from_user.id
    if id == data_base_reader_con1(id):
        await message.answer(f"Здравствуйте {id}")
    else:
        await message.answer(f"Здравствуйте, пройдите регистрацию, {id}")
