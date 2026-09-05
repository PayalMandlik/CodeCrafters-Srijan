"""
Storage Route
GET /api/storage
"""

from fastapi import APIRouter, Query
from services.storage_service import StorageService
from database.supabase_client import get_supabase_client

router = APIRouter(prefix="/api", tags=["Storage"])

@router.get("/storage")
def get_storage_info(location: str = Query(None, description="Location query")):
    db = get_supabase_client()
    storage_service = StorageService(db_client=db)
    return storage_service.get_nearby_facilities(location)
