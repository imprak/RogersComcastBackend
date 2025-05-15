from pydantic_settings import BaseSettings, SettingsConfigDict

import os

pg_user = os.getenv("POSTGRES_USER", "user")
pg_password = os.getenv("POSTGRES_PASSWORD", "password")
pg_host = os.getenv("POSTGRES_HOST", "localhost")
pg_database = os.getenv("POSTGRES_DB", "RogersComcastBackend")


class Settings(BaseSettings):
    APP_NAME: str = "RogersComcastBackend"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str =  f"postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}/{pg_database}"
    
    

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()