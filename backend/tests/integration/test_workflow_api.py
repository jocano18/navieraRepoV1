"""Integration tests — full API happy path and INCOMPLETO loop."""

import pytest
from httpx import AsyncClient

from app.infrastructure.persistence.seed import DEFAULT_CLIENT_ID


def _fields_from_extracted(data: dict[str, object]) -> dict[str, str]:
    """Build digitized field dict matching extracted API payload."""
    fields: dict[str, str] = {}
    for key, val in data.items():
        if key in ("freight_terms", "containers", "text_source"):
            continue
        if isinstance(val, dict) and "value" in val:
            fields[key] = str(val["value"])
    return fields


def _digitized_payload(data: dict[str, object]) -> dict[str, object]:
    """Full digitized request body aligned with extraction for validation."""
    return {
        "fields": _fields_from_extracted(data),
        "freight_terms": data.get("freight_terms"),
        "containers": data.get("containers") or [],
        "digitized_by": "operator1",
    }


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    """Health endpoint returns ok."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_full_happy_path(client: AsyncClient) -> None:
    """PENDIENTE_EXTRACCION through FINALIZADO."""
    client_id = str(DEFAULT_CLIENT_ID)

    inbox = await client.get("/inbox/pdfs")
    assert inbox.status_code == 200
    assert any(p["filename"] == "test.pdf" for p in inbox.json())

    create = await client.post(
        "/shipments",
        json={
            "source_pdf_filename": "test.pdf",
            "cargo_type": "DIRECTO",
            "client_id": client_id,
            "reference": "REF-HAPPY-1",
        },
    )
    assert create.status_code == 201
    shipment_id = create.json()["id"]

    extract = await client.post(f"/shipments/{shipment_id}/extract")
    assert extract.status_code == 200
    assert extract.json()["data"]["bl_number"]["value"]

    reg = await client.post(
        f"/shipments/{shipment_id}/digitized-data",
        json=_digitized_payload(extract.json()["data"]),
    )
    assert reg.status_code == 204

    validate = await client.post(
        f"/shipments/{shipment_id}/validate",
        json={"mark_complete": True},
    )
    assert validate.status_code == 200
    assert validate.json()["new_status"] == "COMPLETO"

    approve = await client.post(f"/shipments/{shipment_id}/approve")
    assert approve.status_code == 204

    capprove = await client.post(f"/shipments/{shipment_id}/client-approve")
    assert capprove.status_code == 204

    finalize = await client.post(f"/shipments/{shipment_id}/finalize")
    assert finalize.status_code == 204

    detail = await client.get(f"/shipments/{shipment_id}")
    assert detail.json()["status"] == "FINALIZADO"


@pytest.mark.asyncio
async def test_incompleto_loop(client: AsyncClient) -> None:
    """Validation mismatch -> INCOMPLETO -> correct -> COMPLETO."""
    client_id = str(DEFAULT_CLIENT_ID)

    create = await client.post(
        "/shipments",
        json={
            "source_pdf_filename": "test.pdf",
            "cargo_type": "DIRECTO",
            "client_id": client_id,
        },
    )
    assert create.status_code == 201
    shipment_id = create.json()["id"]
    extract_resp = await client.post(f"/shipments/{shipment_id}/extract")
    assert extract_resp.status_code == 200, extract_resp.text

    await client.post(
        f"/shipments/{shipment_id}/digitized-data",
        json={
            "fields": {
                "bl_number": "WRONG-NUMBER",
                "shipper": "X",
                "consignee": "Y",
            }
        },
    )

    validate = await client.post(
        f"/shipments/{shipment_id}/validate",
        json={"mark_complete": False},
    )
    assert validate.json()["new_status"] == "INCOMPLETO"

    await client.patch(
        f"/shipments/{shipment_id}/digitized-data",
        json=_digitized_payload(extract_resp.json()["data"]),
    )

    validate2 = await client.post(
        f"/shipments/{shipment_id}/validate",
        json={"mark_complete": True},
    )
    assert validate2.status_code == 200
