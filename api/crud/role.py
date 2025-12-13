from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from api.models.role import Role, Permission
from api.models.user import TelegramUser


class RoleCRUD:
    @staticmethod
    async def create_role(
            db: AsyncSession,
            name: str,
            description: str = None,
            is_system: bool = False
    ) -> Role:
        role = Role(name=name, description=description, is_system=is_system)
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role

    @staticmethod
    async def get_role_by_name(db: AsyncSession, name: str) -> Optional[Role]:
        result = await db.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.name == name)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def assign_permissions_to_role(
            db: AsyncSession,
            role_id: int,
            permission_ids: List[int]
    ) -> Role:
        role = await db.get(Role, role_id, options=[selectinload(Role.permissions)])
        permissions = await db.execute(
            select(Permission).where(Permission.id.in_(permission_ids))
        )
        role.permissions = list(permissions.scalars().all())
        await db.commit()
        await db.refresh(role)
        return role

    @staticmethod
    async def assign_role_to_user(
            db: AsyncSession,
            user_id: int,
            role_id: int
    ) -> TelegramUser:
        user = await db.get(TelegramUser, user_id, options=[selectinload(TelegramUser.roles)])
        role = await db.get(Role, role_id)

        if role not in user.roles:
            user.roles.append(role)
            await db.commit()
            await db.refresh(user)

        return user


class PermissionCRUD:
    @staticmethod
    async def create_permission(
            db: AsyncSession,
            name: str,
            description: str = None
    ) -> Permission:
        """Створення нового дозволу."""
        permission = Permission(name=name, description=description)
        db.add(permission)
        await db.commit()
        await db.refresh(permission)
        return permission

    @staticmethod
    async def get_all_permissions(db: AsyncSession) -> List[Permission]:
        """Отримання всіх дозволів."""
        result = await db.execute(select(Permission))
        return list(result.scalars().all())