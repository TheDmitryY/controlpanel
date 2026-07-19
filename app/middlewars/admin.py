import logging
from typing import Any, Awaitable, Callable, Dict, Set
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

logger = logging.getLogger(__name__)


class AdminAccessMiddleware(BaseMiddleware):
    def __init__(self, admin_ids: Set[int]) -> None:
        self.admin_ids = admin_ids
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        user_id = None

        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        if user_id in self.admin_ids:
            return await handler(event, data)

        logger.warning(f"🚨 Спроба доступу від стороннього користувача! ID: {user_id}")

        if isinstance(event, CallbackQuery):
            await event.answer()

        return