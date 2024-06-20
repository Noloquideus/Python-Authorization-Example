from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str

    ALGORITHM: str
    ACCESS_SECRET_KEY: str
    ACCESS_TTL_MINUTES: int
    REFRESH_SECRET_KEY: str
    REFRESH_TTL_MINUTES: int
    CONFIRM_SECRET_KEY: str
    CONFIRM_TTL_MINUTES: int

    MAX_REFRESH_TOKENS_IN_DB: int
    MAX_ACCESS_LEVEL: int

    SUPERADMIN_EMAIL: str
    SUPERADMIN_USERNAME: str
    SUPERADMIN_PASSWORD: str
    SUPERADMIN_ACCESS_LEVEL: int

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
