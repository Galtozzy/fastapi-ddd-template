from app.application.dto.health_dto import HealthResponseDTO


class HealthCheckUseCase:
    """Use case for checking system health status."""

    async def execute(self) -> HealthResponseDTO:
        return HealthResponseDTO()
