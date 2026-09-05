"""
Buyers Route
GET /api/buyers
"""

from fastapi import APIRouter, Query
from services.buyer_service import BuyerService
from database.supabase_client import get_supabase_client

router = APIRouter(prefix="/api", tags=["Buyers"])

@router.get("/buyers")
def get_buyer_info(crop: str = Query("Tomato", description="Crop name")):
    db = get_supabase_client()
    buyer_service = BuyerService(db_client=db)
    return buyer_service.get_buyers_for_crop(crop)
