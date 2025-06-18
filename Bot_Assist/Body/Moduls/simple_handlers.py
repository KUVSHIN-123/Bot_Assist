from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from Bot_Assist.Head.db_manager import *

simple_handler_rt = Router()

@simple_handler_rt.message(Command('start'))
async def start(message: Message):
    id = message.from_user.id
    id_users = db_users_check('id')
    print(id_users)
    if id_users != []:
        for i in id_users:
            if id == i:
                await message.answer(f"Здравствуйте {id}")
            else:
                await message.answer(f"Здравствуйте, пройдите регистрацию, {id}")
    else:
        await message.answer(f"Здравствуйте, пройдите регистрацию, {id}")