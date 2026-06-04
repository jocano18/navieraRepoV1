"""Domain-level exceptions (no external dependencies)."""


class DomainError(Exception):
    """Base exception for domain rule violations."""

    def __init__(self, message: str) -> None:
        """Initialize with a human-readable message."""
        super().__init__(message)
        self.message = message


class InvalidStateTransitionError(DomainError):
    """Raised when a shipment status transition is not allowed."""


class ShipmentNotFoundError(DomainError):
    """Raised when a shipment aggregate cannot be found."""


class ClientNotFoundError(DomainError):
    """Raised when a client cannot be found."""


class PdfExtractionError(DomainError):
    """Raised when PDF extraction fails or mandatory fields are missing."""


class ValidationIncompleteError(DomainError):
    """Raised when validation cannot proceed due to missing data."""


class InboxFileNotFoundError(DomainError):
    """Raised when a requested inbox PDF does not exist."""


class InvalidApprovalTokenError(DomainError):
    """Raised when an email approval link token is invalid or expired."""
