import asyncio

from aiogram_dialog import setup_dialogs

from api.utils.set_telegram_webhook import set_telegram_webhook, delete_telegram_webhook
from bot import dispatcher, bot
from bot.handlers.messages import router as messages_router
from core import settings, RunningMode, logger


async def run_polling() -> None:
    await delete_telegram_webhook()
    logger.info("🤖 Bot started in long polling mode")

    try:
        await dispatcher.start_polling(bot, skip_updates=True)
    except asyncio.CancelledError:
        logger.info("🛑 Polling stopped")
        raise


async def run_webhook() -> None:
    await set_telegram_webhook()
    logger.info("🌐 Bot webhook configured")


async def start_bot():
    dispatcher.include_router(messages_router)

    setup_dialogs(dispatcher)

    if settings.telegram.running_mode == RunningMode.LONG_POLLING:
        await run_polling()
    elif settings.telegram.running_mode == RunningMode.WEBHOOK:
        await run_webhook()
    else:
        logger.error("❌ Unknown running mode")


async def stop_bot():
    logger.info("🛑 Stopping bot...")

    if settings.telegram.running_mode == RunningMode.WEBHOOK:
        await delete_telegram_webhook()

    await bot.session.close()
    logger.info("✅ Bot stopped")
