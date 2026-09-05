"""
Unit Tests for Cold-Storage Arbitrage Engine
Tests mathematical validity, threshold decision rules, edge case validation, and prompt manual example.
"""

from ai.arbitrage_engine import ArbitrageEngine

def test_manual_mathematical_validation():
    """
    Exact mathematical validation test matching user prompt example:
    - current_price = ₹20/kg
    - projected_future_price = ₹25/kg
    - spoilage_rate = 0.05 (5%)
    - storage_cost = ₹1/kg
    - transit_cost = ₹0.50/kg
    
    Expected:
    - spoilage_adjusted_future_value = 25 * (1 - 0.05) = 23.75
    - total_hold_cost = 1.0 + 0.50 = 1.50
    - ΔP = 23.75 - (20 + 1.50) = 2.25
    - Recommendation: STORE & HOLD
    """
    engine = ArbitrageEngine()
    result = engine.evaluate_arbitrage(
        current_price=20.0,
        projected_future_price=25.0,
        storage_cost_per_kg=1.0,
        transit_cost_per_kg=0.50,
        spoilage_rate=0.05
    )

    assert result["spoilage_adjusted_future_value"] == 23.75
    assert result["total_hold_cost"] == 1.50
    assert result["net_profit_differential"] == 2.25
    assert result["recommendation_action"] == "STORE & HOLD"

def test_future_price_higher_store_and_hold():
    engine = ArbitrageEngine()
    result = engine.evaluate_arbitrage(
        current_price=20.0,
        projected_future_price=28.0,
        storage_cost_per_kg=1.0,
        transit_cost_per_kg=0.50,
        spoilage_rate=0.05
    )
    assert result["recommendation_action"] == "STORE & HOLD"
    assert result["net_profit_differential"] > 0

def test_future_price_low_sell_immediately():
    engine = ArbitrageEngine()
    result = engine.evaluate_arbitrage(
        current_price=20.0,
        projected_future_price=20.5,
        storage_cost_per_kg=1.0,
        transit_cost_per_kg=0.50,
        spoilage_rate=0.05
    )
    assert result["recommendation_action"] == "SELL IMMEDIATELY"
    assert result["net_profit_differential"] < 0

def test_high_spoilage_flips_recommendation():
    engine = ArbitrageEngine()
    # Moderate gain flipped by high 25% spoilage
    result = engine.evaluate_arbitrage(
        current_price=20.0,
        projected_future_price=24.0,
        storage_cost_per_kg=1.0,
        transit_cost_per_kg=0.50,
        spoilage_rate=0.25
    )
    assert result["recommendation_action"] == "SELL IMMEDIATELY"

def test_high_storage_cost_flips_recommendation():
    engine = ArbitrageEngine()
    result = engine.evaluate_arbitrage(
        current_price=20.0,
        projected_future_price=25.0,
        storage_cost_per_kg=4.0,
        transit_cost_per_kg=0.50,
        spoilage_rate=0.05
    )
    assert result["recommendation_action"] == "SELL IMMEDIATELY"

def test_high_transit_cost_flips_recommendation():
    engine = ArbitrageEngine()
    result = engine.evaluate_arbitrage(
        current_price=20.0,
        projected_future_price=25.0,
        storage_cost_per_kg=1.0,
        transit_cost_per_kg=3.50,
        spoilage_rate=0.05
    )
    assert result["recommendation_action"] == "SELL IMMEDIATELY"

def test_invalid_spoilage_raises_error():
    engine = ArbitrageEngine()
    raised = False
    try:
        engine.evaluate_arbitrage(
            current_price=20.0,
            projected_future_price=25.0,
            storage_cost_per_kg=1.0,
            transit_cost_per_kg=0.50,
            spoilage_rate=1.2  # Spoilage > 100%
        )
    except ValueError:
        raised = True
    assert raised, "Expected ValueError for invalid spoilage rate"

def test_negative_current_price_raises_error():
    engine = ArbitrageEngine()
    raised = False
    try:
        engine.evaluate_arbitrage(
            current_price=-10.0,
            projected_future_price=25.0,
            storage_cost_per_kg=1.0,
            transit_cost_per_kg=0.50,
            spoilage_rate=0.05
        )
    except ValueError:
        raised = True
    assert raised, "Expected ValueError for negative current price"
