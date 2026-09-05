"""
Arbitrage Engine Module (AgriPredict AI Engine)

Implements the core economic arbitrage decision formula:
ΔP = spoilage_adjusted_future_value - (current_price + storage_cost + transit_cost)

Determines whether storing produce yield a net financial gain over immediate market sale.
"""

from typing import Dict, Any

class ArbitrageEngine:
    """
    Cold-Storage Arbitrage Constraint Solver.
    Evaluates net profit differential between immediate spot sale vs. deferred cold-storage sale.
    """
    def __init__(self):
        pass

    def evaluate_arbitrage(
        self,
        current_price: float,
        projected_future_price: float,
        storage_cost_per_kg: float,
        transit_cost_per_kg: float,
        spoilage_rate: float = 0.05,
        decision_threshold: float = 0.0,
        storage_days: int = 14
    ) -> Dict[str, Any]:
        """
        Evaluates the economic viability of cold storage.

        Args:
            current_price: Spot price per kg today (> 0)
            projected_future_price: Forecasted price per kg at storage horizon (>= 0)
            storage_cost_per_kg: Total cumulative cold storage cost per kg for storage_days (>= 0)
            transit_cost_per_kg: Logistics and freight cost per kg (>= 0)
            spoilage_rate: Expected cumulative perishability loss percentage (0.0 <= rate < 1.0)
            decision_threshold: Minimum profit differential required to recommend storage (>= 0)
            storage_days: Storage duration in days

        Returns:
            Dict containing gross values, spoilage loss, total hold costs, ΔP differential, break-even price, and action.
        """
        # Validation checks
        if current_price <= 0:
            raise ValueError("Current price must be greater than zero.")
        if projected_future_price < 0:
            raise ValueError("Projected future price cannot be negative.")
        if storage_cost_per_kg < 0:
            raise ValueError("Storage cost cannot be negative.")
        if transit_cost_per_kg < 0:
            raise ValueError("Transit cost cannot be negative.")
        if spoilage_rate < 0.0 or spoilage_rate >= 1.0:
            raise ValueError("Spoilage rate must be between 0.0 and 1.0 (exclusive).")

        # 1. Gross future value per kg
        gross_future_value = projected_future_price

        # 2. Spoilage-adjusted future value per kg
        spoilage_adjusted_future_value = gross_future_value * (1.0 - spoilage_rate)

        # 3. Total additional costs incurred to hold and transport produce
        total_hold_cost = storage_cost_per_kg + transit_cost_per_kg

        # 4. Net future value per kg (after costs and spoilage loss)
        net_future_value = spoilage_adjusted_future_value - total_hold_cost

        # 5. Net Profit Differential (ΔP) per kg
        # ΔP = net_future_value - current_price
        delta_p = net_future_value - current_price

        # 6. Percentage gain or loss relative to current spot price
        profit_gain_percentage = (delta_p / current_price) * 100.0

        # 7. Break-even future price per kg required to achieve zero net profit loss
        # break_even * (1 - spoilage_rate) = current_price + storage_cost + transit_cost
        break_even_future_price = (current_price + total_hold_cost) / (1.0 - spoilage_rate)

        # 8. Decision rule based on ΔP and risk threshold
        recommendation_action = "STORE & HOLD" if delta_p > decision_threshold else "SELL IMMEDIATELY"

        return {
            "optimal_storage_days": storage_days,
            "current_price": round(current_price, 2),
            "projected_future_price": round(projected_future_price, 2),
            "spoilage_rate": round(spoilage_rate, 4),
            "gross_future_value": round(gross_future_value, 2),
            "spoilage_adjusted_future_value": round(spoilage_adjusted_future_value, 2),
            "total_hold_cost": round(total_hold_cost, 2),
            "net_future_value": round(net_future_value, 2),
            "net_profit_differential": round(delta_p, 2),
            "profit_gain_percentage": round(profit_gain_percentage, 2),
            "break_even_future_price": round(break_even_future_price, 2),
            "recommendation_action": recommendation_action
        }
