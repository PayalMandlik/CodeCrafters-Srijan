"""
Storage Service Module
Manages query and retrieval for nearby cold storage facilities, availability, rates, and distance metrics.
"""

import json
import os

class StorageService:
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

    def get_nearby_facilities(self, location: str = None) -> list:
        """
        Retrieves list of nearby cold storage facilities.
        """
        return self.demo_data.get("storage_facilities", [])
