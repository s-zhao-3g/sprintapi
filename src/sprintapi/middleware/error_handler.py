import fastapi

from ..error import (
    Error,
    ErrorCode,
    InvalidArgumentError,
)
from pydantic import ValidationError


__all__ = [
    'register_sprintapi_errors'
]



_error_code_map = {
    ErrorCode.OK: 200,
    ErrorCode.CANCELLED: 499,
    ErrorCode.UNKNOWN: 500,
    ErrorCode.INVALID_ARGUMENT: 400,
    ErrorCode.DEADLINE_EXCEEDED: 504,
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.ALREADY_EXISTS: 409,
    ErrorCode.PERMISSION_DENIED: 403,
    ErrorCode.RESOURCE_EXHAUSTED: 429,
    ErrorCode.FAILED_PRECONDITION: 400,
    ErrorCode.ABORTED: 409,
    ErrorCode.OUT_OF_RANGE: 400,
    ErrorCode.UNIMPLEMENTED: 501,
    ErrorCode.INTERNAL: 500,
    ErrorCode.UNAVAILABLE: 503,
    ErrorCode.DATA_LOSS: 500,
    ErrorCode.UNAUTHENTICATED: 401
}


def _register_sprintapi_error_handler(app: fastapi.FastAPI):
    def _handler(request: fastapi.Request, exc: Error):
        if request.headers.get('accept') == 'text/event-stream':
            return fastapi.Response(
                status_code=200,
                headers={
                    'Content-Type': 'text/event-stream',
                },
                content=f'event: abort\ndata: {exc.json()}\n\n'
            )
        return fastapi.Response(
            status_code=_error_code_map.get(exc.code, 500),
            content=exc.json()
        )
    app.add_exception_handler(Error, _handler)


def _register_pydantic_validation_error(app: fastapi.FastAPI):
    def _handler(request: fastapi.Request, _):
        exc = InvalidArgumentError()
        if request.headers.get('accept') == 'text/event-stream':
            return fastapi.Response(
                status_code=200,
                headers={
                    'Content-Type': 'text/event-stream',
                },
                content=f'event: abort\ndata: {exc.json()}\n\n'
            )
        return fastapi.Response(
            status_code=400,
            content=exc.json()
        )
    app.add_exception_handler(ValidationError, _handler)


def register_sprintapi_errors(app: fastapi.FastAPI):
    _register_sprintapi_error_handler(app)
    _register_pydantic_validation_error(app)
