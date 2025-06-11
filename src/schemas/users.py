from datetime import datetime

from pydantic import BaseModel, Field, field_validator, EmailStr


class UserBaseSchema(BaseModel):
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=150)
    email: EmailStr = Field(..., max_length=100)
    phone: str = Field(..., max_length=20)
    city: str = Field(..., max_length=100)

    @field_validator('phone')
    def validate_phone(cls, v):
        v = ''.join(filter(str.isdigit, v))
        if len(v) < 10:
            raise ValueError("Invalid phone number format")
        return v


class UserReadSchema(UserBaseSchema):
    id: int
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=8, max_length=1024)


class UserUpdateSchema(BaseModel):
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=150)
    email: EmailStr | None = Field(None, max_length=100)
    phone: str | None = Field(None, max_length=20)
    city: str | None = Field(None, max_length=100)
    password: str | None = Field(None, min_length=8, max_length=1024)
    is_active: bool | None = None
    is_superuser: bool | None = None
    is_verified: bool | None = None


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserPasswordChangeSchema(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=1024)
