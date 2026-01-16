"""Application use cases module.

Use cases represent the application's business logic and orchestrate
the flow of data between the domain and interface layers.

Each use case typically:
- Takes input (request DTO)
- Performs business logic
- Returns output (response DTO)
- Delegates to domain services or repositories

This layer is thin by design - most logic should live in the domain layer.
"""

from app.application.use_cases.health_use_cases import HealthCheckUseCase


__all__ = ['HealthCheckUseCase']
