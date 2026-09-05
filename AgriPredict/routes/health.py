"""
Health Route
GET /health
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AgriPredict AI Engine MVP",
        "version": "1.0.0"
    }
