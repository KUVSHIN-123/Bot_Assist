from Bot_Assist.Head.bot_loader import *

async def sending_message(id_performer,text):
    for id_chat in id_performer:
        await bot.send_message(chat_id=id_chat,text=text)