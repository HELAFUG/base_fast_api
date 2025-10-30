from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class DBSettings(BaseModel):
    url: str = os.getenv("DB_URL")
    echo: bool = os.getenv("DB_ECHO", False)
    max_overflow: int = os.getenv("DB_MAX_OVERFLOW", 10)

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str = os.getenv("RESET_PASSWORD_TOKEN_SECRET")
    verification_token_secret: str = os.getenv("VERIFICATION_TOKEN_SECRET")


class SRVSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class APIV1Settings(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"
    messages: str = "/messages"


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
    access_token: AccessToken = AccessToken()


settings = Settings()
