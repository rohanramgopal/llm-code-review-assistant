from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), extra="ignore")

    APP_NAME: str = "LLM Code Review Assistant"
    APP_ENV: str = "development"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    SECRET_KEY: str = "change_me"

    DATABASE_URL: str = "sqlite:///./code_review.db"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "llama3"

    LLM_PROVIDER: str = "rules"

    GITHUB_TOKEN: str = ""
    GITHUB_WEBHOOK_SECRET: str = ""

    MAX_FILE_BYTES: int = 200000
    MAX_TOTAL_FILES: int = 50

    REPORTS_DIR: str = str(BASE_DIR / "reports")
    REPOS_DIR: str = str(BASE_DIR / "data" / "repos")


@lru_cache
def get_settings() -> Settings:
    return Settings()
