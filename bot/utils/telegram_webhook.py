from bot import bot
from core import settings, logger


async def set_telegram_webhook():
    response = await bot.set_webhook(url=settings.telegram.webhook_url)

    if response:
        logger.info(f"Webhook set successfully: {settings.telegram.webhook_url}")
    else:
        logger.error(f"Failed to set webhook")


async def delete_telegram_webhook():
    response = await bot.delete_webhook()

    if response:
        logger.info("Webhook successfully deleted")
    else:
        logger.error("Failed to delete webhook")

