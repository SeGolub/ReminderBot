from datetime import datetime

from aiogram.fsm.state import StatesGroup,State

class TaskReg(StatesGroup):
    task_name = State()
    task_description = State()
    task_point = State()
    task_coins = State()
    