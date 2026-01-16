from types import MappingProxyType

from fastapi import APIRouter

from app.adapters.api.health_router import router as health_router


v1_routers: tuple[APIRouter, ...] = (health_router,)


api_v1_to_routers_map: MappingProxyType[str, tuple[APIRouter, ...]] = MappingProxyType(
    {
        'v1': v1_routers,
    }
)
