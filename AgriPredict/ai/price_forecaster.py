"""
Price Forecaster Module (AgriPredict AI Engine)

Provides a deterministic, explainable forecasting model for crop spot market prices over a 14–30 day horizon.
Uses a weighted momentum and trend-reversion calculation incorporating historical spot prices, recent momentum,
and market arrival volume trends.
"""

from typing import List, Dict, Any, Tuple

class PriceForecaster:
    """
    Deterministic MVP Price Forecasting Engine.
    Combines historical price series slope, arrival volume pressure, and seasonal recovery signals.
    """
    def __init__(self):
        pass

    def forecast_prices(
        self,
        crop: str,
        current_price: float,
        historical_prices: List[float] = None,
        arrival_volume_tons: float = 100.0,
        trend_signal: str = "stable",
        horizon_days: int = 14
    ) -> Dict[str, Any]:
        """
        Generates daily price forecast points for the requested horizon (14 to 30 days).
        
        Args:
            crop: Crop name (e.g. Tomato, Potato, Onion)
            current_price: Spot price per kg (> 0)
            historical_prices: List of recent historical daily spot prices
            arrival_volume_tons: Recent market arrival volume in tons
            trend_signal: General market momentum ('glut_falling', 'glut_recovering', 'rising', 'falling', 'stable')
            horizon_days: Forecast horizon (14 to 30)

        Returns:
            Dict containing daily forecast points, projected end price, peak price, trend, confidence, and reasons.
        """
        # 1. Validation
        if current_price <= 0:
            raise ValueError("Current market price must be greater than zero.")
        if horizon_days < 14 or horizon_days > 30:
            raise ValueError("Forecast horizon must be between 14 and 30 days.")

        prices = historical_prices or [current_price]
        if not prices:
            prices = [current_price]

        # 2. Compute historical momentum slope (linear regression or simple diff)
        if len(prices) > 1:
            # Simple weighted daily slope over historical series
            slope_sum = 0.0
            weight_sum = 0.0
            for i in range(1, len(prices)):
                diff = prices[i] - prices[i - 1]
                weight = float(i)  # Give more weight to recent price movements
                slope_sum += diff * weight
                weight_sum += weight
            historical_daily_momentum = slope_sum / weight_sum if weight_sum > 0 else 0.0
        else:
            historical_daily_momentum = 0.0

        # 3. Market signal adjustment
        # Glut recovery effect: if price dropped significantly, market supply drops and prices recover over 14-20 days
        trend_lower = trend_signal.lower()
        if "recovering" in trend_lower or "glut" in trend_lower:
            # Post-glut supply taper: prices increase deterministically by ~1.5% to 2.5% daily, dampening over time
            base_daily_growth_pct = 0.018
            signal_trend = "rising"
        elif "rising" in trend_lower:
            base_daily_growth_pct = 0.012
            signal_trend = "rising"
        elif "falling" in trend_lower:
            base_daily_growth_pct = -0.010
            signal_trend = "falling"
        else:  # stable
            base_daily_growth_pct = 0.002
            signal_trend = "stable"

        # Arrival volume impact factor: high arrival (>250 tons) suppresses growth; moderate arrival boosts recovery
        if arrival_volume_tons > 250.0:
            volume_multiplier = 0.7
        elif arrival_volume_tons < 150.0:
            volume_multiplier = 1.2
        else:
            volume_multiplier = 1.0

        effective_daily_rate = (base_daily_growth_pct * volume_multiplier) + (historical_daily_momentum / current_price * 0.2)

        # 4. Generate daily forecast trajectory (deterministic logarithmic/dampened growth curve)
        daily_forecast = []
        running_price = current_price

        for day in range(1, horizon_days + 1):
            # Dampening factor reduces growth acceleration over longer horizons to prevent unrealistic exponential divergence
            dampening = 1.0 / (1.0 + 0.02 * (day - 1))
            daily_change = running_price * effective_daily_rate * dampening
            running_price = round(running_price + daily_change, 2)
            daily_forecast.append({"day": day, "price": running_price})

        projected_price = daily_forecast[-1]["price"]
        peak_point = max(daily_forecast, key=lambda x: x["price"])
        peak_price = peak_point["price"]
        peak_day = peak_point["day"]

        # Confidence calculation based on historical data consistency
        confidence = 0.85 if len(prices) >= 7 else 0.75

        # Explainable reasons
        reasons = [
            f"Historical spot price momentum over last {len(prices)} days indicates a daily change rate of {historical_daily_momentum:+.2f} ₹/kg.",
            f"Market arrival volume ({arrival_volume_tons:.1f} tons) applies a volume adjustment factor of {volume_multiplier:.2f}x.",
            f"Trend signal '{trend_signal}' projects a {signal_trend} price trajectory over the {horizon_days}-day horizon."
        ]

        return {
            "forecast_horizon_days": horizon_days,
            "current_price": current_price,
            "projected_price": projected_price,
            "peak_price": peak_price,
            "peak_day": peak_day,
            "daily_forecast": daily_forecast,
            "trend": signal_trend,
            "confidence": confidence,
            "reasons": reasons
        }
