from functools import wraps
from typing import Callable
from aiogram.types import CallbackQuery, Message

from api.crud.user import TelegramUserCRUD
from api.db import db_helper


def require_role(role: str):
    """
    Декоратор для перевірки ролі.

    Usage:
        @require_role("admin")
        async def on_admin_panel(...):
            ...
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = None
            dialog_manager = None
            print("243238032308")
            for arg in args:
                print(arg)
                print("**********************************************************")
            print(type(args[1]))
            user_id = args[1].from_user.id
            async with db_helper.session() as session:
                result = await TelegramUserCRUD.has_role(session, "editor", user_id)
            print(result)
            # print(type(args[0]))
                # user = arg.get('from_user')
                # print(user)
                # break

            if 'dialog_manager' in kwargs:
                dialog_manager = kwargs['dialog_manager']
                user = dialog_manager.middleware_data.get('user')

            if not user:
                print("0+8=80")
                return await func(*args, **kwargs)

            if not user.has_role(role):
                for arg in args:
                    if isinstance(arg, CallbackQuery):
                        await arg.answer("❌ У вас немає доступу до цієї функції.", show_alert=True)
                        return
                    elif isinstance(arg, Message):
                        await arg.answer("❌ У вас немає доступу до цієї функції.")
                        return

                return

            return await func(*args, **kwargs)

        return wrapper

    return decorator