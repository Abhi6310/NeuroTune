import os
from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ConfigDict

class Settings(BaseSettings):
    #App settings and configs
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", protected_namespaces=('model_',))

    #API configs
    api_title: str = "Neurotune API"
    api_version: str = "1.0.0"
    api_description: str = "Personalized Brain Stimulating API"
    #Server
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    #Auth
    secret_key: str = "temp_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    #Database config
    database_url: str = "sqlite:////./neurotune.db"

#Global settings object
settings = Settings()
