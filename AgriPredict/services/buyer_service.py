"""
Buyer Service Module (AgriPredict AI Engine)

Retrieves institutional, processing, and retail produce buyers from Supabase PostgreSQL
with local demo JSON fallback.
"""

import json
import os
from typing import List, Dict, Any

class BuyerService:
    """
    Produce Buyer Retrieval Service.
    Queries Supabase buyers catalog table with fallback to local demo data.
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

    def get_buyers_for_crop(self, crop: str) -> List[Dict[str, Any]]:
        """
        Retrieves active institutional and commercial buyers matching the specified crop.
        """
        crop_clean = crop.lower().strip()

        # 1. Attempt Supabase lookup if configured
        if self.db:
            try:
                response = self.db.table("buyers").select("*").eq("is_active", True).ilike("crop", crop_clean).execute()
                if response.data and len(response.data) > 0:
                    buyers = []
                    for row in response.data:
                        buyers.append({
                            "buyer_id": str(row.get("id")),
                            "company_name": row.get("buyer_name"),
                            "buyer_type": row.get("buyer_type", "Commercial Buyer"),
                            "demand_score": float(row.get("demand_score", 85.0)),
                            "offered_price_per_kg": float(row.get("offered_price_per_kg", 25.0)),
                            "capacity_kg": float(row.get("capacity_kg", 20000.0)),
                            "distance_km": float(row.get("distance_km", 25.0)),
                            "preferred_crops": [row.get("crop", crop.capitalize())],
                            "data_source": "supabase"
                        })
                    return buyers
            except Exception as e:
                print(f"[BuyerService] Supabase buyers query fallback to demo data: {e}")

        # 2. Fallback to demo data
        buyers = self.demo_data.get("buyers", [])
        matched = []
        for b in buyers:
            if crop_clean in [c.lower() for c in b.get("preferred_crops", [])]:
                b_copy = dict(b)
                b_copy["data_source"] = "demo_fallback"
                matched.append(b_copy)

        if not matched:
            for b in buyers:
                b_copy = dict(b)
                b_copy["data_source"] = "demo_fallback"
                matched.append(b_copy)

        return matched
