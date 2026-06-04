"""Health endpoint schemas."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response schema.

    Attributes:
        status: Application health indicator.
    """

    status: str = Field(..., examples=["ok"])
