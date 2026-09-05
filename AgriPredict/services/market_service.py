"""
Market Service Module
Retrieves current crop prices, historical arrival volumes, and mandi trends.
"""

import json
import os

class MarketService:
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

    def get_market_data(self, crop: str, location: str = None) -> dict:
        """
        Retrieves spot prices, arrival volume, and market trends for a crop.
        """
        markets = self.demo_data.get("markets", {})
        crop_data = markets.get(crop.lower(), {
            "crop": crop,
            "current_price": 24.50,
            "unit": "kg",
            "arrival_volume_tons": 120,
            "trend": "falling",
            "location": location or "Local Mandi"
        })
        return crop_data
