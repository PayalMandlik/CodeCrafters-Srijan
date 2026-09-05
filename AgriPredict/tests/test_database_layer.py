"""
Unit Tests for Supabase Database Layer & Fallback Architecture
Tests Mode A (Supabase), Mode B (Fallback), Mode C (Empty DB Table Controlled Fallback), and Client Security.
"""

from database.supabase_client import get_supabase_client, get_supabase_status
from services.market_service import MarketService
from services.storage_service import StorageService
from services.buyer_service import BuyerService

class MockSupabaseTable:
    def __init__(self, data_to_return):
        self._data = data_to_return

    def select(self, *args, **kwargs):
        return self

    def ilike(self, *args, **kwargs):
        return self

    def eq(self, *args, **kwargs):
        return self

    def order(self, *args, **kwargs):
        return self

    def execute(self):
        class Response:
            def __init__(self, data):
                self.data = data
        return Response(self._data)

class MockSupabaseClient:
    def __init__(self, tables_data=None):
        self.tables_data = tables_data or {}

    def table(self, table_name):
        data = self.tables_data.get(table_name, [])
        return MockSupabaseTable(data)

def test_supabase_client_safe_unconfigured():
    """Mode B: Unconfigured client returns None without crashing."""
    status = get_supabase_status()
    assert "connected" in status
    assert "mode" in status

def test_market_service_fallback_mode():
    """Mode B: Null DB client falls back to demo_data.json."""
    service = MarketService(db_client=None)
    data = service.get_market_data("Tomato")
    assert data["crop"].lower() == "tomato"
    assert data["data_source"] == "demo_fallback"
    assert "historical_prices" in data

def test_market_service_supabase_mode():
    """Mode A: Valid Supabase query returns Supabase data source."""
    mock_db = MockSupabaseClient({
        "market_prices": [
            {
                "crop": "Tomato",
                "price_per_kg": 21.50,
                "arrival_volume_kg": 190000.0,
                "market_location": "Nashik Mandi",
                "recorded_at": "2026-09-05T10:00:00Z"
            }
        ]
    })
    service = MarketService(db_client=mock_db)
    data = service.get_market_data("Tomato")
    assert data["data_source"] == "supabase"
    assert data["current_price"] == 21.50

def test_market_service_empty_table_controlled_fallback():
    """Mode C: Controlled fallback to demo JSON if Supabase table is empty."""
    mock_db = MockSupabaseClient({"market_prices": []})
    service = MarketService(db_client=mock_db)
    data = service.get_market_data("Tomato")
    assert data["data_source"] == "demo_fallback"
    assert data["current_price"] > 0

def test_storage_service_fallback_and_supabase_modes():
    """Mode A & B for StorageService."""
    # Fallback mode
    srv_fallback = StorageService(db_client=None)
    facs_fb = srv_fallback.get_facilities()
    assert len(facs_fb) > 0
    assert facs_fb[0]["data_source"] == "demo_fallback"

    # Supabase mode
    mock_db = MockSupabaseClient({
        "cold_storage": [
            {
                "id": "CS-999",
                "facility_name": "Supabase Cold Vault",
                "location": "Nashik Zone B",
                "distance_km": 10.0,
                "storage_rate_per_kg_per_day": 0.06,
                "total_capacity_kg": 400000.0,
                "available_capacity_kg": 150000.0,
                "rating": 4.9,
                "is_active": True
            }
        ]
    })
    srv_supa = StorageService(db_client=mock_db)
    facs_supa = srv_supa.get_facilities()
    assert len(facs_supa) == 1
    assert facs_supa[0]["data_source"] == "supabase"
    assert facs_supa[0]["name"] == "Supabase Cold Vault"

def test_buyer_service_fallback_and_supabase_modes():
    """Mode A & B for BuyerService."""
    # Fallback mode
    srv_fallback = BuyerService(db_client=None)
    buyers_fb = srv_fallback.get_buyers_for_crop("Tomato")
    assert len(buyers_fb) > 0
    assert buyers_fb[0]["data_source"] == "demo_fallback"

    # Supabase mode
    mock_db = MockSupabaseClient({
        "buyers": [
            {
                "id": "BY-999",
                "buyer_name": "Supabase Agri Corp",
                "buyer_type": "Food Processor",
                "crop": "Tomato",
                "demand_score": 92.0,
                "offered_price_per_kg": 27.00,
                "capacity_kg": 30000.0,
                "distance_km": 20.0,
                "is_active": True
            }
        ]
    })
    srv_supa = BuyerService(db_client=mock_db)
    buyers_supa = srv_supa.get_buyers_for_crop("Tomato")
    assert len(buyers_supa) == 1
    assert buyers_supa[0]["data_source"] == "supabase"
    assert buyers_supa[0]["company_name"] == "Supabase Agri Corp"
