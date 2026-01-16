"""Health DTOs (Data Transfer Objects).

This module contains request and response schemas for health-related
operations. DTOs are used to transfer data between application layers.
"""

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from app.core.pydantic_base import BaseModel
from app.domain.models.health import HealthStatus


class HealthResponseDTO(BaseModel):
    """Response DTO for health check endpoint."""

    id: UUID = Field(default_factory=uuid4)
    status: HealthStatus = HealthStatus.HEALTHY
    timestamp: datetime = Field(default_factory=datetime.now)
