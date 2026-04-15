from functools import lru_cache
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI-Powered Market Reaction Simulator"
    app_env: str = "development"
    database_url: str = "sqlite:///./market_simulator.db"
    allowed_origins: List[str] = ["http://localhost:3000"]
    huggingface_model_name: str = "ProsusAI/finbert"
    yfinance_period: str = "1mo"
    yfinance_interval: str = "1d"

   


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
