from typing import Dict, Generator

import pytest
import pytest_asyncio
from databases import Database
from httpx import AsyncClient

from app.core.config import settings
from app.main import app
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import get_superuser_token_headers, random_email


@pytest_asyncio.fixture
async def api_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url=settings.SERVER_HOST) as client:
        yield client


@pytest.fixture(autouse=True)
def reset_dependency_overrides() -> Generator:
    yield
    app.dependency_overrides = {}


@pytest_asyncio.fixture
async def superuser_token_headers(api_client: AsyncClient) -> Dict[str, str]:
    return await get_superuser_token_headers(api_client)


@pytest_asyncio.fixture
async def normal_user_token_headers(
    api_client: AsyncClient, pg_db: Database
) -> Dict[str, str]:
    return await authentication_token_from_email(
        api_client=api_client, email=random_email(), db=pg_db
    )
