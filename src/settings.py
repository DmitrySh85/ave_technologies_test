from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    redis_url: str = Field(alias="REDIS_URL")


settings = Settings()