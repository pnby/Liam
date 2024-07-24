from typing import Union, Callable, Dict, Any, Awaitable, override

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot import get_session
from bot.config import ADMIN_IDs
from bot.database.repositores.user import UserRepository


class RegisterMiddleWare(BaseMiddleware):
    @override
    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        async with get_session() as session:
            user_repository = UserRepository(session)
            user = await user_repository.find_by_credentials(tg_id=event.from_user.id)
            if user is not None:
                if not user.is_disabled or str(event.from_user.id) in ADMIN_IDs:
                    return await handler(event, data)
                else:
                    return None
            else:
                await user_repository.create_user(
                    tg_id=event.from_user.id,
                    name=event.from_user.first_name,
                    username=event.from_user.username,
                    premium=event.from_user.is_premium
                )

            data['user_repository'] = user_repository
            return None
