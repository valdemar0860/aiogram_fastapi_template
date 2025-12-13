from pydantic import BaseModel, ConfigDict
from typing import Optional


class TelegramUserCreate(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: bool = False
    is_bot: bool = False

class TelegramUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: Optional[str]
    first_name: Optional[str]
    is_premium: bool
