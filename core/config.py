from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum


class RunningMode(str, Enum):
    LONG_POLLING = "LONG_POLLING"
    WEBHOOK = "WEBHOOK"


class SecretsConfig(BaseModel):
    secret_key: str = ""
    admin_password: str = ""


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True


class LoggingConfig(BaseModel):
    level: str = "INFO"


class DatabaseConfig(BaseModel):
    url: PostgresDsn = None
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class TelegramConfig(BaseModel):
    token: str = None
    running_mode: RunningMode = "LONG_POLLING"
    webhook_path: str = None
    webhook_url: str = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="allow"
    )
    secrets: SecretsConfig = SecretsConfig()
    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()
    telegram: TelegramConfig = TelegramConfig()
    log: LoggingConfig = LoggingConfig()


settings = Settings()
