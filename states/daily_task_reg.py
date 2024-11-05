from aiogram.fsm.state import State,StatesGroup

class DailyReg(StatesGroup):

    daily_name = State()
    daily_description = State()
    daily_points = State()
    daily_coins = State()