import asyncio
import logging
from typing import override

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import BOT_TOKEN
from bot.utils.utils import singleton


@singleton
class Startup(object):
    _logger = logging.getLogger(__name__)
    _bot = bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    _dp = Dispatcher()

    @override
    def __new__(cls, *args, **kwargs):
        logging.basicConfig(
            level=logging.INFO,
            format="%(filename)s:%(lineno)d #%(levelname)-8s "
                   "[%(asctime)s] - %(name)s - %(message)s",
        )
        cls._logger.info("Setup logger")
        return super().__new__(cls)

    @classmethod
    def get_logger(cls):
        return cls._logger

    @classmethod
    def get_bot(cls):
        return cls._bot

    @classmethod
    def get_dispatcher(cls):
        return cls._dp

    @classmethod
    async def start_polling(cls):
        cls._logger.info("Starting polling")
        await cls._dp.start_polling(cls._bot)


startup = Startup()
asyncio.run(startup.start_polling())
