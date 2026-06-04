"""Test fakes for ports (in-memory, no I/O)."""

from pathlib import Path
from uuid import UUID

from app.application.ports.file_storage import FileStorage
from app.application.ports.inbox_storage import InboxStorage
from app.application.ports.notifier import Notifier
from app.application.ports.ocr_engine import OcrEngine
from app.application.ports.pdf_extractor import PdfExtractor
from app.domain.entities.document_data import DocumentData
from app.domain.value_objects.field_source import FieldSource
from app.infrastructure.pdf.generic_bl_extractor import GenericBlExtractor


class FakeInboxStorage(InboxStorage):
    """In-memory inbox with preset PDF files."""

    def __init__(self, files: dict[str, bytes] | None = None) -> None:
        self._files = files or {"test.pdf": b"%PDF-1.4 fake"}

    def list_pdfs(self) -> list[str]:
        return list(self._files.keys())

    def get_path(self, filename: str) -> Path:
        from app.domain.exceptions import InboxFileNotFoundError

        if filename not in self._files:
            raise InboxFileNotFoundError(filename)
        return Path(f"/fake/inbox/{filename}")

    def read_bytes(self, filename: str) -> bytes:
        from app.domain.exceptions import InboxFileNotFoundError

        if filename not in self._files:
            raise InboxFileNotFoundError(filename)
        return self._files[filename]


class FakeFileStorage(FileStorage):
    """In-memory PDF storage per shipment."""

    def __init__(self) -> None:
        self._store: dict[UUID, bytes] = {}

    async def save_pdf(
        self,
        shipment_id: UUID,
        filename: str,
        content: bytes,
    ) -> Path:
        self._store[shipment_id] = content
        return Path(f"/fake/{shipment_id}/{filename}")

    async def get_pdf_path(self, shipment_id: UUID) -> Path | None:
        if shipment_id not in self._store:
            return None
        return Path(f"/fake/{shipment_id}/doc.pdf")

    async def read_pdf_bytes(self, shipment_id: UUID) -> bytes | None:
        return self._store.get(shipment_id)


class FakePdfExtractor(PdfExtractor):
    """Returns fixed DocumentData for tests."""

    def __init__(self, text: str | None = None) -> None:
        self._text = text

    def extract(self, pdf_path: Path) -> DocumentData:
        text = self._text or "B/L NO: TESTBL123456 SHIPPER: A CONSIGNEE: B"
        return GenericBlExtractor().extract_fields(text, source=FieldSource.NATIVE)


class FakeNotifier(Notifier):
    """Records sent notifications."""

    def __init__(self) -> None:
        self.sent: list[dict[str, object]] = []

    async def notify(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        *,
        attachment_path: Path | None = None,
        shipment_id: UUID | None = None,
    ) -> None:
        self.sent.append(
            {
                "email": recipient_email,
                "subject": subject,
                "shipment_id": shipment_id,
            }
        )


class FakeOcrEngine(OcrEngine):
    """Returns preset OCR text."""

    def __init__(self, text: str = "B/L NO: OCR123") -> None:
        self._text = text

    def extract_text(self, pdf_path: Path) -> str:
        return self._text
