from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import find_dotenv
from authlib.integrations.starlette_client import OAuth


class settings_oauth_yandex(BaseSettings):
    name: str = 'yandex'
    authorize_url: str = 'https://oauth.yandex.ru/authorize'
    access_token_url: str = 'https://oauth.yandex.ru/token'
    api_base_url: str = 'https://login.yandex.ru/info'
    client_id: str = Field(default="", env="CLIENT_ID")
    client_secret: str = Field(default="", env="CLIENT_SECRET")

    class Config:
        env_file = find_dotenv(".env.yandex_oauth")
        env_file_encoding = "utf-8"
        case_sensitive = False


oauth = OAuth()
oauth.register(**dict(settings_oauth_yandex()))
