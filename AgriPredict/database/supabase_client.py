"""
Supabase Client Module (AgriPredict AI Engine)

Handles safe connection initialization to Supabase hosted PostgreSQL backend.
Provides fallback mechanisms when unconfigured or offline without disrupting application startup.
"""

import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

supabase = None

if SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL.startswith("http"):
    try:
        from supabase import create_client, Client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        # Safe fallback logging without printing sensitive credentials
        print(f"[Database] Info: Supabase client connection initialization deferred ({type(e).__name__}). Using demo JSON fallback service.")
        supabase = None

def get_supabase_client():
    """
    Returns the initialized Supabase client instance or None if unconfigured.
    """
    return supabase

def get_supabase_status() -> dict:
    """
    Returns safe connection status summary without exposing credentials.
    """
    is_connected = supabase is not None
    return {
        "connected": is_connected,
        "mode": "supabase" if is_connected else "demo_fallback"
    }
