from functools import wraps
from aiogram import types

def validate_number(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        try:
            # Try to convert message text to an integer
            task_int  = int(message.text)
            if task_int < 0:
                raise ValueError("Your value must be non-negative.")
        except ValueError as e:
            # If conversion fails or points are invalid, send an error message
            await message.answer(f"Invalid value: {e}")
            return
        # If validation succeeds, call the original handler
        return await func(message, *args, **kwargs)
    return wrapper