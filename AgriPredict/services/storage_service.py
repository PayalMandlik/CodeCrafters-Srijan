"""
Storage Service Module (AgriPredict AI Engine)

Manages query, retrieval, and economic optimization of cold-storage facilities from Supabase PostgreSQL
with local demo JSON fallback.
"""

import json
import os
from typing import List, Dict, Any, Optional

class StorageService:
    """
    Cold-Storage Facility Query and Selection Service.
    Integrates Supabase cold_storage records with local synthetic demo data fallback.
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

    def get_facilities(self, location: str = None) -> List[Dict[str, Any]]:
        """
        Retrieves active cold-storage facilities.
        """
        # 1. Attempt Supabase query if configured
        if self.db:
            try:
                response = self.db.table("cold_storage").select("*").eq("is_active", True).execute()
                if response.data and len(response.data) > 0:
                    facilities = []
                    for row in response.data:
                        facilities.append({
                            "facility_id": str(row.get("id")),
                            "name": row.get("facility_name"),
                            "location": row.get("location"),
                            "distance_km": float(row.get("distance_km", 15.0)),
                            "daily_cost_per_kg": float(row.get("storage_rate_per_kg_per_day", 0.0714)),
                            "capacity_kg": float(row.get("total_capacity_kg", 500000.0)),
                            "available_capacity_kg": float(row.get("available_capacity_kg", 100000.0)),
                            "rating": float(row.get("rating", 4.5)),
                            "data_source": "supabase"
                        })
                    return facilities
            except Exception as e:
                print(f"[StorageService] Supabase storage_facilities query fallback to demo data: {e}")

        # 2. Fallback to local demo data
        raw_facilities = self.demo_data.get("storage_facilities", [])
        facilities = []
        for fac in raw_facilities:
            f_copy = dict(fac)
            f_copy["data_source"] = "demo_fallback"
            facilities.append(f_copy)
        return facilities

    def calculate_transit_cost(self, distance_km: float, quantity_kg: float) -> float:
        """
        Calculates total freight transit cost based on distance and quantity.
        Base logistics rate: ₹0.02 per kg per km + ₹100 base handling fee.
        """
        transit_per_kg = 0.02 * distance_km + 0.05
        return round(transit_per_kg * quantity_kg, 2)

    def select_optimal_facility(
        self,
        quantity_kg: float,
        storage_days: int = 14,
        preferred_location: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Selects the economically optimal cold-storage facility based on available capacity,
        total storage rate, and freight transit distance.
        """
        facilities = self.get_facilities(preferred_location)
        if not facilities:
            return None

        candidates = []
        for fac in facilities:
            avail = fac.get("available_capacity_kg", 0)
            if avail >= quantity_kg:
                dist = fac.get("distance_km", 20.0)
                daily_rate = fac.get("daily_cost_per_kg", 0.10)
                
                storage_cost_total = daily_rate * storage_days * quantity_kg
                transit_cost_total = self.calculate_transit_cost(dist, quantity_kg)
                total_facility_cost = storage_cost_total + transit_cost_total

                candidate = dict(fac)
                candidate["estimated_transit_cost"] = round(transit_cost_total, 2)
                candidate["total_storage_cost"] = round(storage_cost_total, 2)
                candidate["_total_cost"] = total_facility_cost
                candidates.append(candidate)

        if not candidates:
            # If no facility meets strict capacity, evaluate available candidates
            for fac in facilities:
                dist = fac.get("distance_km", 20.0)
                daily_rate = fac.get("daily_cost_per_kg", 0.10)
                storage_cost_total = daily_rate * storage_days * quantity_kg
                transit_cost_total = self.calculate_transit_cost(dist, quantity_kg)
                candidate = dict(fac)
                candidate["estimated_transit_cost"] = round(transit_cost_total, 2)
                candidate["total_storage_cost"] = round(storage_cost_total, 2)
                candidate["_total_cost"] = storage_cost_total + transit_cost_total
                candidates.append(candidate)

        # Sort candidates by lowest overall cost (storage + freight)
        candidates.sort(key=lambda x: x["_total_cost"])
        optimal = candidates[0]
        optimal.pop("_total_cost", None)
        return optimal
