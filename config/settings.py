"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Project configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    base_url: str = "https://russia-tv.online/"
    environment: str = "prod"

    browser: str = "chromium"
    headless: bool = True
    slow_mo: int = 0

    parallel_workers: int = 4

    allure_results_dir: str = "reports/allure-results"

    api_timeout: int = 30
    api_base_url: str = "https://russia-tv.online/api"

    screenshot_dir: str = "reports/screenshots"


@lru_cache
def get_settings() -> Settings:
    """Return cached Settings instance."""
    return Settings()
