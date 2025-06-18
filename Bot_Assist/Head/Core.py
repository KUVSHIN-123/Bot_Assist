
from bot_loader import *
from Bot_Assist.Body.Moduls.simple_handlers import simple_handler_rt
from Bot_Assist.Body.Moduls.md_super_main_menu.super_main_menu import super_main_menu_rt
from Bot_Assist.Body.Moduls.md_main_menu.main_menu import main_menu_rt
from Bot_Assist.Body.Moduls.registration import registration_rt

import asyncio
import logging




dp.include_router(simple_handler_rt)
dp.include_router(super_main_menu_rt)
dp.include_router(main_menu_rt)
dp.include_router(registration_rt)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())