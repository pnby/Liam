from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional
from bot.database.models.user import User


class UserRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, tg_id: int, name: str, username: str, premium: bool) -> User:
        user = User(
            tg_id=tg_id,
            name=name,
            premium=premium,
            username=username,
            password=None
        )
        self.session.add(user)
        await self.session.commit()

        return user

    async def find_by_credentials(self, tg_id: int = None, username: str = None) -> Optional[User]:
        stmt = select(User).where(or_(User.tg_id == tg_id, User.username == username))
        user = await self.session.execute(stmt)
        user = user.scalar_one_or_none()

        return user

    async def change_password(self, tg_id: int, password: str) -> bool:
        stmt = select(User).where(and_(User.tg_id == tg_id))
        user = await self.session.execute(stmt)
        user = user.scalar_one_or_none()

        if user is None:
            return False
        else:
            user.password = password
            await self.session.commit()
            return True
