import asyncio
import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from admin.views import (
    TelegramUserAdmin, RoleAdmin, PermissionAdmin,
)
# from admin import setup_admin
from core.db import db_helper
from bot.__main__ import start_bot, stop_bot
from api.v1.endpoints.webhook import router as webhook_router
from api.v1.endpoints.user import router as user_router
from core import settings, logger


@asynccontextmanager
async def lifespan(app):
    """Lifecycle manager для FastAPI."""
    logger.info("🚀 Starting application...")

    await db_helper.init_db()
    logger.info("✅ Database initialized")

    bot_task = asyncio.create_task(start_bot())
    logger.info("✅ Bot task started")

    yield

    logger.info("🛑 Stopping application...")
    await stop_bot()
    bot_task.cancel()

    try:
        await bot_task
    except asyncio.CancelledError:
        logger.info("✅ Bot task cancelled")

    await db_helper.dispose()
    logger.info("✅ Application stopped")


app = FastAPI(title="Backend API", version="1.0", lifespan=lifespan)

app.include_router(webhook_router)
app.include_router(user_router)

admin = Admin(app, db_helper.engine, title="🛍️ Адмін-панель шаблону")

admin.add_view(TelegramUserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(PermissionAdmin)
# admin = setup_admin(app, db_helper.engine)


async def main():
    config = uvicorn.Config(
        app=app,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())