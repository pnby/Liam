import asyncio
import multiprocessing
from datetime import datetime
from typing import override, final

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.api.backup import BackupManager
from bot.config import BOT_TOKEN, SOURCE_DIR, DESTINATION_DIR
from bot.utils.utils import singleton
from handlers.status import router as status_router
from middleware.register import RegisterMiddleWare


@final
@singleton
class Startup(object):
    _bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    _dp = Dispatcher()
    _backup_manager: BackupManager

    @override
    def __init__(
            self,
            source_dir: str,
            destination_dir: str,
    ):
        self._backup_manager = BackupManager(
            timestamp="".join(str(datetime.now())[:10].split(" ")),
            source_dir=source_dir,
            destination_dir=destination_dir,
        )
        self._register_middlewares()
        self._register_routers()

    def run_backup_process(self, time: str):
        backup_process = multiprocessing.Process(target=self._backup_manager.run_backup_task, args=(time, ))
        backup_process.start()

    @classmethod
    async def start_polling(cls):
        await cls._dp.start_polling(cls._bot)

    @classmethod
    def _register_middlewares(cls):
        cls._dp.message.outer_middleware(RegisterMiddleWare())

    @classmethod
    def _register_routers(cls):
        cls._dp.include_router(status_router)


if __name__ == "__main__":
    startup = Startup(
        source_dir=SOURCE_DIR,
        destination_dir=DESTINATION_DIR,
    )
    startup.run_backup_process("19:23")
    asyncio.run(startup.start_polling())
