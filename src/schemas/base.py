from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ExceptionContentSchema(BaseModel):
    status: str
    message: str | None = None
    data: dict = {}


class OkContentSchema(BaseModel):
    status: str
    data: dict = {}
