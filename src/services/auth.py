from fastapi import HTTPException, status, Response, Request

from src.uow.sqlalchemy import UnitOfWork
from src.auth import CookieTransport, RedisStrategy
from src.schemas import UserBase


class AuthService:
    def __init__(
            self,
            uow: UnitOfWork,
            cookie_transport: CookieTransport,
            redis_strategy: RedisStrategy
    ):
        self.uow = uow
        self.cookie_transport = cookie_transport
        self.redis_strategy = redis_strategy

    async def get_current_user(self, request: Request) -> UserBase:
        token = self.cookie_transport.get_token_from_request(request)

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Требуется аутентификация",
            )

        session_data = await self.redis_strategy.get_session(token)

        if not session_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Сессия истекла или недействительна",
            )

        user_id = session_data.get("user_id")
        user = await self.uow.user_repo.get_by_id(user_id)

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден или неактивен",
            )

        return user

    async def login(self, response: Response, phone: str) -> UserBase:
        user = await self.uow.user_repo.get_by_phone(phone)

        if not user:
            await self.uow.user_repo.create(
                UserBase(phone=phone),
            )

        elif not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь неактивен",
            )

        # Создаем сессию в Redis
        user_data = user.to_base_scheme()
        session_id = await self.redis_strategy.create_session(user.id)

        # Устанавливаем cookie
        self.cookie_transport.set_login_cookie(response, session_id)

        return user_data

    async def logout(self, request: Request, response: Response) -> None:
        session_id = self.cookie_transport.get_token_from_request(request)
        self.cookie_transport.set_logout_cookie(response)
        await self.redis_strategy.delete_session(session_id)
