"""File storage adapters."""

from app.infrastructure.storage.inbox_storage import InboxFolderStorage
from app.infrastructure.storage.shipment_file_storage import ShipmentFileStorage

__all__ = ["InboxFolderStorage", "ShipmentFileStorage"]
