"""FastAPI dependency injection — composition root."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.client_repository import ClientRepository
from app.application.ports.event_publisher import EventPublisher
from app.application.ports.file_storage import FileStorage
from app.application.ports.inbox_storage import InboxStorage
from app.application.ports.notifier import Notifier
from app.application.ports.pdf_extractor import PdfExtractor
from app.application.ports.shipment_repository import ShipmentRepository
from app.application.use_cases.approve_shipment import ApproveShipmentUseCase
from app.application.use_cases.compare_data import CompareDataUseCase
from app.application.use_cases.create_shipment import CreateShipmentUseCase
from app.application.use_cases.extract_pdf_data import ExtractPdfDataUseCase
from app.application.use_cases.list_inbox_pdfs import ListInboxPdfsUseCase
from app.application.use_cases.validate_and_transition import (
    ValidateAndTransitionUseCase,
)
from app.infrastructure.config.settings import Settings, get_settings
from app.infrastructure.notifications.console_notifier import ConsoleNotifier
from app.infrastructure.notifications.email_notifier import EmailNotifier
from app.infrastructure.notifications.event_publisher import LoggingEventPublisher
from app.infrastructure.pdf.pdf_extraction_service import PdfExtractionService
from app.infrastructure.pdf.pdfplumber_text import PdfPlumberTextExtractor
from app.infrastructure.pdf.tesseract_ocr import TesseractOcrEngine
from app.infrastructure.persistence.repositories.client_repository import (
    SqlAlchemyClientRepository,
)
from app.infrastructure.persistence.repositories.shipment_repository import (
    SqlAlchemyShipmentRepository,
)
from app.infrastructure.persistence.session import get_db_session
from app.infrastructure.storage.inbox_storage import InboxFolderStorage
from app.infrastructure.storage.shipment_file_storage import ShipmentFileStorage


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Database session per request."""
    async for session in get_db_session():
        yield session


def get_inbox() -> InboxStorage:
    """Inbox folder adapter."""
    return InboxFolderStorage()


def get_file_storage() -> FileStorage:
    """Shipment PDF storage adapter."""
    return ShipmentFileStorage()


def get_pdf_extractor() -> PdfExtractor:
    """PDF extraction pipeline (native text + OCR fallback)."""
    return PdfExtractionService(
        text_extractor=PdfPlumberTextExtractor(),
        ocr_engine=TesseractOcrEngine(),
    )


def get_notifier(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Notifier:
    """Email or console notifier based on settings."""
    if settings.use_console_notifier:
        return ConsoleNotifier()
    return EmailNotifier(settings)


def get_event_publisher() -> EventPublisher:
    """Domain event publisher."""
    return LoggingEventPublisher()


async def get_shipment_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ShipmentRepository:
    """Shipment repository."""
    return SqlAlchemyShipmentRepository(session)


async def get_client_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ClientRepository:
    """Client repository."""
    return SqlAlchemyClientRepository(session)


def get_list_inbox(
    inbox: Annotated[InboxStorage, Depends(get_inbox)],
) -> ListInboxPdfsUseCase:
    """List inbox PDFs use case."""
    return ListInboxPdfsUseCase(inbox)


def get_create_shipment(
    repo: Annotated[ShipmentRepository, Depends(get_shipment_repo)],
    inbox: Annotated[InboxStorage, Depends(get_inbox)],
    storage: Annotated[FileStorage, Depends(get_file_storage)],
    client_repo: Annotated[ClientRepository, Depends(get_client_repo)],
) -> CreateShipmentUseCase:
    """Create shipment use case."""
    return CreateShipmentUseCase(repo, inbox, storage, client_repo)


def get_extract_pdf(
    repo: Annotated[ShipmentRepository, Depends(get_shipment_repo)],
    extractor: Annotated[PdfExtractor, Depends(get_pdf_extractor)],
    storage: Annotated[FileStorage, Depends(get_file_storage)],
) -> ExtractPdfDataUseCase:
    """Extract PDF use case."""
    return ExtractPdfDataUseCase(repo, extractor, storage)


def get_compare(
    repo: Annotated[ShipmentRepository, Depends(get_shipment_repo)],
) -> CompareDataUseCase:
    """Compare data use case."""
    return CompareDataUseCase(repo)


def get_validate(
    repo: Annotated[ShipmentRepository, Depends(get_shipment_repo)],
) -> ValidateAndTransitionUseCase:
    """Validate and transition use case."""
    return ValidateAndTransitionUseCase(repo)


def get_approve(
    repo: Annotated[ShipmentRepository, Depends(get_shipment_repo)],
    client_repo: Annotated[ClientRepository, Depends(get_client_repo)],
    notifier: Annotated[Notifier, Depends(get_notifier)],
    storage: Annotated[FileStorage, Depends(get_file_storage)],
    publisher: Annotated[EventPublisher, Depends(get_event_publisher)],
) -> ApproveShipmentUseCase:
    """Approve and notify use case."""
    return ApproveShipmentUseCase(repo, client_repo, notifier, storage, publisher)
