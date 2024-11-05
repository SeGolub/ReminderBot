from datetime import datetime,timedelta

from sqlalchemy import select,delete,update
from sqlalchemy.exc import SQLAlchemyError

from database.models import User,Task,Daily
from database.models import async_session

NEXT_LEVEL = 100

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, user_level=1, user_exp=0, user_coins=0))
            await session.commit()


async def set_task(data, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            session.add(Task(task_name=data['task_name'], task_description=data['task_description'], task_point=data['task_point'], task_coins=data['task_coins'], user=user))
            await session.commit()

async def get_task_by_id(task_class, tg_id, task_id):
    # Returns task by id

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id==tg_id))
        if user:
            task = await session.scalar(select(task_class).where(task_class.id==task_id))
            return task

async def list_of_tasks(task_class, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            now = datetime.utcnow()
            today_midnight = datetime(now.year, now.month, now.day)
            
            
            # Filter tasks based on last completion time
            if task_class == Daily:
                result = await session.scalars(
                    select(task_class)
                    .where(task_class.user_id == user.id)
                    .where(
                        (task_class.last_completed_at.is_(None)) |
                        (task_class.last_completed_at < today_midnight))
                    )
            else:
                result = await session.scalars(
                    select(task_class)
                    .where(task_class.user_id == user.id)
                )
            tasks = result.all()
            return tasks
        
    
async def remove_task(task_class,task_id, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            task = await session.scalar(select(task_class).where(task_class.id==task_id))
            if task and task.user_id == user.id:
                await session.execute(delete(task_class).where(task_class.id == task_id))
                await session.commit()


async def complete_task(task_class,task_id, points, coins, tg_id):
    global NEXT_LEVEL
    async with async_session() as session:
        task = await session.scalar(select(task_class).where(task_class.id==task_id))
        user = await session.scalar(select(User).where(User.tg_id==tg_id))

        #Check if task and user are connected
        if task and user and task.user_id == user.id:

            new_exp = user.user_exp + points 
            exp = new_exp // NEXT_LEVEL #if exp is more than NEXT_LEVEL it will add new lever to user
            if exp >= 1:
                new_exp = new_exp % NEXT_LEVEL
                NEXT_LEVEL += 10
                new_user_level = user.user_level + 1
            else:
                new_user_level = user.user_level

            await session.execute(
                update(User)
                .where(User.tg_id==tg_id)
                .values(user_level=new_user_level,
                        user_exp=new_exp, 
                        user_coins = user.user_coins+coins)
                )
            # Daily Task will repeat every day
            if task_class == Task:
                await session.execute(delete(task_class).where(task_class.id == task_id))
            # Update the last completed time for the daily task
            if task_class == Daily:
                new_streak = task.daily_streak + 1
                await session.execute(
                    update(Daily)
                    .where(Daily.id == task_id)
                    .values(last_completed_at=datetime.now(), daily_streak=new_streak)
                )

            await session.commit()

#for future 
# async def check_streak(tg_id):
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id==tg_id))

#         if not user:
#             return "User not found"
        
#         now = datetime.now()

#         if user.user_last_in:
#             last_login_date = user.user_last_in.date()
#             current_date = now.date()

#             if last_login_date == current_date:
#                 return f"User {tg_id} has already performed the action today. Current streak: {user.user_streak} days."
#             elif last_login_date == current_date - timedelta(days=1):
#                 user.user_streak += 1
#         else:
#             user.user_streak = 0

#         user.user_last_in = now
#         await session.commit()




async def set_daily_task(data,tg_id):
    async with async_session() as session: 
        user = await session.scalar(select(User).where(User.tg_id==tg_id))
        if user:
            try:
                session.add(Daily(daily_name=data["daily_name"], daily_description=data["daily_description"], daily_point=data["daily_points"], daily_coins=data["daily_coins"], daily_streak = 0,user=user))
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback() 
                return f"An error occurred: {str(e)}"
            except Exception as e:
                await session.rollback()  
                return f"An unexpected error occurred: {str(e)}"
                

async def get_user_stats(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id==tg_id))
        if user:
            user_stats = {
                "user_level":user.user_level,
                "user_exp": user.user_exp,
                "user_coins": user.user_coins,
                "user_streak": user.user_streak,
            }
        
            return user_stats
    
