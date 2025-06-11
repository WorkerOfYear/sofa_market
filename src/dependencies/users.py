from src.repositories.users import UsersRepository
from src.services.users import UsersService


def users_service():
    return UsersService(UsersRepository)
