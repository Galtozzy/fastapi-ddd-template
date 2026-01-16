import importlib
from functools import lru_cache

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from app.core.settings import get_settings


settings = get_settings()


def create_engine() -> AsyncEngine:
    return create_async_engine(
        settings.db_url,
        poolclass=NullPool,
        execution_options={'insertmanyvalues_page_size': 1000, 'postgresql_insert_many_values': True},
    )


@lru_cache
def get_async_session_maker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=create_engine(),
        expire_on_commit=False,
        autoflush=False,
        future=True,
    )


def get_app_models_path(app: str) -> list[str] | None:
    imported_modules = []
    app_models_paths = [f'{app}.models', f'{app}.models_split']
    for app_models_path in app_models_paths:
        try:
            importlib.import_module(app_models_path)
            imported_modules.append(app_models_path)
        except (ImportError, ModuleNotFoundError) as e:
            if 'No module named' in str(e):
                continue
            raise

    return imported_modules


def get_models() -> list[str]:
    models = []

    for app_name in settings.get_apps_list():
        if models_path := get_app_models_path(app_name):
            models.extend(models_path)

    return models
