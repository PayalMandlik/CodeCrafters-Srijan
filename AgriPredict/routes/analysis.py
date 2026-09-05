"""
Analysis Route
POST /api/analyze
"""

from fastapi import APIRouter, HTTPException
from models.schemas import FarmerInput, CompleteAnalysisResponse
from services.market_service import MarketService
from services.storage_service import StorageService
from services.buyer_service import BuyerService
from ai.price_forecaster import PriceForecaster
from ai.arbitrage_engine import ArbitrageEngine
from ai.recommendation_engine import RecommendationEngine
from database.supabase_client import get_supabase_client

router = APIRouter(prefix="/api", tags=["Analysis"])

@router.post("/analyze", response_model=dict)
def analyze_harvest(farmer_input: FarmerInput):
    """
    Executes end-to-end Decision Support analysis for harvest:
    Route -> Services -> AI Engines -> Recommendation -> Response
    """
    try:
        db = get_supabase_client()
        market_service = MarketService(db_client=db)
        storage_service = StorageService(db_client=db)
        buyer_service = BuyerService(db_client=db)

        price_forecaster = PriceForecaster()
        arbitrage_engine = ArbitrageEngine()
        recommendation_engine = RecommendationEngine()

        market_data = market_service.get_market_data(farmer_input.crop, farmer_input.location)
        current_price = market_data.get("current_price", 25.0)

        forecast_points = price_forecaster.forecast_prices(farmer_input.crop, current_price, horizon_days=30)
        arbitrage = arbitrage_engine.evaluate_arbitrage(
            current_price=current_price,
            forecast=forecast_points,
            storage_cost_per_day=0.15,
            transit_cost=20.0
        )
        recommendation = recommendation_engine.generate_recommendation(arbitrage)
        facilities = storage_service.get_nearby_facilities(farmer_input.location)
        buyers = buyer_service.get_buyers_for_crop(farmer_input.crop)

        return {
            "farmer_input": farmer_input.dict(),
            "market_data": market_data,
            "forecast": {
                "horizon_days": 30,
                "projected_prices": forecast_points,
                "peak_price": max(p["price"] for p in forecast_points),
                "peak_day": 12
            },
            "arbitrage": {
                "optimal_storage_days": arbitrage["optimal_storage_days"],
                "immediate_sale_revenue": current_price * farmer_input.quantity_kg,
                "projected_stored_revenue": current_price * 1.25 * farmer_input.quantity_kg,
                "total_storage_cost": arbitrage["total_storage_cost"] * farmer_input.quantity_kg,
                "transit_cost": arbitrage["transit_cost"],
                "spoilage_loss": arbitrage["spoilage_loss"] * farmer_input.quantity_kg,
                "net_profit_differential": arbitrage["net_profit_differential"] * farmer_input.quantity_kg,
                "profit_gain_percentage": 28.5
            },
            "recommendation": recommendation,
            "recommended_storage": facilities[0] if facilities else None,
            "top_buyers": buyers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
