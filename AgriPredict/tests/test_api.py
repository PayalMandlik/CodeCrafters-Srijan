"""
End-to-End API Route Integration Tests
"""

import httpx
from app import app

async def test_health_endpoint():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "AgriPredict AI Engine MVP"

async def test_root_index_endpoint():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "AgriPredict AI Engine" in response.text

async def test_analyze_valid_payload():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "crop": "Tomato",
            "variety": "Roma",
            "quantity_kg": 5000.0,
            "expected_harvest_window": "2026-09-10",
            "location": "Nashik Zone B",
            "expected_storage_days": 14
        }
        response = await client.post("/api/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()

        # Validate complete pipeline response structure
        assert "farmer_input" in data
        assert "market_data" in data
        assert "forecast" in data
        assert "arbitrage" in data
        assert "recommendation" in data
        assert "recommended_storage" in data
        assert "top_buyers" in data

        # Check nested values
        assert data["forecast"]["forecast_horizon_days"] == 14
        assert data["recommendation"]["action"] in ["STORE & HOLD", "SELL IMMEDIATELY"]
        assert len(data["recommendation"]["reasons"]) > 0
        assert len(data["top_buyers"]) > 0

async def test_analyze_invalid_quantity_returns_error():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "crop": "Tomato",
            "quantity_kg": 0.0,
            "location": "Zone B"
        }
        response = await client.post("/api/analyze", json=payload)
        assert response.status_code in [400, 422]
