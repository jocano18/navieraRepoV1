"""FastAPI application entrypoint."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.config.settings import get_settings
from app.infrastructure.persistence.seed import seed_default_client
from app.infrastructure.persistence.session import get_session_factory, init_db
from app.interfaces.api.exception_handlers import register_exception_handlers
from app.interfaces.api.routers.health import router as health_router
from app.interfaces.api.routers.inbox import router as inbox_router
from app.interfaces.api.routers.public import router as public_router
from app.interfaces.api.routers.shipments import router as shipments_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Startup: create tables and seed default client."""
    await init_db()
    factory = get_session_factory()
    async with factory() as session:
        await seed_default_client(session)
    yield


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="Naviera Documentation Management System API",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(application)
    application.include_router(health_router)
    application.include_router(inbox_router)
    application.include_router(shipments_router)
    application.include_router(public_router)

    return application


app = create_app()
