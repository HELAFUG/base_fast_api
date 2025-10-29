from fastapi_users.authentication import BearerTransport
from core.config import settings

bearer_transport = BearerTransport(token_url=settings.api.bearer_token_to_url)
