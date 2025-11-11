from typing import Any, AsyncGenerator

import pytest
from fastapi import FastAPI
from fastapi.routing import APIRoute
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from fastapi_org.db.dependencies import get_db_session
from fastapi_org.db.utils import create_database, drop_database
from fastapi_org.settings import settings
from fastapi_org.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from fastapi_org.db.meta import meta
    from fastapi_org.db.models import load_all_models

    load_all_models()

    await create_database()

    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


@pytest.fixture(scope="session")
async def session_data(_engine: AsyncEngine) -> None:
    """Fill database with test data once per session using raw SQL."""
    async with _engine.begin() as conn:
        await conn.execute(text("DELETE FROM organization_activity"))
        await conn.execute(text("DELETE FROM phone_numbers"))
        await conn.execute(text("DELETE FROM organizations"))
        await conn.execute(text("DELETE FROM activities"))
        await conn.execute(text("DELETE FROM buildings"))

        await conn.execute(
            text(
                """
            INSERT INTO buildings (id, address, latitude, longitude) VALUES
            (1, 'Test Address 1, Moscow', 55.7558, 37.6173),
            (2, 'Test Address 2, Moscow', 55.7559, 37.6174),
            (3, 'Test Address 3, St. Petersburg', 59.9343, 30.3351)
        """,
            ),
        )

        await conn.execute(
            text(
                """
            INSERT INTO activities (id, name, parent_id) VALUES
            (1, 'Restaurant', NULL),
            (2, 'Sports Center', NULL),
            (3, 'Italian Cuisine', 1),
            (4, 'Fitness', 2)
        """,
            ),
        )

        await conn.execute(
            text(
                """
            INSERT INTO organizations (id, name, building_id) VALUES
            (1, 'Moscow Restaurant 1', 1),
            (2, 'Moscow Restaurant 2', 1),
            (3, 'Moscow Sports Center', 2),
            (4, 'Petersburg Restaurant', 3)
        """,
            ),
        )

        await conn.execute(
            text(
                """
            INSERT INTO phone_numbers (id, organization_id, phone_number) VALUES
            (1, 1, '+79990001111'),
            (2, 1, '+79990002222'),
            (3, 2, '+79990003333'),
            (4, 3, '+79990004444'),
            (5, 4, '+79990005555')
        """,
            ),
        )

        await conn.execute(
            text(
                """
            INSERT INTO organization_activity (organization_id, activity_id) VALUES
            (1, 1), (1, 3),
            (2, 1),
            (3, 2), (3, 4),
            (4, 1)
        """,
            ),
        )

        await conn.commit()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
    session_data: None,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :param session_data: ensures test data is loaded.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
def fastapi_app(
    dbsession: AsyncSession,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    return application


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test", timeout=2.0) as ac:
        yield ac


@pytest.fixture
async def correct_api_key() -> str:
    return settings.api_key


@pytest.fixture
def protected_routes(fastapi_app: FastAPI) -> list[APIRoute]:
    unprotected_paths = {"/api/openapi.json", "/api/docs", "/api/redoc"}
    return [
        route
        for route in fastapi_app.routes
        if isinstance(route, APIRoute)
        and route.path.startswith("/api/")
        and route.path not in unprotected_paths
    ]
