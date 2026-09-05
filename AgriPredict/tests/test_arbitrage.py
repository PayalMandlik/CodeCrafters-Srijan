"""
Test Arbitrage Engine
"""

from ai.arbitrage_engine import ArbitrageEngine

def test_arbitrage_basic():
    engine = ArbitrageEngine()
    result = engine.evaluate_arbitrage(
        current_price=20.0,
        forecast=[],
        storage_cost_per_day=0.10,
        transit_cost=15.0
    )
    assert "net_profit_differential" in result
    assert "optimal_storage_days" in result
