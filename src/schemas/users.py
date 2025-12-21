from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr, BaseModel


class BaseUser(BaseModel):
    id: Optional[UUID] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    city: Optional[str] = None
    phone: str
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
