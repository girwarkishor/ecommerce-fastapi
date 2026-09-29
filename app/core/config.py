from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "E-Commerce API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "super-secret-key-change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres_password@localhost:5432/ecommerce_db"
    )
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
