from aiogram import types,Router,F
from aiogram.filters import CommandStart,Command

from keyboards.start_inline import task_inline

import database.requests as rq

from common.user_text import welcome_text,quick_text,help_text


user_private_router = Router()


@user_private_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(text=welcome_text)
    await rq.set_user(message.from_user.id)


@user_private_router.message((F.text =="/quick_start") | (F.text == "quick start") )
async def quick_guide(message: types.Message):
    await message.answer(text=quick_text, reply_markup=task_inline)


@user_private_router.message(F.text == '/stats')
async def user_stats(message: types.Message):
    stats = await rq.get_user_stats(message.from_user.id)
    await message.answer((
        "User Stats below\n"
        f"User Level: {stats['user_level']}\n"
        f"User Coins: {stats['user_coins']}\n"
        f"User Exp: {stats['user_exp']}\n"
        f"User Streak: {stats['user_streak']}"
    ))


@user_private_router.message((F.text == "help") | (F.text == "/help") )
async def help(message: types.Message):
    await message.answer(text=help_text)















