from functools import wraps
from typing import Callable

from api.crud.user import TelegramUserCRUD
from core.db import db_helper


def require_roles(roles: list):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            callback = args[1]  # да, пока так
            user_id = callback.from_user.id

            async with db_helper.session() as session:
                for role in roles:
                    has_role = await TelegramUserCRUD.has_role(
                        session, role, user_id
                    )
                    if has_role:
                        break
                else:
                    await callback.answer("❌ У вас нет прав", show_alert=True)
                    return

            return await func(*args, **kwargs)

        return wrapper
    return decorator