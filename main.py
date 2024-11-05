import os
import asyncio

from aiogram import Bot,Dispatcher,types

from data import config
from utils.admin_notify import notify
from utils.user_notify import send_reminders

from handlers.user_private import user_private_router
from handlers.tasks.common_tasks import tasks_router
from handlers.daily.daily_task import daily_router
from handlers.general_handler import general_tasks_router

from common.bot_cmds_list import private

from database.models import conn_db


bot = Bot(token=config.TOKEN)
dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(tasks_router)
dp.include_router(daily_router)
dp.include_router(general_tasks_router)

async def main():
    await conn_db()
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await notify(bot)
    asyncio.create_task(send_reminders(bot))
    

    await dp.start_polling(bot) 

if __name__ == "__main__":
    asyncio.run(main())
