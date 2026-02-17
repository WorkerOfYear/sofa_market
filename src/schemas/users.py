from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from .base import BaseSchema


class UserBase(BaseSchema):
    id: Optional[UUID] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
