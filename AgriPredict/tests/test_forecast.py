"""
Test Price Forecaster
"""

from ai.price_forecaster import PriceForecaster

def test_price_forecaster_horizon():
    forecaster = PriceForecaster()
    horizon = 14
    forecast = forecaster.forecast_prices("Tomato", base_price=25.0, horizon_days=horizon)
    assert len(forecast) == horizon
    assert forecast[0]["price"] > 0
