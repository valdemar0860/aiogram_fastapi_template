from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.models.role import Role
from api.models.user import TelegramUser
from api.schemas.user import TelegramUserCreate as TelegramUserSchema


class TelegramUserCRUD:

    @staticmethod
    async def get_user_by_id(
            db: AsyncSession,
            user_id: int
    ) -> Optional[TelegramUser]:
        result = await db.execute(
            select(TelegramUser).where(TelegramUser.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_or_update_user(session: AsyncSession, user_data: TelegramUserSchema) -> tuple[TelegramUser, bool]:
        user = await TelegramUserCRUD.get_user_by_id(session, user_data.id)
        is_new_user = False

        if user:
            for key, value in user_data.dict().items():
                setattr(user, key, value)
        else:
            user = TelegramUser(**user_data.dict())
            session.add(user)
            is_new_user = True

        await session.commit()
        await session.refresh(user)

        return user, is_new_user

    @staticmethod
    async def get_user_with_roles(
            db: AsyncSession,
            user_id: int
    ) -> Optional[TelegramUser]:
        result = await db.execute(
            select(TelegramUser)
            .options(
                selectinload(TelegramUser.roles).selectinload(Role.permissions)
            )
            .where(TelegramUser.id == user_id)
        )
        return result.scalar_one_or_none()