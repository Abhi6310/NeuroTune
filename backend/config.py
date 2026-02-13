import os
from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ConfigDict

class Settings(BaseSettings):
    #App settings and configs
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", protected_namespaces=('model_',))

    #API config
    api_title: str = "Neurotune API"
    api_version: str = "1.0.0"
    api_description: str = "Personalized Brain Stimulating API"
    #Server
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True
    allowed_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    #Auth
    secret_key: str = "temp_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    #Database config — SQLite default for local dev, override via .env for MySQL
    database_url: str = "sqlite+aiosqlite:///./neurotune.db"

    #LLM config
    hf_model_id: str = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
    llm_max_new_tokens: int = 2048
    llm_temperature: float = 0.6
    llm_timeout_seconds: int = 15

#Global settings object
settings = Settings()
