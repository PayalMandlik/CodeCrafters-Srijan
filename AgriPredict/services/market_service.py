"""
Market Service Module (AgriPredict AI Engine)

Retrieves spot market prices, historical daily arrivals, and price trend signals from Supabase PostgreSQL
with seamless fallback to synthetic demo data.
"""

import json
import os
from typing import Dict, Any

class MarketService:
    """
    Market Data Ingestion and Query Service.
    Connects to Supabase market_prices table with fallback to local JSON demo dataset.
    """
    def __init__(self, db_client=None):
        self.db = db_client
        self._load_demo_data()

    def _load_demo_data(self):
        demo_path = os.path.join(os.path.dirname(__file__), "..", "data", "demo_data.json")
        try:
            with open(demo_path, "r") as f:
                self.demo_data = json.load(f)
        except Exception:
            self.demo_data = {}

    def get_market_data(self, crop: str, location: str = None) -> Dict[str, Any]:
        """
        Retrieves current spot price, arrival volume, historical price series, and trend for a crop.
        """
        crop_clean = crop.lower().strip()
        
        # 1. Attempt Supabase lookup if configured
        if self.db:
            try:
                # Query market_prices ordered by recorded_at descending
                response = self.db.table("market_prices").select("*").ilike("crop", f"%{crop_clean}%").order("recorded_at", desc=True).execute()
                if response.data and len(response.data) > 0:
                    records = response.data
                    latest = records[0]
                    
                    # Extract historical series in chronological order (oldest to newest)
                    recent_series = list(reversed(records[:14]))
                    historical_prices = [float(r.get("price_per_kg", 20.0)) for r in recent_series]
                    arrival_kg = float(latest.get("arrival_volume_kg", 180000.0))
                    
                    # Infer trend from historical slope if multiple points exist
                    if len(historical_prices) > 1:
                        diff = historical_prices[-1] - historical_prices[0]
                        trend_label = "rising" if diff > 1.0 else ("glut_recovering" if diff > 0 else "stable")
                    else:
                        trend_label = "glut_recovering"

                    return {
                        "crop": latest.get("crop", crop.capitalize()),
                        "current_price": float(latest.get("price_per_kg", 20.0)),
                        "unit": "kg",
                        "arrival_volume_tons": round(arrival_kg / 1000.0, 1),
                        "trend": trend_label,
                        "location": location or latest.get("market_location") or latest.get("market") or "Regional Mandi",
                        "historical_prices": historical_prices,
                        "data_source": "supabase"
                    }
            except Exception as e:
                print(f"[MarketService] Supabase query fallback to demo data: {e}")

        # 2. Fallback to local demo data
        markets = self.demo_data.get("markets", {})
        if crop_clean in markets:
            data = dict(markets[crop_clean])
            if location:
                data["location"] = location
            data["data_source"] = "demo_fallback"
            return data

        # 3. Default fallback if crop is not specifically in demo dictionary
        return {
            "crop": crop.capitalize(),
            "current_price": 22.50,
            "unit": "kg",
            "arrival_volume_tons": 150.0,
            "trend": "glut_recovering",
            "location": location or "Regional Mandi",
            "historical_prices": [18.0, 18.5, 19.0, 19.5, 20.5, 21.5, 22.5],
            "data_source": "demo_fallback"
        }
