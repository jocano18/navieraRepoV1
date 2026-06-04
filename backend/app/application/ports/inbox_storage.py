"""Inbox folder storage port."""

from abc import ABC, abstractmethod
from pathlib import Path


class InboxStorage(ABC):
    """Port for scanning and reading PDFs from the shared inbox folder."""

    @abstractmethod
    def list_pdfs(self) -> list[str]:
        """Return filenames of PDF files in the inbox."""

    @abstractmethod
    def get_path(self, filename: str) -> Path:
        """Resolve inbox filename to absolute path.

        Raises:
            InboxFileNotFoundError: If file does not exist.
        """

    @abstractmethod
    def read_bytes(self, filename: str) -> bytes:
        """Read raw PDF bytes from inbox."""
