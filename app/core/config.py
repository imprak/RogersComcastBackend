from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env",
                                      env_file_encoding="utf-8")



class AppSettings(CommonSettings):
    APP_NAME: str = "RogersComcastBackend"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"


class DbSettings(CommonSettings):
    DB_HOST: str = "10.168.171.11"
    DB_PORT: int = 3306
    DB_USERNAME: str = "root"
    DB_PASSWORD: str = "root"
    DB_NAME: str = "rogers"


class Settings(DbSettings, AppSettings):
    pass



settings = Settings()