from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from sqlalchemy.orm import declarative_base
from bot.config import BOT_TOKEN, POSTGRES_URL

engine = create_async_engine(POSTGRES_URL)
session_maker = async_sessionmaker(engine)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with session_maker() as session:
        return session
