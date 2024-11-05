# For daily and common tasks because I'm very lazy write them apart 

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

task_manager = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Completed", callback_data="completed")
    ],
    [
        InlineKeyboardButton(text="Delete", callback_data="delete")
    ]

])