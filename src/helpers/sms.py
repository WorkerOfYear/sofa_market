from abc import ABC, abstractmethod

import httpx
from fastapi import HTTPException, status


class SmsClient(ABC):
    @abstractmethod
    async def send_sms(self, phone: str, message: str) -> bool | None:
        pass


class MobizonClient(SmsClient):
    def __init__(
            self,
            key: str,
            url: str = 'https://api.mobizon.kz/service/Message/SendSmsMessage',
    ):
        self.key = key
        self.url = url

    async def send_sms(self, phone: str, message: str) -> bool | None:
        params = {
            'recipient': phone,
            'text': message,
            'apiKey': self.key
        }

        # async with httpx.AsyncClient() as client:
        #     try:
        #         response = await client.post(self.url, data=params, timeout=10.0)
        #         response.raise_for_status()
        #         result = response.json()
        #
        #         if result.get('code') == 0:
        #             print(f"SMS успешно отправлено. ID: {result.get('data', {}).get('messageId')}")
        #             return True
        #         else:
        #             error_message = result.get("message", "Неизвестная ошибка API Mobizon")
        #             print(f"Ошибка Mobizon: Код {result.get('code')}, {error_message}")
        #
        #     except httpx.HTTPStatusError as e:
        #         # Ошибка на уровне HTTP-протокола
        #         print(f"HTTP ошибка при обращении к Mobizon: {e.response.status_code}")
        #         raise HTTPException(
        #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #             detail="Ошибка соединения с сервисом SMS"
        #         )
        #     except Exception as e:
        #         # Другие ошибки (сеть, JSON парсинг)
        #         print(f"Произошла непредвиденная ошибка: {e}")
        #         raise HTTPException(
        #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #             detail="Внутренняя ошибка сервера при отправке SMS"
        #         )
