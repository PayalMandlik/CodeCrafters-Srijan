"""
Unit Tests for Buyer Matcher
Tests normalization, weighted score calculation, and descending sorting.
"""

from ai.buyer_matcher import BuyerMatcher

def test_buyer_matcher_sorting_and_weights():
    matcher = BuyerMatcher()
    sample_buyers = [
        {
            "buyer_id": "B1",
            "company_name": "Low Match Buyer",
            "demand_score": 50.0,
            "offered_price_per_kg": 20.0,
            "capacity_kg": 2000.0,
            "distance_km": 50.0
        },
        {
            "buyer_id": "B2",
            "company_name": "High Match Buyer",
            "demand_score": 95.0,
            "offered_price_per_kg": 30.0,
            "capacity_kg": 10000.0,
            "distance_km": 10.0
        }
    ]

    matched = matcher.match_buyers(
        crop="Tomato",
        quantity_kg=5000.0,
        location="Zone B",
        buyers_list=sample_buyers
    )

    assert len(matched) == 2
    assert matched[0]["buyer_id"] == "B2"
    assert matched[0]["match_score"] > matched[1]["match_score"]
    assert "match_reasons" in matched[0]
    assert len(matched[0]["match_reasons"]) > 0

def test_empty_buyer_list():
    matcher = BuyerMatcher()
    matched = matcher.match_buyers("Tomato", 5000.0, "Zone B", [])
    assert matched == []
