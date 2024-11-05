from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

common_task_inl = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Add task", callback_data="add task")
        ],
        [
            InlineKeyboardButton(text="Task list", callback_data="task list")
        ],
        [
            InlineKeyboardButton(text="Back", callback_data="back")
        ]

    ]
)