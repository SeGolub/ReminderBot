from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

daily_inl = InlineKeyboardMarkup( inline_keyboard=[
    [
        InlineKeyboardButton(text="Add Daily Task", callback_data="add daily")
     ],
    [
        InlineKeyboardButton(text="Daily List", callback_data="daily list")
    ],
    [
        InlineKeyboardButton(text="Back", callback_data="back")
    ]

])