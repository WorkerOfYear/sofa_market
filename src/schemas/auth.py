import re

from pydantic import BaseModel, field_validator


class PhoneNumberPayload(BaseModel):
    phone: str

    @field_validator('phone')
    @classmethod
    def validate_and_format_phone(cls, v: str) -> str:
        cleaned_phone = re.sub(r'[\s\-()]+', '', v)
        if not re.match(r'^(\+7|8)\d{10}$', cleaned_phone):
            raise ValueError('Номер телефона должен быть действительным номером РФ/Казахстана (+7XXXXXXXXXX или 8XXXXXXXXXX)')
        if cleaned_phone.startswith('8'):
            return '+7' + cleaned_phone[1:]
        return cleaned_phone


class VerifyOTPayload(BaseModel):
    phone: str
    otp_code: str
