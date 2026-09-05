"""
Analysis Route (AgriPredict AI Engine)
POST /api/analyze

Orchestrates complete decision support pipeline:
FarmerInput -> Market Service -> Price Forecaster -> Storage Service -> Arbitrage Engine -> Buyer Matcher -> Recommendation Engine -> CompleteAnalysisResponse
"""

from fastapi import APIRouter, HTTPException, status
from models.schemas import FarmerInput, CompleteAnalysisResponse
from services.market_service import MarketService
from services.storage_service import StorageService
from services.buyer_service import BuyerService
from ai.price_forecaster import PriceForecaster
from ai.arbitrage_engine import ArbitrageEngine
from ai.buyer_matcher import BuyerMatcher
from ai.recommendation_engine import RecommendationEngine
from database.supabase_client import get_supabase_client

router = APIRouter(prefix="/api", tags=["Analysis"])

@router.post("/analyze", response_model=CompleteAnalysisResponse)
def analyze_harvest(farmer_input: FarmerInput):
    """
    Executes end-to-end AI Decision Optimization pipeline for harvest.
    """
    # 1. Validation of input parameters
    if farmer_input.quantity_kg <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produce quantity (quantity_kg) must be greater than zero."
        )

    horizon_days = farmer_input.expected_storage_days or 14
    if horizon_days < 14 or horizon_days > 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Storage horizon days must be between 14 and 30 days."
        )

    try:
        # Initialize database client and services
        db = get_supabase_client()
        market_service = MarketService(db_client=db)
        storage_service = StorageService(db_client=db)
        buyer_service = BuyerService(db_client=db)

        price_forecaster = PriceForecaster()
        arbitrage_engine = ArbitrageEngine()
        buyer_matcher = BuyerMatcher()
        recommendation_engine = RecommendationEngine()

        # 2. Retrieve Market Data
        market_data_dict = market_service.get_market_data(farmer_input.crop, farmer_input.local_market)
        current_price = market_data_dict.get("current_price", 20.0)
        historical_prices = market_data_dict.get("historical_prices", [current_price])
        arrival_volume = market_data_dict.get("arrival_volume_tons", 100.0)
        trend_signal = market_data_dict.get("trend", "stable")
        data_source = market_data_dict.get("data_source", "demo_fallback")

        # 3. Generate Price Forecast
        forecast_dict = price_forecaster.forecast_prices(
            crop=farmer_input.crop,
            current_price=current_price,
            historical_prices=historical_prices,
            arrival_volume_tons=arrival_volume,
            trend_signal=trend_signal,
            horizon_days=horizon_days
        )
        projected_future_price = forecast_dict["projected_price"]

        # 4. Storage Economics & Facility Selection
        optimal_storage = storage_service.select_optimal_facility(
            quantity_kg=farmer_input.quantity_kg,
            storage_days=horizon_days,
            preferred_location=farmer_input.location
        )

        if optimal_storage:
            daily_rate = optimal_storage.get("daily_cost_per_kg", 0.0714)
            storage_cost_per_kg = daily_rate * horizon_days
            transit_cost_total = optimal_storage.get("estimated_transit_cost", 50.0)
            transit_cost_per_kg = transit_cost_total / farmer_input.quantity_kg
        else:
            storage_cost_per_kg = 0.10 * horizon_days
            transit_cost_per_kg = 0.02
            transit_cost_total = transit_cost_per_kg * farmer_input.quantity_kg

        # 5. Run Arbitrage Calculation
        spoilage_rate = min(0.15, 0.005 * horizon_days)

        arbitrage_dict = arbitrage_engine.evaluate_arbitrage(
            current_price=current_price,
            projected_future_price=projected_future_price,
            storage_cost_per_kg=storage_cost_per_kg,
            transit_cost_per_kg=transit_cost_per_kg,
            spoilage_rate=spoilage_rate,
            decision_threshold=0.0,
            storage_days=horizon_days
        )

        # 6. Rank Buyers
        raw_buyers = buyer_service.get_buyers_for_crop(farmer_input.crop)
        matched_buyers = buyer_matcher.match_buyers(
            crop=farmer_input.crop,
            quantity_kg=farmer_input.quantity_kg,
            location=farmer_input.location,
            buyers_list=raw_buyers
        )
        top_buyer = matched_buyers[0] if matched_buyers else None

        # 7. Generate Final Recommendation
        rec_dict = recommendation_engine.generate_recommendation(
            farmer_quantity_kg=farmer_input.quantity_kg,
            arbitrage_result=arbitrage_dict,
            forecast_result=forecast_dict,
            selected_storage=optimal_storage,
            top_buyer=top_buyer
        )

        # 8. Assemble & Return Complete Analysis Response
        response_payload = {
            "farmer_input": farmer_input,
            "market_data": {
                "crop": market_data_dict.get("crop", farmer_input.crop),
                "current_price": current_price,
                "unit": market_data_dict.get("unit", "kg"),
                "arrival_volume_tons": arrival_volume,
                "trend": trend_signal,
                "location": market_data_dict.get("location", "Local Mandi"),
                "historical_prices": historical_prices,
                "data_source": data_source
            },
            "forecast": {
                "forecast_horizon_days": horizon_days,
                "current_price": current_price,
                "projected_price": projected_future_price,
                "peak_price": forecast_dict["peak_price"],
                "peak_day": forecast_dict["peak_day"],
                "daily_forecast": forecast_dict["daily_forecast"],
                "trend": forecast_dict["trend"],
                "confidence": forecast_dict["confidence"],
                "reasons": forecast_dict["reasons"]
            },
            "arbitrage": arbitrage_dict,
            "recommendation": rec_dict,
            "recommended_storage": optimal_storage,
            "top_buyers": matched_buyers,
            "data_source": data_source
        }

        return response_payload

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during AI analysis: {str(e)}"
        )
