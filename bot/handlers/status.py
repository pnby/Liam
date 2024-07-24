from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=["status"]))
async def status_handler(message: Message):
    await message.answer("Status: OK")
