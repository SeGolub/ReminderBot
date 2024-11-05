import asyncio
from aiogram import Bot
from sqlalchemy.future import select
from database.models import async_session, User, Task, Daily

async def send_reminders(bot: Bot):
    while True:
        async with async_session() as session:
            #Take every user from database
            users = await session.scalars(select(User))
            users = users.all()

            #Iterate them with for loop
            for user in users:
                #Select all tasks that attached to User 
                tasks = await session.scalars(select(Task).where(Task.user_id == user.id))
                tasks = tasks.all()
                if tasks:
                    # task_messages = '\n'.join(
                        # f"Task #{task.id}: {task.task_name} - {task.task_description}" for task in tasks)
                    await bot.send_message(user.tg_id, f"Reminder: You have not done all tasks")

                # daily_tasks = await session.scalars(select(DailyTask).where(DailyTask.user_id == user.id))
                # daily_tasks = daily_tasks.all()
                # if daily_tasks:
                #     # daily_task_messages = '\n'.join(
                #     #     f"Daily #{task.id}: {task.daily_name} - {task.daily_description}" for task in daily_tasks)
                #     await bot.send_message(user.tg_id, f"Reminder: You have the following daily tasks:\n{")

        await asyncio.sleep(3600)  
