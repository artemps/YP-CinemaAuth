from fastapi import status
from httpx import AsyncClient

from core import settings


async def test_doc_url_works(client: AsyncClient) -> None:
    response = await client.get(settings.api_documentation_url)
    assert response.status_code == status.HTTP_200_OK


async def test_openapi_doc_url_works(client: AsyncClient) -> None:
    response = await client.get(settings.openapi_documentation_url)
    assert response.status_code == status.HTTP_200_OK
