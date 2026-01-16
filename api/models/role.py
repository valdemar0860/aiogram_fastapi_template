from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from core.db.base import Base

if TYPE_CHECKING:
    from api.models.user import TelegramUser


role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
)

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', ForeignKey('telegram_users.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
)


class Permission(Base):
    name: Mapped[str] = mapped_column(String(100), unique=True)  # "view_products", "create_order"
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    roles: Mapped[List["Role"]] = relationship(
        secondary=role_permissions,
        back_populates="permissions"
    )


class Role(Base):
    name: Mapped[str] = mapped_column(String(50), unique=True)  # "admin", "seller", "customer"
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)  # Захист від видалення базових ролей

    permissions: Mapped[List[Permission]] = relationship(
        secondary=role_permissions,
        back_populates="roles"
    )
    users: Mapped[List["TelegramUser"]] = relationship(
        secondary=user_roles,
        back_populates="roles"
    )
