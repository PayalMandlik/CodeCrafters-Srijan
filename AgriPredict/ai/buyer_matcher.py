"""
Buyer Matcher Module (AgriPredict AI Engine)

Ranks potential institutional and commercial produce buyers based on a weighted matching model:
- 40% Buyer Demand Index
- 30% Purchase Capacity Match
- 20% Offered Price per kg
- 10% Proximity / Distance (closer is higher score)
"""

from typing import List, Dict, Any

class BuyerMatcher:
    """
    Weighted Produce Buyer Ranking Engine.
    Normalizes candidate attributes and ranks buyers by calculated match score.
    """
    def __init__(self):
        pass

    def match_buyers(
        self,
        crop: str,
        quantity_kg: float,
        location: str,
        buyers_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Ranks candidate buyers according to demand, capacity, price, and distance.

        Args:
            crop: Crop name
            quantity_kg: Farmer's produce quantity in kg
            location: Farmer's farm/mandi location
            buyers_list: List of buyer dictionary objects

        Returns:
            Sorted list of buyer dictionaries enriched with match_score and match_reasons.
        """
        if not buyers_list:
            return []

        # Find max values for normalization across the candidate pool
        max_demand = max((b.get("demand_score", 50.0) for b in buyers_list), default=100.0)
        max_demand = max_demand if max_demand > 0 else 100.0

        max_price = max((b.get("offered_price_per_kg", 1.0) for b in buyers_list), default=1.0)
        max_price = max_price if max_price > 0 else 1.0

        max_dist = max((b.get("distance_km", 10.0) for b in buyers_list), default=10.0)
        max_dist = max_dist if max_dist > 0 else 10.0

        scored_buyers = []

        for b in buyers_list:
            raw_demand = float(b.get("demand_score", 50.0))
            raw_capacity = float(b.get("capacity_kg", quantity_kg))
            raw_price = float(b.get("offered_price_per_kg", 20.0))
            raw_dist = float(b.get("distance_km", 20.0))

            # 1. Normalize individual factors (0.0 to 1.0)
            norm_demand = min(1.0, max(0.0, raw_demand / 100.0))
            norm_capacity = min(1.0, max(0.0, raw_capacity / quantity_kg if quantity_kg > 0 else 1.0))
            norm_price = min(1.0, max(0.0, raw_price / max_price))
            norm_distance = min(1.0, max(0.0, 1.0 - (raw_dist / max_dist if max_dist > 0 else 0.0)))

            # 2. Compute weighted score (0 - 100 scale)
            weighted_score = (
                0.40 * norm_demand +
                0.30 * norm_capacity +
                0.20 * norm_price +
                0.10 * norm_distance
            ) * 100.0

            match_score = round(weighted_score, 1)

            # 3. Generate explainable reasons
            reasons = []
            if norm_demand >= 0.8:
                reasons.append(f"High buyer demand score ({raw_demand:.1f}/100).")
            if raw_capacity >= quantity_kg:
                reasons.append(f"Full purchase capacity ({raw_capacity:,.0f} kg) covers total batch ({quantity_kg:,.0f} kg).")
            if raw_price >= max_price * 0.9:
                reasons.append(f"Top competitive offer price at ₹{raw_price:.2f}/kg.")
            if raw_dist <= 25.0:
                reasons.append(f"Close transit proximity ({raw_dist:.1f} km).")
            if not reasons:
                reasons.append("Verified commercial buyer matching crop specifications.")

            buyer_entry = dict(b)
            buyer_entry["match_score"] = match_score
            buyer_entry["match_reasons"] = reasons
            scored_buyers.append(buyer_entry)

        # Sort buyers descending by match_score
        scored_buyers.sort(key=lambda x: x["match_score"], reverse=True)
        return scored_buyers
