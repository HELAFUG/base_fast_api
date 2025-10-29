from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class DBSettings(BaseModel):
    url:str = os.getenv("DB_URL", "postgres://postgres:postgres@localhost:5432/postgres")
    echo:bool = os.getenv("DB_ECHO", False)
    max_overflow:int = os.getenv("DB_MAX_OVERFLOW", 5)

class APIV1Settings(BaseModel):
    prefix:str = "/v1"


class APISettings(BaseModel):
    pretix:str = "/api"
    v1:APIV1Settings = APIV1Settings()

    

class Settings(BaseSettings):
    db:DBSettings = DBSettings()
    api:APISettings = APISettings()


settings = Settings()


