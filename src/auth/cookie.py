from typing import Optional

from fastapi import Request, Response


class CookieTransport:
    def __init__(
        self,
        cookie_name: str = "auth",
        cookie_max_age: int = 3600,
        cookie_secure: bool = False,
        cookie_httponly: bool = True,
    ):
        self.cookie_name = cookie_name
        self.cookie_max_age = cookie_max_age
        self.cookie_secure = cookie_secure
        self.cookie_httponly = cookie_httponly

    def set_login_cookie(self, response: Response, token: str):
        """Установка cookie с токеном"""
        response.set_cookie(
            key=self.cookie_name,
            value=token,
            max_age=self.cookie_max_age,
            secure=self.cookie_secure,
            httponly=self.cookie_httponly,
        )

    def set_logout_cookie(self, response: Response):
        """Удаление cookie при выходе"""
        response.delete_cookie(
            key=self.cookie_name,
            secure=self.cookie_secure,
            httponly=self.cookie_httponly,
        )

    def get_token_from_request(self, request: Request) -> Optional[str]:
        """Извлечение токена из cookie запроса"""
        return request.cookies.get(self.cookie_name)
