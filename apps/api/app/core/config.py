from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "multimodal-rag-api"
    ENV: str = "dev"
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
