import re

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from states.task_registration import TaskReg

from database.requests import set_task, list_of_tasks, remove_task, get_task_by_id,complete_task
from database.models import Task
from keyboards.common_task_inl.task_inline import common_task_inl
from keyboards.tasks_manage import task_manager

from common.decorators import validate_number

tasks_router = Router()


@tasks_router.callback_query(F.data == "add task")
async def add_task(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.answer("Enter a task's name: ")
    await state.set_state(TaskReg.task_name)
    await callback.answer('')



@tasks_router.message(TaskReg.task_name)
async def set_task_name(message: types.Message, state: FSMContext):
    await state.update_data(task_name=message.text)
    await state.set_state(TaskReg.task_description)
    await message.answer("Task description:")


@tasks_router.message(TaskReg.task_description)
async def set_task_description(message: types.Message, state: FSMContext):
    await state.update_data(task_description=message.text)

    await state.set_state(TaskReg.task_point)
    await message.answer("Task points:")


@tasks_router.message(TaskReg.task_point)
@validate_number
async def set_task_points(message: types.Message, state: FSMContext):
    await state.update_data(task_point=message.text)

    await state.set_state(TaskReg.task_coins)
    await message.answer("Amount of coins: ")


@tasks_router.message(TaskReg.task_coins)
@validate_number
async def set_task_points(message: types.Message, state: FSMContext):
    await state.update_data(task_coins=message.text)
    id = message.from_user.id
    data = await state.get_data()
    await message.answer("Your task registered!😉", reply_markup=common_task_inl)

    await set_task(data,tg_id=id)
    await state.clear()
    


@tasks_router.callback_query(F.data == "task list")
async def task_list(callback: types.CallbackQuery):
    id = callback.from_user.id
    tasks = await list_of_tasks(Task,tg_id=id)
    for task in tasks:
        await callback.message.answer(
            f"Task #{task.id}\n"
            f"Name: {task.task_name}\n"
            f"Description: {task.task_description}\n"
            f"Points: {task.task_point}\n"
            f"Coins: {task.task_coins}",
            reply_markup=task_manager
)


