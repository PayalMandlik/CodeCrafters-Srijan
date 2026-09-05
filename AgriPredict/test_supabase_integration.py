import asyncio
import httpx
import json
from app import app

async def run_verification():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # 1. Health check
        res_health = await client.get("/health")
        print("GET /health -> Status:", res_health.status_code, "| Response:", res_health.json())

        # 2. Tomato Scenario
        tomato_payload = {
            "crop": "Tomato",
            "variety": "Hybrid",
            "quantity_kg": 5000.0,
            "location": "Nashik",
            "expected_storage_days": 14
        }
        res_tomato = await client.post("/api/analyze", json=tomato_payload)
        data_tomato = res_tomato.json()
        
        print("\n--- TOMATO SCENARIO ---")
        print("Status Code:", res_tomato.status_code)
        print("Data Source:", data_tomato.get("data_source"))
        print("Current Price:", data_tomato.get("market_data", {}).get("current_price"))
        print("Historical Prices:", data_tomato.get("market_data", {}).get("historical_prices"))
        print("Projected Price:", data_tomato.get("forecast", {}).get("projected_price"))
        print("Recommendation:", data_tomato.get("recommendation", {}).get("action"))
        print("Recommended Storage:", data_tomato.get("recommended_storage", {}).get("name"), "| Source:", data_tomato.get("recommended_storage", {}).get("data_source"))
        print("Top Buyer:", data_tomato.get("top_buyers", [{}])[0].get("company_name"), "| Source:", data_tomato.get("top_buyers", [{}])[0].get("data_source"))

        # 3. Potato Scenario
        potato_payload = {
            "crop": "Potato",
            "variety": "Standard",
            "quantity_kg": 10000.0,
            "location": "Agra",
            "expected_storage_days": 14
        }
        res_potato = await client.post("/api/analyze", json=potato_payload)
        data_potato = res_potato.json()

        print("\n--- POTATO SCENARIO ---")
        print("Status Code:", res_potato.status_code)
        print("Data Source:", data_potato.get("data_source"))
        print("Current Price:", data_potato.get("market_data", {}).get("current_price"))
        print("Recommendation:", data_potato.get("recommendation", {}).get("action"))

if __name__ == "__main__":
    asyncio.run(run_verification())
