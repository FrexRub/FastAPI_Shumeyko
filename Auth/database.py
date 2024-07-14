from typing import AsyncGenerator
import datetime

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, func, DateTime

from database import Base, async_session_maker


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str]
    registered_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        default=datetime.datetime.utcnow(),
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
