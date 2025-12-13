from sqladmin import ModelView

from api.models.user import TelegramUser
from api.models.role import Role, Permission


class TelegramUserAdmin(ModelView, model=TelegramUser):
    """Адмін-панель для користувачів."""

    name = "Користувач"
    name_plural = "Користувачі"
    icon = "fa-solid fa-user"

    column_list = [
        TelegramUser.id,
        TelegramUser.username,
        TelegramUser.first_name,
        TelegramUser.last_name,
        TelegramUser.is_premium,
        TelegramUser.created_at
    ]

    column_searchable_list = [
        TelegramUser.username,
        TelegramUser.first_name,
        TelegramUser.last_name
    ]
    column_sortable_list = [TelegramUser.id, TelegramUser.created_at]
    column_default_sort = [(TelegramUser.created_at, True)]

    form_columns = [
        TelegramUser.username,
        TelegramUser.first_name,
        TelegramUser.last_name,
        TelegramUser.roles
    ]

    column_details_list = [
        TelegramUser.id,
        TelegramUser.username,
        TelegramUser.first_name,
        TelegramUser.last_name,
        TelegramUser.language_code,
        TelegramUser.is_premium,
        TelegramUser.is_bot,
        TelegramUser.created_at,
        TelegramUser.updated_at
    ]

    can_create = False


class RoleAdmin(ModelView, model=Role):
    """Адмін-панель для ролей."""

    name = "Роль"
    name_plural = "Ролі"
    icon = "fa-solid fa-shield"

    column_list = [Role.id, Role.name, Role.description, Role.is_system]
    column_searchable_list = [Role.name]
    column_sortable_list = [Role.id, Role.name]

    form_columns = [
        Role.name,
        Role.description,
        Role.is_system,
        Role.permissions
    ]

    column_details_list = [
        Role.id,
        Role.name,
        Role.description,
        Role.is_system,
        Role.created_at
    ]

    async def delete_model(self, request, pk: str) -> bool:
        """Заборона видалення системних ролей."""
        async with self.session_maker() as session:
            role = await session.get(Role, pk)
            if role and role.is_system:
                return False
        return await super().delete_model(request, pk)


class PermissionAdmin(ModelView, model=Permission):
    """Адмін-панель для прав доступу."""

    name = "Право"
    name_plural = "Права доступу"
    icon = "fa-solid fa-key"

    column_list = [Permission.id, Permission.name, Permission.description]
    column_searchable_list = [Permission.name]

    form_columns = [Permission.name, Permission.description]
