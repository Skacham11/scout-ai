"""App settings loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://scout:scout@localhost:5432/scout_ai"
    embedding_dims: int = 384


settings = Settings()
