import datetime

from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env",
                                      env_file_encoding="utf-8")


class AppSettings(CommonSettings):
    APP_NAME: str = "RogersComcastBackend"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"


class DbSettings(CommonSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str

class ComcastInfoSettings(CommonSettings):
    COMCAST_AUTH_TOKEN_URL: str
    COMCAST_AUTH_CLIENT_ID: str
    COMCAST_AUTH_CLIENT_SECRET: str
    COMCAST_AUTH_SCOPE: str
    COMCAST_TOKEN: str | None = None
    COMCAST_TOKEN_EXPIRES_AT: datetime = datetime.datetime.now()
    COMCAST_SERVER_BASE_URL: str


class Settings(DbSettings, AppSettings, ComcastInfoSettings):
    pass



settings = Settings()