from datetime import datetime

from sqlalchemy import BigInteger, String, ForeignKey,DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    user_level: Mapped[int] = mapped_column()
    user_exp: Mapped[int] = mapped_column()
    user_coins: Mapped[int] = mapped_column()
    # user_streak: Mapped[int] = mapped_column() for future feature
    # user_last_in: Mapped[datetime] = mapped_column(DateTime,nullable=True)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")
    daily_tasks: Mapped[list["Daily"]] = relationship("Daily", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_name: Mapped[str] = mapped_column(String(25))
    task_description: Mapped[str] = mapped_column(String(125))
    task_point: Mapped[int] = mapped_column()
    task_coins: Mapped[int] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship("User", back_populates="tasks")


class Daily(Base):
    __tablename__ = "daily"

    id: Mapped[int] = mapped_column(primary_key=True)
    daily_name: Mapped[str] = mapped_column(String(25))
    daily_description: Mapped[str] = mapped_column(String(125))
    daily_point: Mapped[int] = mapped_column()
    daily_coins: Mapped[int] = mapped_column()
    daily_streak: Mapped[int] = mapped_column()
    last_completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)



    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship("User", back_populates="daily_tasks")



async def conn_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

