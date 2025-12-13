from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from core import settings

bot = Bot(
    token=settings.telegram.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)

__all__ = ["bot", "dispatcher", "storage"]