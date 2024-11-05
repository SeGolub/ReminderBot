from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

task_inline = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Common tasks", callback_data="switch_to_task")    
    ],
    [
        InlineKeyboardButton(text="Daily tasks", callback_data="switch_to_daily")

    ]
]
)