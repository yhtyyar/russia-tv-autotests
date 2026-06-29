"""Настройки приложения, загружаемые из переменных окружения."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки конфигурации проекта."""

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

    screenshot_dir: str = "reports/screenshots"


@lru_cache
def get_settings() -> Settings:
    """Вернуть кэшированный экземпляр Settings."""
    return Settings()
