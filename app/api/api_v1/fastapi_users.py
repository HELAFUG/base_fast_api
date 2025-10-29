from fastapi_users import FastAPIUsers
from api.dependencies.authentication import get_user_manager
from api.dependencies.authentication import authentication_backend

fastapi_users = FastAPIUsers(
    get_user_manager,
    [authentication_backend],
)
