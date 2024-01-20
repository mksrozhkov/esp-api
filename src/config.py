# stdlib
from functools import lru_cache

# thirdparty
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Настройки проекта
    PROJECT_NAME: str = "Home-Metrics"
    ENVIRONMENT: str = "dev"
    OPENAPI_URL: str | None = None

    # Настройки БД
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    # Sentry
    SENTRY_DSN: str = ""
    TRACES_SAMPLE_RATE: float = 0.0

    # API-KEYS
    DEVICE_UUID: str
    SECRET_KEY: str

    @computed_field  # type: ignore
    @property
    def DB_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
