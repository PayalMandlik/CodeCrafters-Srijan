"""
Unit Tests for Price Forecaster
Tests horizon limits, input validation, and output determinism.
"""

from ai.price_forecaster import PriceForecaster

def test_valid_historical_prices_forecast():
    forecaster = PriceForecaster()
    prices = [18.0, 18.5, 19.0, 19.5, 20.0]
    result = forecaster.forecast_prices(
        crop="Tomato",
        current_price=20.0,
        historical_prices=prices,
        horizon_days=14
    )
    assert result["forecast_horizon_days"] == 14
    assert len(result["daily_forecast"]) == 14
    assert result["projected_price"] > 20.0
    assert result["trend"] in ["rising", "stable", "falling"]
    assert len(result["reasons"]) >= 2

def test_forecast_horizon_14_days():
    forecaster = PriceForecaster()
    result = forecaster.forecast_prices("Tomato", current_price=25.0, horizon_days=14)
    assert len(result["daily_forecast"]) == 14

def test_forecast_horizon_30_days():
    forecaster = PriceForecaster()
    result = forecaster.forecast_prices("Tomato", current_price=25.0, horizon_days=30)
    assert len(result["daily_forecast"]) == 30

def test_invalid_horizon_rejected():
    forecaster = PriceForecaster()
    raised_low = False
    try:
        forecaster.forecast_prices("Tomato", current_price=25.0, horizon_days=7)
    except ValueError:
        raised_low = True
    assert raised_low, "Expected ValueError for horizon < 14"

    raised_high = False
    try:
        forecaster.forecast_prices("Tomato", current_price=25.0, horizon_days=45)
    except ValueError:
        raised_high = True
    assert raised_high, "Expected ValueError for horizon > 30"

def test_deterministic_output():
    forecaster = PriceForecaster()
    history = [18.0, 18.5, 19.0, 19.5, 20.0]
    
    res1 = forecaster.forecast_prices("Tomato", current_price=20.0, historical_prices=history, horizon_days=14)
    res2 = forecaster.forecast_prices("Tomato", current_price=20.0, historical_prices=history, horizon_days=14)
    
    assert res1 == res2
    assert res1["projected_price"] == res2["projected_price"]
