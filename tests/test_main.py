import pytest
from _pytest.logging import LogCaptureFixture
from fastapi import FastAPI
from httpx import AsyncClient

from app.core.settings import get_settings
from app.main import create_app


@pytest.mark.asyncio
async def test_asyncio_runs():
    assert bool(1) is True


def test_sync_runs():
    assert bool(1) is True


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


def test_create_app(app):
    assert isinstance(app, FastAPI)


def test_app_title(app: FastAPI):
    settings = get_settings()
    assert app.title == settings.APP_NAME


def test_app_initialization_logs(caplog: LogCaptureFixture):
    create_app()
    assert 'Initializing app...' in caplog.text
    assert 'App is up and running!' in caplog.text
