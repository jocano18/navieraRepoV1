"""Client entity."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class Client:
    """Import client who receives notifications and approvals.

    Attributes:
        id: Unique identifier.
        name: Display name.
        nit: Tax identification number.
        email: Notification email address.
        is_active: Whether the account is active.
    """

    id: UUID
    name: str
    nit: str = ""
    email: str = ""
    is_active: bool = True
