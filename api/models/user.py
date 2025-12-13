from typing import List, TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.base import Base

if TYPE_CHECKING:
    from api.models.role import Role


class TelegramUser(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(String(32), nullable=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    language_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False)

    roles: Mapped[List["Role"]] = relationship(
        secondary="user_roles",
        back_populates="users"
    )

    def has_permission(self, permission_name: str) -> bool:
        for role in self.roles:
            if any(p.name == permission_name for p in role.permissions):
                return True
        return False

    def has_role(self, role_name: str) -> bool:
        return any(r.name == role_name for r in self.roles)

    def __repr__(self) -> str:
        return f"<TelegramUser(id={self.id}, username={self.username}, is_premium={self.is_premium})>"
