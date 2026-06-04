"""Pytest fixtures."""

import os
from collections.abc import AsyncIterator
from pathlib import Path
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.application.ports.pdf_extractor import PdfExtractor
from app.infrastructure.persistence.models import Base
from app.infrastructure.persistence.seed import DEFAULT_CLIENT_ID, seed_default_client
from app.main import app

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def sample_bl_text() -> str:
    return (FIXTURES / "sample_bl.txt").read_text(encoding="utf-8")


@pytest.fixture
def default_client_id() -> UUID:
    return DEFAULT_CLIENT_ID


@pytest.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    """In-memory SQLite session per test."""
    engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        await seed_default_client(session)
        yield session
    await engine.dispose()


@pytest.fixture
async def client(
    db_session: AsyncSession,
    sample_bl_text: str,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> AsyncIterator[AsyncClient]:
    """HTTP client with overridden DB session and fake PDF pipeline."""
    from app.infrastructure.config import settings as settings_mod
    from app.interfaces.api import dependencies as deps
    from tests.unit.fakes import FakeFileStorage, FakeInboxStorage, FakePdfExtractor

    inbox_dir = tmp_path / "inbox"
    inbox_dir.mkdir()
    pdf_path = inbox_dir / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 test content")

    monkeypatch.setenv("DATABASE_URL", TEST_DB_URL)
    monkeypatch.setenv("DATABASE_URL_SYNC", "sqlite:///:memory:")
    monkeypatch.setenv("INBOX_PATH", str(inbox_dir))
    monkeypatch.setenv("STORAGE_LOCAL_PATH", str(tmp_path / "storage"))
    monkeypatch.setenv("USE_CONSOLE_NOTIFIER", "true")
    monkeypatch.setenv("PUBLIC_API_URL", "http://test")
    monkeypatch.setenv("APPROVAL_TOKEN_SECRET", "test-secret")
    settings_mod.get_settings.cache_clear()

    engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_session() -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            await seed_default_client(session)
            yield session

    fake_extractor: PdfExtractor = FakePdfExtractor(sample_bl_text)

    app.dependency_overrides[deps.get_session] = override_session
    fake_storage = FakeFileStorage()
    app.dependency_overrides[deps.get_pdf_extractor] = lambda: fake_extractor
    app.dependency_overrides[deps.get_inbox] = lambda: FakeInboxStorage(
        {"test.pdf": pdf_path.read_bytes()},
        base_dir=inbox_dir,
    )
    app.dependency_overrides[deps.get_file_storage] = lambda: fake_storage

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as http_client:
        yield http_client

    app.dependency_overrides.clear()
    settings_mod.get_settings.cache_clear()
    os.environ.pop("DATABASE_URL", None)
