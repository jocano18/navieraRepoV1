"""Centralized FastAPI exception handlers."""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.infrastructure.config.settings import get_settings

from app.domain.exceptions import (
    ClientNotFoundError,
    DomainError,
    InboxFileNotFoundError,
    InvalidStateTransitionError,
    PdfExtractionError,
    ShipmentNotFoundError,
    ValidationIncompleteError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Register domain exception -> HTTP status mappings."""

    @app.exception_handler(ShipmentNotFoundError)
    @app.exception_handler(InboxFileNotFoundError)
    @app.exception_handler(ClientNotFoundError)
    async def not_found_handler(
        _request: Request,
        exc: DomainError,
    ) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(InvalidStateTransitionError)
    async def conflict_handler(
        _request: Request,
        exc: InvalidStateTransitionError,
    ) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": exc.message})

    @app.exception_handler(ValidationIncompleteError)
    @app.exception_handler(PdfExtractionError)
    async def unprocessable_handler(
        _request: Request,
        exc: DomainError,
    ) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": exc.message})

    @app.exception_handler(IntegrityError)
    async def integrity_handler(
        _request: Request,
        exc: IntegrityError,
    ) -> JSONResponse:
        logging.exception("Database integrity error", exc_info=exc)
        return JSONResponse(
            status_code=400,
            content={
                "detail": (
                    "No se pudo guardar el envío (referencia o cliente inválido). "
                    "Reinicia el backend para aplicar el cliente demo."
                )
            },
        )

    @app.exception_handler(PermissionError)
    @app.exception_handler(OSError)
    async def storage_handler(_request: Request, exc: OSError) -> JSONResponse:
        logging.exception("Storage I/O error", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={
                "detail": (
                    "No se pudo guardar el PDF del envío (permisos de almacenamiento). "
                    "Reinicia el backend: docker compose up -d --force-recreate backend"
                )
            },
        )

    @app.exception_handler(ResponseValidationError)
    async def response_validation_handler(
        _request: Request,
        exc: ResponseValidationError,
    ) -> JSONResponse:
        logging.exception("Response validation error", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error al serializar la respuesta del servidor."},
        )

    if get_settings().debug:

        @app.exception_handler(Exception)
        async def unhandled_handler(_request: Request, exc: Exception) -> JSONResponse:
            logging.exception("Unhandled error", exc_info=exc)
            return JSONResponse(
                status_code=500,
                content={"detail": str(exc) or exc.__class__.__name__},
            )
