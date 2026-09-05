"""
Recommendation Engine Module (AgriPredict AI Engine)

Synthesizes outputs from Price Forecaster, Arbitrage Engine, Storage Economics, and Buyer Matcher
into a farmer-friendly actionable decision: 'STORE & HOLD' or 'SELL IMMEDIATELY'.
"""

from typing import Dict, Any, List

class RecommendationEngine:
    """
    Final Decision Synthesis Engine.
    Translates mathematical arbitrage outputs into plain-language financial recommendations.
    """
    def __init__(self):
        pass

    def generate_recommendation(
        self,
        farmer_quantity_kg: float,
        arbitrage_result: Dict[str, Any],
        forecast_result: Dict[str, Any],
        selected_storage: Dict[str, Any] = None,
        top_buyer: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes AI and economic inputs into structured recommendation output.

        Args:
            farmer_quantity_kg: Total produce quantity in kg
            arbitrage_result: Dict output from ArbitrageEngine
            forecast_result: Dict output from PriceForecaster
            selected_storage: Dict output of selected cold-storage facility
            top_buyer: Dict output of top ranked buyer

        Returns:
            Dict matching Recommendation schema.
        """
        action = arbitrage_result.get("recommendation_action", "SELL IMMEDIATELY")
        net_diff_per_kg = arbitrage_result.get("net_profit_differential", 0.0)
        total_economic_diff = net_diff_per_kg * farmer_quantity_kg

        current_price = arbitrage_result.get("current_price", 20.0)
        future_price = arbitrage_result.get("projected_future_price", 25.0)
        spoilage_rate = arbitrage_result.get("spoilage_rate", 0.05)
        storage_days = arbitrage_result.get("optimal_storage_days", 14)

        current_sale_value = round(current_price * farmer_quantity_kg, 2)
        future_sale_value = round(future_price * (1.0 - spoilage_rate) * farmer_quantity_kg, 2)
        
        storage_cost = round(arbitrage_result.get("total_hold_cost", 0.0) * farmer_quantity_kg, 2)
        if selected_storage and "total_storage_cost" in selected_storage:
            storage_cost = selected_storage["total_storage_cost"]
            transit_cost = selected_storage.get("estimated_transit_cost", 0.0)
        else:
            transit_cost = round(arbitrage_result.get("total_hold_cost", 0.0) * 0.3 * farmer_quantity_kg, 2)

        spoilage_loss_value = round(future_price * spoilage_rate * farmer_quantity_kg, 2)
        break_even_price = arbitrage_result.get("break_even_future_price", current_price * 1.15)
        confidence = forecast_result.get("confidence", 0.85)

        reasons = []
        risks = []

        if action == "STORE & HOLD":
            gain_pct = arbitrage_result.get("profit_gain_percentage", 0.0)
            reasons.append(
                f"Expected market price for your produce is projected to rise from ₹{current_price:.2f}/kg to ₹{future_price:.2f}/kg over the next {storage_days} days."
            )
            reasons.append(
                f"Even after accounting for storage fees (₹{storage_cost:,.2f}), transport costs (₹{transit_cost:,.2f}), and estimated spoilage (₹{spoilage_loss_value:,.2f}), holding your crop is projected to yield ₹{total_economic_diff:,.2f} (+{gain_pct:.1f}%) more net profit than selling today."
            )
            if selected_storage:
                reasons.append(
                    f"Optimal storage facility '{selected_storage.get('name')}' ({selected_storage.get('distance_km')} km away) has available capacity at ₹{selected_storage.get('daily_cost_per_kg')}/kg daily."
                )

            risks.append(
                f"Market spot price must stay above the break-even price of ₹{break_even_price:.2f}/kg for storage to remain profitable."
            )
            risks.append(
                "Ensure produce temperature is maintained at cold storage to prevent spoilage exceeding estimated limits."
            )
        else:
            loss_diff = abs(total_economic_diff)
            reasons.append(
                f"Current market spot price is ₹{current_price:.2f}/kg. Market price trends do not project a high enough price surge to cover storage and logistics expenses over the next {storage_days} days."
            )
            reasons.append(
                f"Selling today avoids estimated storage and transport fees of ₹{storage_cost + transit_cost:,.2f} and prevents potential spoilage losses."
            )
            if top_buyer:
                reasons.append(
                    f"Recommended buyer '{top_buyer.get('company_name')}' offers a competitive spot price of ₹{top_buyer.get('offered_price_per_kg')}/kg today."
                )

            risks.append(
                "Local market arrivals may increase in coming days, which could further lower spot prices."
            )

        return {
            "action": action,
            "confidence": confidence,
            "current_sale_value": current_sale_value,
            "future_sale_value": future_sale_value,
            "storage_cost": storage_cost,
            "transit_cost": transit_cost,
            "spoilage_loss": spoilage_loss_value,
            "economic_difference": round(total_economic_diff, 2),
            "break_even_price": round(break_even_price, 2),
            "reasons": reasons,
            "risks": risks
        }
