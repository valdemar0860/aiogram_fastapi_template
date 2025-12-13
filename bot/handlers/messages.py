# from aiogram import Router
# from aiogram.filters import Command
# from aiogram.types import Message
# from aiogram_dialog import StartMode, DialogManager
#
# from api.crud.user import TelegramUserCRUD
# from bot.dialogs.states import Wiki
# from core import logger
# from api.schemas.user import TelegramUserCreate
#
# router = Router()
#
# @router.message(Command(commands=["start"]))
# async def start_command(message: Message):
#     if message.from_user is None:
#         return
#
#     user_data = TelegramUserCreate(
#         id=message.from_user.id,
#         username=message.from_user.username,
#         first_name=message.from_user.first_name,
#         last_name=message.from_user.last_name,
#         language_code=message.from_user.language_code,
#         is_premium=message.from_user.is_premium or False,
#         is_bot=message.from_user.is_bot
#     )
#
#     user, is_new_user = await TelegramUserCRUD.create_or_update_user(db, user_data)
#
#     if is_new_user:
#         text = (
#             f"👋 Привіт, {user.first_name}!\n\n"
#             f"Ласкаво просимо до нашого магазину! 🛍️\n"
#             f"Ти був автоматично зареєстрований як покупець.\n\n"
#             f"Використовуй меню нижче для навігації:"
#         )
#     else:
#         text = f"🎉 Раді знову тебе бачити, {user.first_name}!"
#
#     await message.answer(text, reply_markup=get_main_menu(user))
#
#
# @router.message(Command(commands=["catalog"]))
# async def start_command(message: Message, dialog_manager: DialogManager):
#     await dialog_manager.start(Wiki.main, mode=StartMode.RESET_STACK)
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud.user import TelegramUserCRUD
from api.db import db_helper
from api.schemas.user import TelegramUserCreate
from core import logger

router = Router()


@router.message(CommandStart())
async def start_command(
    message: Message,
):
    if message.from_user is None:
        return

    user_data = TelegramUserCreate(
        id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        language_code=message.from_user.language_code,
        is_premium=message.from_user.is_premium or False,
        is_bot=message.from_user.is_bot
    )

    async with db_helper.session() as session:
        user, is_new_user = await TelegramUserCRUD.create_or_update_user(session, user_data)

    if is_new_user:
        await message.answer(
            f"🎉 <b>Вітаємо, {user.first_name}!</b>\n\n"
            f"Ти успішно зареєстрований у нашому магазині.\n"
            f"Зараз відкриється головне меню 👇",
            parse_mode="HTML"
        )
    else:
        await message.answer(
            f"👋 З поверненням, <b>{user.first_name}</b>!",
            parse_mode="HTML"
        )


@router.message()
async def debug_any_message(message: Message):
    """Catch-all для всіх повідомлень."""
    logger.info(
        f"🐛 DEBUG: Unhandled message\n"
        f"  User: {message.from_user.id}\n"
        f"  Text: {message.text}\n"
        f"  Type: {message.content_type}"
    )
    await message.answer(
        f"🐛 Debug mode\n"
        f"Received: {message.text or message.content_type}"
    )


@router.callback_query()
async def debug_any_callback(callback: CallbackQuery):
    """Catch-all для всіх callback."""
    logger.info(
        f"🐛 DEBUG: Unhandled callback\n"
        f"  User: {callback.from_user.id}\n"
        f"  Data: {callback.data}"
    )
    await callback.answer("Debug: callback received")