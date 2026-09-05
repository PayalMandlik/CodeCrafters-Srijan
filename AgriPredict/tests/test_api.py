"""
Test API Endpoints using httpx AsyncClient
"""

import pytest
import httpx
from app import app

@pytest.mark.asyncio
async def test_health_endpoint():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        json_resp = response.json()
        assert json_resp["status"] == "healthy"

@pytest.mark.asyncio
async def test_index_page():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "AgriPredict AI Engine" in response.text
