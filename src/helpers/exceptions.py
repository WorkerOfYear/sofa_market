import logging

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from src.schemas.base import ExceptionContentSchema


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    422: "unprocessable_entity",
    500: "internal_server_error",
}


class HTTPUnprocessableEntity(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class HTTPUnauthorized(HTTPException):
    def __init__(self, detail: str, status_code: int = 401):
        super().__init__(status_code=status_code, detail=detail)


class HTTPForbidden(HTTPException):
    def __init__(self, detail: str, status_code: int = 403):
        super().__init__(status_code=status_code, detail=detail)


class HTTPNotFound(HTTPException):
    def __init__(self, detail: str, status_code: int = 404):
        super().__init__(status_code=status_code, detail=detail)


class HTTPConflict(HTTPException):
    def __init__(self, detail: str, status_code: int = 409):
        super().__init__(status_code=status_code, detail=detail)


class HTTPSuperset(HTTPException):
    def __init__(self, detail: str, status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)


async def unauthorized_exception_handler(request: Request, exc: HTTPUnauthorized):
    logging.error(f"Error: {exc.detail}, status: {exc.status_code}")
    error = jsonable_encoder(ExceptionContentSchema(
        status=HTTP_ERROR_CODES.get(exc.status_code),
        message=exc.detail
    ))
    return JSONResponse(
        status_code=exc.status_code,
        content=error
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Error: {exc.body}, status: Unprocessable Entity")
    error = jsonable_encoder(ExceptionContentSchema(
        status=HTTP_ERROR_CODES.get(422),
        message="Unprocessable Entity",
        data={
            "body": exc.body,
            "errors": list(exc.errors())
        }
    ))
    return JSONResponse(
        status_code=422,
        content=error,
    )


async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Error: {exc}")
    error = jsonable_encoder(ExceptionContentSchema(
        status=HTTP_ERROR_CODES.get(500),
        message="Internal Server Error"
    ))
    return JSONResponse(
        status_code=500,
        content=error
    )
