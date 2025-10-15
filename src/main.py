import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from src.helpers.exceptions import (
    HTTPUnauthorized,
    unauthorized_exception_handler,
    validation_exception_handler,
    global_exception_handler
)
from src.middlewares import log_middleware
from src.routers import router
from src.logger import logger


app = FastAPI(title="marketplace")
logger.info("Starting API...")

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.include_router(router)


# app.add_exception_handler(HTTPUnauthorized, unauthorized_exception_handler)
# app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_exception_handler(Exception, global_exception_handler)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
    )
