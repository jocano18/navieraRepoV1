"""Bill of Lading number value object."""

from dataclasses import dataclass

from app.domain.exceptions import DomainError


@dataclass(frozen=True)
class BlNumber:
    """Validated, non-empty B/L number used as the primary document anchor.

    Attributes:
        value: Normalized B/L number string.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate B/L number is non-empty after normalization."""
        normalized = self.value.strip().upper()
        if not normalized:
            msg = "B/L number cannot be empty"
            raise DomainError(msg)
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        """Return string representation."""
        return self.value
