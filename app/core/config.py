from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class DBSettings(BaseModel):
    url: str = os.getenv("DB_URL")
    echo: bool = os.getenv("DB_ECHO", False)
    max_overflow: int = os.getenv("DB_MAX_OVERFLOW", 10)


class SRVSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class APIV1Settings(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"


class APISettings(BaseModel):
    pretix: str = "/api"
    v1: APIV1Settings = APIV1Settings()

    @property
    def bearer_token_to_url(self):
        parts = (self.pretix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    api: APISettings = APISettings()
    srv: SRVSettings = SRVSettings()


settings = Settings()
