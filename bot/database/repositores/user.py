from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional
from bot.database.models.user import User


class UserRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self) -> User: ...

    async def find_by_credentials(self) -> Optional[User]: ...
