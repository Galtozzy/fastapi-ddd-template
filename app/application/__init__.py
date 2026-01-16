"""Application layer.

This layer contains use cases and DTOs that orchestrate
the domain layer to fulfill business requirements.

Use cases represent single units of work and coordinate
domain objects to perform business operations.

DTOs (Data Transfer Objects) are simple objects for
transferring data between layers without any behavior.
"""

from app.application.dto.health_dto import HealthResponseDTO
from app.application.use_cases import HealthCheckUseCase


__all__ = ['HealthResponseDTO', 'HealthCheckUseCase']
