"""Inbox PDF listing router."""

from fastapi import APIRouter, Depends

from app.application.use_cases.list_inbox_pdfs import ListInboxPdfsUseCase
from app.interfaces.api.dependencies import get_list_inbox
from app.interfaces.api.schemas.shipment import InboxPdfResponse

router = APIRouter(prefix="/inbox", tags=["inbox"])


@router.get("/pdfs", response_model=list[InboxPdfResponse])
async def list_inbox_pdfs(
    use_case: ListInboxPdfsUseCase = Depends(get_list_inbox),
) -> list[InboxPdfResponse]:
    """List PDF files available in the shared inbox folder."""
    items = use_case.execute()
    return [
        InboxPdfResponse(filename=i.filename, size_bytes=i.size_bytes) for i in items
    ]
