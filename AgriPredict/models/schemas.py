"""
Pydantic Data Schemas for AgriPredict AI Engine
Defines complete data contracts for API requests, services, and AI calculations.
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class FarmerInput(BaseModel):
    crop: str = Field(..., example="Tomato", description="Crop type name")
    variety: Optional[str] = Field(default="Standard", example="Roma")
    cultivation_area: Optional[float] = Field(default=1.0, ge=0, description="Area in acres/hectares")
    expected_harvest_window: Optional[str] = Field(default="Immediate", description="Harvest date / window")
    local_market: Optional[str] = Field(default=None, description="Local market name or ID")
    location: Optional[str] = Field(default="Local Agro Zone", description="Farmer location or district")
    quantity_kg: float = Field(..., gt=0, example=5000, description="Available produce quantity in kg")
    expected_storage_days: Optional[int] = Field(default=14, ge=14, le=30, description="Storage horizon days")
    target_mandi: Optional[str] = Field(default=None, description="Target wholesale market")

class MarketData(BaseModel):
    crop: str
    current_price: float = Field(..., gt=0)
    unit: str = "kg"
    arrival_volume_tons: float
    trend: str
    location: str
    historical_prices: List[float] = []
    data_source: Optional[str] = "demo_fallback"

class ForecastPoint(BaseModel):
    day: int
    price: float

class ForecastOutput(BaseModel):
    forecast_horizon_days: int
    current_price: float
    projected_price: float
    peak_price: float
    peak_day: int
    daily_forecast: List[ForecastPoint]
    trend: str
    confidence: float
    reasons: List[str]

class StorageInfo(BaseModel):
    facility_id: str
    name: str
    location: str
    distance_km: float
    daily_cost_per_kg: float
    capacity_kg: float
    available_capacity_kg: float
    rating: float
    estimated_transit_cost: float = 0.0
    total_storage_cost: float = 0.0
    data_source: Optional[str] = "demo_fallback"

class BuyerInfo(BaseModel):
    buyer_id: str
    company_name: str
    buyer_type: str = "Commercial Buyer"
    demand_score: float
    offered_price_per_kg: float
    capacity_kg: float
    distance_km: float
    preferred_crops: List[str] = []
    match_score: float = 0.0
    match_reasons: List[str] = []
    data_source: Optional[str] = "demo_fallback"

class ArbitrageResult(BaseModel):
    optimal_storage_days: int
    current_price: float
    projected_future_price: float
    spoilage_rate: float
    gross_future_value: float
    spoilage_adjusted_future_value: float
    total_hold_cost: float
    net_future_value: float
    net_profit_differential: float
    profit_gain_percentage: float
    break_even_future_price: float
    recommendation_action: str

class Recommendation(BaseModel):
    action: str  # "STORE & HOLD" or "SELL IMMEDIATELY"
    confidence: float
    current_sale_value: float
    future_sale_value: float
    storage_cost: float
    transit_cost: float
    spoilage_loss: float
    economic_difference: float
    break_even_price: float
    reasons: List[str]
    risks: List[str]

class CompleteAnalysisResponse(BaseModel):
    farmer_input: FarmerInput
    market_data: MarketData
    forecast: ForecastOutput
    arbitrage: ArbitrageResult
    recommendation: Recommendation
    recommended_storage: Optional[StorageInfo]
    top_buyers: List[BuyerInfo]
    data_source: Optional[str] = "demo_fallback"
