from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from states.daily_task_reg import DailyReg
from database.models import Daily
from database.requests import set_daily_task,list_of_tasks


from common.decorators import validate_number
from keyboards.tasks_manage import task_manager
from keyboards.daily_tasks_inline.daily_inline import daily_inl


daily_router = Router()

@daily_router.callback_query(F.data == "add daily")
async def daily_first_step(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Enter your daily task name:")
    await state.set_state(DailyReg.daily_name)
    await callback.answer('')

@daily_router.message(DailyReg.daily_name)
async def daily_second_step(message: types.Message, state: FSMContext):
    await state.update_data(daily_name = message.text)
    await state.set_state(DailyReg.daily_description)
    await message.answer("Enter description for your daily:")

@daily_router.message(DailyReg.daily_description)
async def daily_third_step(message: types.Message, state: FSMContext):
    await state.update_data(daily_description = message.text)
    await state.set_state(DailyReg.daily_points)
    await message.answer("Enter amount points:")

@daily_router.message(DailyReg.daily_points)
@validate_number
async def daily_fourth_step(message: types.Message, state: FSMContext):
    await state.update_data(daily_points = int(message.text))
    await state.set_state(DailyReg.daily_coins)
    await message.answer("Enter amount of coins:")


@daily_router.message(DailyReg.daily_coins)
@validate_number
async def daily_fifth_step(message: types.Message, state: FSMContext):
    await state.update_data(daily_coins = int(message.text))
    id = message.from_user.id
    data = await state.get_data()

    await set_daily_task(data, tg_id=id)
    await state.clear()
    await message.answer("Your daily task is registered!", reply_markup=daily_inl)


@daily_router.callback_query(F.data=="daily list")
async def daily_list(callback: types.CallbackQuery):
    id = callback.from_user.id
    await callback.message.answer(f"Fetching daily tasks for user ID: {id}")    
    dailies = await list_of_tasks(Daily, tg_id=id)
    for daily in dailies:
        await callback.message.answer(
            f"Daily #{daily.id}\n"
            f"Name: {daily.daily_name}\n"
            f"Description: {daily.daily_description}\n"
            f"Points: {daily.daily_point}\n"
            f"Coins: {daily.daily_coins}\n"
            f"Streak: {daily.daily_streak}",
            reply_markup=task_manager
)
    
