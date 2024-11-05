import re

from aiogram import Router,types,F

from keyboards.common_task_inl.task_inline import common_task_inl
from keyboards.daily_tasks_inline.daily_inline import daily_inl
from keyboards.start_inline import task_inline

from database.requests import complete_task,remove_task,get_task_by_id
from database.models import Task, Daily

from common.user_text import quick_text

general_tasks_router = Router()

@general_tasks_router.callback_query(F.data=="switch_to_task")
async def switch_common(callback: types.CallbackQuery):
    await callback.message.edit_text("Common tasks", reply_markup=common_task_inl)
    await callback.answer("")


@general_tasks_router.callback_query(F.data=="switch_to_daily")
async def switch_common(callback: types.CallbackQuery):
    await callback.message.edit_text("Daily tasks", reply_markup=daily_inl)
    await callback.answer("")

@general_tasks_router.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.edit_text(text=quick_text, reply_markup=task_inline)
    await callback.answer("")


@general_tasks_router.callback_query(F.data=="completed")
async def set_task_complete(callback: types.CallbackQuery): 
    await callback.answer("")
    TASK_CLASSES = {
        "Task": Task,
        "Daily": Daily
    }
    message_text = callback.message.text
    user_tg_id = callback.from_user.id
    pattern = re.match(r'([^\n]*)', message_text)
    components = pattern.group(1).split()


    task_class = components[0] 
    task_id = int(components[1][1:])

    task = await get_task_by_id(task_class = TASK_CLASSES[task_class], tg_id = user_tg_id, task_id = task_id)

    await complete_task(task_class=TASK_CLASSES[task_class],
                        task_id=task.id,
                        points=task.task_point,
                        coins=task.task_coins,
                        tg_id=user_tg_id)

    await callback.message.answer("You complete your task🤑")
    await callback.message.delete()

@general_tasks_router.callback_query(F.data=="delete")
async def delete_task(callback: types.CallbackQuery):
    await callback.answer('')
    message_text = callback.message.text
    user_id = callback.from_user.id
    task_id = 0
    task_class = Task

    task_id_match = re.search(r'Task #(\d+)', message_text)
    daily_id_match = re.search(r'Daily #(\d+)', message_text)
    if task_id_match:
        task_id = int(task_id_match.group(1))
    
    if daily_id_match:
        task_id = int(daily_id_match.group(1))
        task_class = Daily
    
    await remove_task(task_class=task_class, task_id=task_id, tg_id=user_id )
    await callback.message.answer("You delete your task 😢")
    await callback.message.delete()

    




    

    



    
    


