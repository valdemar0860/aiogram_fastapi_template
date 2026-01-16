from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import db_helper
from api.crud.user import TelegramUserCRUD
from api.schemas.user import TelegramUserCreate

router = APIRouter(tags=["users"])


@router.post("/add_user")
async def add_user(user_data: TelegramUserCreate, db: AsyncSession = Depends(db_helper.session_getter)):
    user, is_new_user = await TelegramUserCRUD.create_or_update_user(db, user_data)
    return {"user": user, "is_new_user": is_new_user}
