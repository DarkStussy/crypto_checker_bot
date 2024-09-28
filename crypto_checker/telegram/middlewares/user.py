import logging
from decimal import Decimal
from typing import Optional, Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import User as AiogramUser, Update

from crypto_checker.core.exceptions import UserNotFound
from crypto_checker.core.models.dto import User
from crypto_checker.infrastructure.db.repositories import Repository

logger = logging.getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Optional[Any]:
        aiogram_user: Optional[AiogramUser] = data.get("event_from_user")
        if not aiogram_user:
            return

        repository: Repository = data["repository"]
        try:
            user = await repository.user.get_by_id(user_id=aiogram_user.id)
        except UserNotFound:
            user = await repository.user.create(User(id=aiogram_user.id, percent=Decimal("5")))
            await repository.commit()

        data["user"] = user
        return await handler(event, data)
