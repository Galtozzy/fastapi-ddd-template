"""Health check API router."""

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from app.application.dto.health_dto import HealthResponseDTO
from app.application.use_cases import HealthCheckUseCase
from app.core.logging_config import get_logger


logger = get_logger(__name__)

router = APIRouter(
    prefix='/health',
    tags=['health'],
    default_response_class=ORJSONResponse,
)


@router.get(
    '/ping',
    response_model=HealthResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def ping() -> HealthResponseDTO:
    return await HealthCheckUseCase().execute()
