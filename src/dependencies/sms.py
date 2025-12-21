from fastapi import Request

from src.helpers.sms import SmsClient


async def get_sms_client(request: Request) -> SmsClient:
    return request.app.state.sms_client
