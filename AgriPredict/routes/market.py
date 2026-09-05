"""
Market Route
GET /api/markets
"""

from fastapi import APIRouter, Query
from services.market_service import MarketService
from database.supabase_client import get_supabase_client

router = APIRouter(prefix="/api", tags=["Market"])

@router.get("/markets")
def get_market_info(crop: str = Query("Tomato", description="Crop name")):
    db = get_supabase_client()
    market_service = MarketService(db_client=db)
    return market_service.get_market_data(crop)
