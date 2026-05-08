from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    GOOGLE_AUTH_URL:str = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL:str = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL:str = "https://www.googleapis.com/oauth2/v3/userinfo"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_DAYS: int = 7

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_USER: str

    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    MAIL_PORT:int
    MAIL_SERVER:str
    MAIL_TO:str = "default@example.com"
    MAIL_STARTTLS:bool = False
    MAIL_SSL_TLS:bool = True
    USE_CREDENTIALS:bool = True
    VALIDATE_CERTS:bool = True


    model_config = SettingsConfigDict(
    env_file=ENV_PATH,
    env_file_encoding="utf-8",
    extra="ignore"
    )


Config = Settings()