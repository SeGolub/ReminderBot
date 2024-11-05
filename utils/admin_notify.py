import asyncio

from aiogram import types
from aiogram import Bot

from data.config import ADMIN_IDS

async def notify(bot: Bot):
    for admin in ADMIN_IDS:
        await bot.send_message(chat_id=admin, text="Бот Запущен")
    
    