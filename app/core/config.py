from pydantic_settings import BaseSettings, SettingsConfigDict


# Step 1: Create a Settings CLASS
class Settings(BaseSettings):
    # Step 2: Define what variables you expect
    PROJECT_NAME: str = "E-Commerce API"  # default if not in .env
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "super-secret-key-change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres_password@localhost:5432/ecommerce_db"
    )
    REDIS_URL: str = "redis://localhost:6379/0"

    # Step 3: Tell Pydantic where to find values
    model_config = SettingsConfigDict(
        env_file=".env",  # Look in .env file
        env_file_encoding="utf-8",  # File encoding
        extra="ignore",  # Ignore extra variables in .env
    )


# Step 4: Create one instance to use everywhere
settings = Settings()
