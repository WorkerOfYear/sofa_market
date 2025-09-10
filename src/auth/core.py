from uuid import UUID

from fastapi_users import FastAPIUsers
from src.auth.manager import get_user_manager
from src.auth.config import auth_backend
from src.database.models.users import User

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)