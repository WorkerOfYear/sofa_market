from pydantic import BaseModel


class ExceptionContentSchema(BaseModel):
    status: str
    message: str | None = None
    data: dict = {}


class OkContentSchema(BaseModel):
    status: str
    data: dict = {}
