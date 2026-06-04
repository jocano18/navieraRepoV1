"""Inbox folder storage adapter."""

from pathlib import Path

from app.application.ports.inbox_storage import InboxStorage
from app.domain.exceptions import InboxFileNotFoundError
from app.infrastructure.config.settings import get_settings


class InboxFolderStorage(InboxStorage):
    """Adapter: scans data/inbox/ for incoming B/L PDFs."""

    def __init__(self, inbox_path: str | None = None) -> None:
        settings = get_settings()
        self._inbox = Path(inbox_path or settings.inbox_path)
        self._inbox.mkdir(parents=True, exist_ok=True)

    def list_pdfs(self) -> list[str]:
        """List .pdf filenames sorted by name."""
        return sorted(
            p.name for p in self._inbox.iterdir() if p.suffix.lower() == ".pdf"
        )

    def get_path(self, filename: str) -> Path:
        """Resolve and validate inbox file path."""
        path = self._inbox / filename
        if not path.is_file():
            raise InboxFileNotFoundError(f"Inbox PDF not found: {filename}")
        return path

    def read_bytes(self, filename: str) -> bytes:
        """Read PDF bytes from inbox."""
        return self.get_path(filename).read_bytes()
