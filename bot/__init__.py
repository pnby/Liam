from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from sqlalchemy.orm import declarative_base
from bot.config import BOT_TOKEN, POSTGRES_URL
import logging

engine = create_async_engine(POSTGRES_URL)
session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)


def init_database():
    from bot.database.models.user import User


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with session_maker() as session:
        yield session
