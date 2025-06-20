from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from Bot_Assist.Head.db_manager import *
from Bot_Assist.TOKEN import id_super_user

simple_handler_rt = Router()


#ОБРАБОТЧИК КОМАНДЫ СТАРТ
@simple_handler_rt.message(Command('start'))
async def start(message: Message):
    id = message.from_user.id               #ПОЛУЧАЕМ ID ПОЛЬЗОВАТЕЛЯ КОТОРЫЙ ИСПОЛЬЗОВАЛ КОМАНДУ
    id_users = db_users_check('id')         #ПОЛУЧАЕМ СПИСОК ВСЕХ ЗАРАГИСТРИРОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ
    if id_users != []:                      #ЕСЛИ СПИСОК ПОЛЬЗОВАТЕЛЕЙ НЕ ПУСТ
        if id in id_users:                  #ЕСЛИ ID ПОЛЬЗОВАТЕЛЯ ЕСТЬ В СПИСКЕ ЗАРЕГИСТРИРОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ
            if id in id_super_user:         #ЕСЛИ ID ПОЛЬЗОВАТЕЛЕЯ ЕСТЬ В СПИСКЕ СУПЕО ПОЛЬЗОВАТЕЛЕЙ
                await message.answer(f"Здравствуйте! выберите меню /super_main_menu  /main_menu")
            else:
                await message.answer(f"Здравствуйте! выберите меню /main_menu")
        else:
            await message.answer(f"Здравствуйте, пройдите регистрацию /registration")
    else:
        await message.answer(f"Здравствуйте, пройдите регистрацию /registration")