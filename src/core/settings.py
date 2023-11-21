from logging import config as logging_config
from pathlib import Path

from dotenv import find_dotenv
from pydantic_settings import BaseSettings

from pydantic import Field

from core.logger import LOGGING


class Settings(BaseSettings):
    project_name: str = Field("Cinema Auth", env="PROJECT_NAME")
    base_dir: Path = Path(__file__).parent
    debug: bool = Field(..., env="DEBUG")
    secret_key: str = Field(..., env="SECRET_KEY")
    app_host: str = Field(..., env="APP_HOST")
    app_port: int = Field(..., env="APP_PORT")

    api_documentation_url: str = "/api/docs"
    openapi_documentation_url: str = "/api/openapi.json"

    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")

    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")

    logging_config.dictConfig(LOGGING)

    class Config:
        env_file = find_dotenv(".env")
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def log_config(self) -> dict:
        return LOGGING
