"""
Supabase Client Module
Handles connection initialization to Supabase hosted PostgreSQL backend.
"""

import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

supabase = None

try:
    if SUPABASE_URL and SUPABASE_KEY:
        from supabase import create_client, Client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    else:
        # Fallback for local initialization without credentials
        supabase = None
except Exception as e:
    print(f"Warning: Supabase client initialization failed ({e}). Falling back to local data service.")
    supabase = None

def get_supabase_client():
    """
    Returns the initialized Supabase client instance or None if unconfigured.
    """
    return supabase
