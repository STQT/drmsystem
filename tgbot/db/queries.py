import asyncio
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.db.base import Base
from tgbot.db.models import (
    User, School,
    College, Texnikum, Lyceum
)

from tgbot.config import load_config

config = load_config(".env")


class Database:
    def get_engine(self):
        engine = create_async_engine(
            config.db.database_url,
            future=True,
            echo=True
        )

        return engine

    def get_credentials(self) -> (str, str):
        return config.db.admin_login, config.db.admin_password

    async def load(self) -> AsyncSession:
        engine = self.get_engine()
        async with engine.begin() as conn:
            x = await conn.run_sync(Base.metadata.create_all)
            print(x, "######################################")
        async_sessionmaker = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )

        self.async_session = async_sessionmaker

    # ---User model---

    async def reg_user(self, user_id: str, username: str, first_name: str):
        """Регистрация пользователя"""
        async with self.async_session() as session:
            session: AsyncSession
            await session.merge(
                User(
                    user_id=user_id,
                    username=username,
                    first_name=first_name
                )
            )
            await session.commit()

    async def get_user(self, user_id) -> User:
        """Получения пользователя"""
        async with self.async_session() as session:
            session: AsyncSession

            response = await session.get(User, user_id)
            return response

    async def get_all_users(self) -> Sequence[User]:
        """Получения всех пользователей"""
        async with self.async_session() as session:
            session: AsyncSession

            response = await session.execute(select(User))
            return response.scalars().all()

    # ---School model---

    async def get_school_data(self, name) -> School:
        async with self.async_session() as session:
            session: AsyncSession

            response = await session.execute(select(School).where(School.nomi == name))
            return response.scalar()

    async def get_all_school_names(self):
        async with self.async_session() as session:
            session: AsyncSession

            response = await session.execute(select(School.nomi))
            return response.scalars().all()

    # ---College model---

    async def get_college_data(self, name) -> College:
        async with self.async_session() as session:
            session: AsyncSession

            response = await session.execute(select(College).where(College.nomi == name))
            return response.scalar()

    async def get_all_college_names(self):
        async with self.async_session() as session:
            session: AsyncSession

            response = await session.execute(select(College.nomi))
            return response.scalars().all()

    # ---Texnikum model---

    async def get_texnikum_data(self, name) -> Texnikum:
        async with self.async_session() as session:
            session: AsyncSession

            response = await session.execute(select(Texnikum).where(Texnikum.nomi == name))
            return response.scalar()

    async def get_all_texnikum_names(self):
        async with self.async_session() as session:
            session: AsyncSession

            response = await session.execute(select(Texnikum.nomi))
            return response.scalars().all()

    # ---Lyceum model---

    async def get_lyceum_data(self, name) -> Lyceum:
        async with self.async_session() as session:
            session: AsyncSession

            response = await session.execute(select(Lyceum).where(Lyceum.nomi == name))
            return response.scalar()

    async def get_all_lyceum_names(self):
        async with self.async_session() as session:
            session: AsyncSession

            response = await session.execute(select(Lyceum.nomi))
            return response.scalars().all()

    # ---Issues---

    async def reg_issue(self, user_id: str, username: str, name: str, contact: str, issue: str):
        """Регистрация пользователя"""
        async with self.async_session() as session:
            session: AsyncSession
            await session.merge(
                User(
                    user_id=user_id,
                    username=username,
                    name=name,
                    contact=contact,
                    issue=issue
                )
            )
            await session.commit()
