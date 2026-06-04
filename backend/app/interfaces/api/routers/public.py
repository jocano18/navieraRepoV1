"""Public routes (no auth) — email approval deep links."""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse

from app.application.use_cases.approve_via_email_link import ApproveViaEmailLinkUseCase
from app.domain.exceptions import (
    DomainError,
    InvalidApprovalTokenError,
    ShipmentNotFoundError,
    ValidationIncompleteError,
)
from app.interfaces.api.dependencies import get_approve_via_email
from app.interfaces.api.html_pages import approval_error_page, approval_success_page

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/approve", response_class=HTMLResponse)
async def approve_via_email_link(
    token: str = Query(..., min_length=10),
    use_case: ApproveViaEmailLinkUseCase = Depends(get_approve_via_email),
) -> HTMLResponse:
    """Client clicks 'Aprobar' in email → NOTIFICADO → FINALIZADO."""
    try:
        result = await use_case.execute(token)
    except InvalidApprovalTokenError as exc:
        return HTMLResponse(
            approval_error_page(exc.message),
            status_code=400,
        )
    except (ShipmentNotFoundError, ValidationIncompleteError) as exc:
        return HTMLResponse(
            approval_error_page(exc.message),
            status_code=422,
        )
    except DomainError as exc:
        return HTMLResponse(
            approval_error_page(exc.message),
            status_code=422,
        )

    if result.already_finalized:
        return HTMLResponse(
            approval_success_page(
                reference=result.reference,
                status=result.status.value,
            ),
        )

    return HTMLResponse(
        approval_success_page(
            reference=result.reference,
            status=result.status.value,
        ),
    )
