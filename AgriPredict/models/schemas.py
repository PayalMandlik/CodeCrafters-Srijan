"""
Pydantic Data Schemas for AgriPredict AI Engine
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class FarmerInput(BaseModel):
    crop: str = Field(..., example="Tomato")
    variety: Optional[str] = Field(default="Hybrid", example="Roma")
    quantity_kg: float = Field(..., gt=0, example=5000)
    harvest_date: str = Field(..., example="2026-09-10")
    location: str = Field(..., example="Zone-B Agro Hub")
    target_mandi: Optional[str] = Field(default="Central Market", example="Central Market")

class MarketData(BaseModel):
    crop: str
    current_price: float
    unit: str = "kg"
    arrival_volume_tons: float
    trend: str
    location: str

class ForecastPoint(BaseModel):
    day: int
    price: float

class ForecastOutput(BaseModel):
    horizon_days: int
    projected_prices: List[ForecastPoint]
    peak_price: float
    peak_day: int

class StorageInfo(BaseModel):
    facility_id: str
    name: str
    distance_km: float
    daily_cost_per_kg: float
    capacity_kg: float
    available_capacity_kg: float
    rating: float

class BuyerInfo(BaseModel):
    buyer_id: str
    company_name: str
    demand_score: float
    offered_price_per_kg: float
    capacity_kg: float
    distance_km: float
    preferred_crops: List[str]

class ArbitrageResult(BaseModel):
    optimal_storage_days: int
    immediate_sale_revenue: float
    projected_stored_revenue: float
    total_storage_cost: float
    transit_cost: float
    spoilage_loss: float
    net_profit_differential: float
    profit_gain_percentage: float

class Recommendation(BaseModel):
    action: str  # "STORE & HOLD" or "SELL IMMEDIATELY"
    confidence_score: float
    reasoning: str
    optimal_storage_days: int

class CompleteAnalysisResponse(BaseModel):
    farmer_input: FarmerInput
    market_data: MarketData
    forecast: ForecastOutput
    arbitrage: ArbitrageResult
    recommendation: Recommendation
    recommended_storage: Optional[StorageInfo]
    top_buyers: List[BuyerInfo]
