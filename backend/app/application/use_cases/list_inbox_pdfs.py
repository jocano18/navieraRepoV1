"""ListInboxPdfs use case."""

from app.application.dto.shipment_dto import InboxPdfDTO
from app.application.ports.inbox_storage import InboxStorage


class ListInboxPdfsUseCase:
    """Scan the inbox folder and return available B/L PDF filenames."""

    def __init__(self, inbox: InboxStorage) -> None:
        self._inbox = inbox

    def execute(self) -> list[InboxPdfDTO]:
        """List PDF files in the inbox."""
        result: list[InboxPdfDTO] = []
        for filename in self._inbox.list_pdfs():
            size_bytes = self._inbox.get_path(filename).stat().st_size
            result.append(InboxPdfDTO(filename=filename, size_bytes=size_bytes))
        return sorted(result, key=lambda x: x.filename)
