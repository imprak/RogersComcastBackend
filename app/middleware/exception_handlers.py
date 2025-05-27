from fastapi import Request, status
from fastapi.applications import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app import log
from app.core.exceptions import (
    ConflictError,
    NotFoundError,
    AuthenticationError,
    BadRequestError,
    BackendError,
)


def authentication_exception_handler(
    _request: Request,
    exc: AuthenticationError,
) -> JSONResponse:
    log.error(f"An authentication error occurred: {exc}")

    status_code = status.HTTP_401_UNAUTHORIZED
    content = {
        "error": {
            "code": status_code,
            "message": str(exc),
            "status": "Error",
        }
    }

    return JSONResponse(
        content=content,
        status_code=status_code,
    )


def not_found_exception_handler(
    _request: Request,
    exc: NotFoundError,
) -> JSONResponse:
    log.error(f"A Not found error occurred: {exc}")

    status_code = status.HTTP_404_NOT_FOUND
    content = {
        "error": {
            "code": status_code,
            "message": str(exc),
            "status": "Error",
        }
    }

    return JSONResponse(
        content=content,
        status_code=status_code,
    )


def conflict_exception_handler(
    _request: Request,
    exc: ConflictError,
) -> JSONResponse:
    log.error(f"A conflict error occurred: {exc}")

    status_code = status.HTTP_409_CONFLICT
    content = {
        "error": {
            "code": status_code,
            "message": str(exc),
            "status": "Error",
        }
    }

    return JSONResponse(
        content=content,
        status_code=status_code,
    )


def validation_exception_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    log.error(f"A Validation error occurred: {exc}")

    status_code = status.HTTP_400_BAD_REQUEST
    content = {
        "error": {
            "code": status_code,
            "message": str(exc),
            "status": "Error",
        }
    }

    return JSONResponse(
        content=content,
        status_code=status_code,
    )


def bad_request_exception_handler(
    _request: Request,
    exc: BadRequestError,
) -> JSONResponse:
    log.error(f"A Bad request error occurred: {exc}")

    status_code = status.HTTP_400_BAD_REQUEST
    content = {
        "error": {
            "code": status_code,
            "message": str(exc),
            "status": "Error",
        }
    }

    return JSONResponse(
        content=content,
        status_code=status_code,
    )


def database_exception_handler(
    _request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    log.error(f"A Database error occurred: {exc}")

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    content = {
        "error": {
            "code": status_code,
            "message": str(exc),
            "status": "Error",
        }
    }

    return JSONResponse(
        content=content,
        status_code=status_code,
    )


def backend_exception_handler(
    _request: Request,
    exc: BackendError,
) -> JSONResponse:
    log.error(f"A backend error occurred: {exc}")

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    content = {
        "error": {
            "code": status_code,
            "message": str(exc),
            "status": "Error",
        }
    }

    return JSONResponse(
        content=content,
        status_code=status_code,
    )


def register_handlers(app: FastAPI):
    app.add_exception_handler(
        ConflictError,
        conflict_exception_handler,
    )
    app.add_exception_handler(
        NotFoundError,
        not_found_exception_handler,
    )
    app.add_exception_handler(
        AuthenticationError,
        authentication_exception_handler,
    )
    app.add_exception_handler(
        BadRequestError,
        bad_request_exception_handler,
    )
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )
    app.add_exception_handler(
        SQLAlchemyError,
        database_exception_handler,
    )
    app.add_exception_handler(
        BackendError,
        backend_exception_handler,
    )
