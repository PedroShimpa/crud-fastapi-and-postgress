from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:123456@localhost:5432/crud"
    DBBaseModel = declarative_base()

    class Config:
        case_senstive = True


settings = Settings()
