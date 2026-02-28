import enum
from pydantic import BaseModel


__all__ = [
    'Error',
    'ErrorCode',
    'ErrorModel',

    'Ok',
    'AlreadyExistsError',
    'DeadlineExceededError',
    'FailedPreconditionError',
    'InternalError',
    'InvalidArgumentError',
    'NotFoundError',
    'PermissionDeniedError',
    'TooManyRequestsError',
    'UnauthenticatedError',
    'UnimplementedError'
]


class ErrorCode(enum.IntEnum):
    """
    错误代码。定义参照谷歌RPC错误代码定义。
    """
    OK = 0
    CANCELLED = 1
    UNKNOWN = 2
    INVALID_ARGUMENT = 3
    DEADLINE_EXCEEDED = 4
    NOT_FOUND = 5
    ALREADY_EXISTS = 6
    PERMISSION_DENIED = 7
    RESOURCE_EXHAUSTED = 8
    FAILED_PRECONDITION = 9
    ABORTED = 10
    OUT_OF_RANGE = 11
    UNIMPLEMENTED = 12
    INTERNAL = 13
    UNAVAILABLE = 14
    DATA_LOSS = 15
    UNAUTHENTICATED = 16


class ErrorModel(BaseModel):
    code: ErrorCode
    message: str


class Ok(ErrorModel):
    def __init__(self):
        super().__init__(code=ErrorCode.OK, message='Ok.')


class Error(Exception):
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message

    def json(self):
        return self.model().model_dump_json()

    def model(self):
        return ErrorModel(
            code=self.code,
            message=self.message
        )


class AlreadyExistsError(Error):
    def __init__(self, message: str = 'Requested resource already exists.'):
        super().__init__(code=ErrorCode.ALREADY_EXISTS, message=message)


class DeadlineExceededError(Error):
    def __init__(self, message: str = 'Deadline exceeded.'):
        super().__init__(code=ErrorCode.DEADLINE_EXCEEDED, message=message)


class FailedPreconditionError(Error):
    def __init__(self, message: str = 'Resource is not in a valid state.'):
        super().__init__(code=ErrorCode.FAILED_PRECONDITION, message=message)


class InternalError(Error):
    def __init__(self, message: str = 'Internal error.'):
        super().__init__(code=ErrorCode.INTERNAL, message=message)


class InvalidArgumentError(Error):
    def __init__(self, message: str = 'Invalid argument.'):
        super().__init__(code=ErrorCode.INVALID_ARGUMENT, message=message)


class NotFoundError(Error):
    def __init__(self, message: str = 'Requested resource does not exist.'):
        super().__init__(code=ErrorCode.NOT_FOUND, message=message)


class PermissionDeniedError(Error):
    def __init__(self, message: str = 'Permission denied.'):
        super().__init__(code=ErrorCode.PERMISSION_DENIED, message=message)


class TooManyRequestsError(Error):
    def __init__(self, message: str = 'Too many requests.'):
        super().__init__(code=ErrorCode.UNAVAILABLE, message=message)


class UnauthenticatedError(Error):
    def __init__(self, message: str = 'Unauthenticated request.'):
        super().__init__(code=ErrorCode.UNAUTHENTICATED, message=message)


class UnimplementedError(Error):
    def __init__(self, message: str = 'Unimplemented method.'):
        super().__init__(code=ErrorCode.UNIMPLEMENTED, message=message)
