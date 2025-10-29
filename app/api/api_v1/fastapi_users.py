from fastapi_users import FastAPIUsers
from dependencies.authentication import get_user_manager
from dependencies.authentication import authentication_backend

fastapi_users = FastAPIUsers(
    get_user_manager,
    [authentication_backend],
)
