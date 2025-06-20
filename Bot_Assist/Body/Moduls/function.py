from Bot_Assist.Head.bot_loader import *
from datetime import datetime

# ФУНКЦИЯ ОТПРАВЛЯЕТ СООБЩЕНИЕ ПОЛЬЗОВАТЕЛЯМ
async def sending_message(id_performer,text):
    for chat_id in id_performer:
        await bot.send_message(chat_id=chat_id,text=text)

# ФУНКЦИЯ УДАЛЯЕТ СООБЩЕНИЕ
async def delete_message(chat_id,message_id):
    await bot.delete_message(chat_id=chat_id,message_id=message_id)

# ФУНЦИЯ ОТПРАВЛЯЕТ СООБЩЕНИЕ АДМИНИСТРАЦИИ
async def sending_message_admin(id_admin,text):
    for id in id_admin:
        await bot.send_message(chat_id=id,text=text)


# ФУНЦИЯ ДЛЯ ФОРМИРОВАНИЯ id_task
def build_id_task(_: int = 0):
    now = str(datetime.now())
    date, time = now.split()
    date = date.replace('-','')
    time = time.replace(':','.').replace('.','')
    id_task = date+time
    return id_task