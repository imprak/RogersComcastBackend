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
    DB_PORT: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str


class Settings(DbSettings, AppSettings):
    pass



settings = Settings()