"""
Buyer Service Module
Retrieves buyers, demand scores, target offered prices, and capacities.
"""

import json
import os

class BuyerService:
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

    def get_buyers_for_crop(self, crop: str) -> list:
        """
        Retrieves institutional & commercial buyers matching the crop.
        """
        buyers = self.demo_data.get("buyers", [])
        return [b for b in buyers if crop.lower() in [c.lower() for c in b.get("preferred_crops", [])]] or buyers
