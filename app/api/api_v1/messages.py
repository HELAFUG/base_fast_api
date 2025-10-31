from fastapi import APIRouter, Depends
from typing import Annotated
from core.models import User

from core.config import settings
from core.schemas.user import UserRead
from .fastapi_users import (
    current_user,
    current_superuser,
)

router = APIRouter(
    prefix=settings.api.v1.messages,
    tags=["Messagesss"],
)


@router.get("")
def get_user_messages(user: Annotated[User, Depends(current_user)]):
    return {"messages": UserRead.model_validate(user)}


@router.get("/secrets")
def get_superuser_messages(user: Annotated[User, Depends(current_superuser)]):
    return {"user": UserRead.model_validate(user)}
