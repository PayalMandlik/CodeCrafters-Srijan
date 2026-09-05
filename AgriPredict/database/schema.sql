-- ====================================================================
-- AgriPredict AI Engine - PostgreSQL Schema Definition (Supabase)
-- ====================================================================

-- 1. Market Prices Table
CREATE TABLE IF NOT EXISTS market_prices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    crop VARCHAR(100) NOT NULL,
    variety VARCHAR(100) DEFAULT 'Standard',
    market VARCHAR(150) NOT NULL,
    market_location VARCHAR(150),
    price_per_kg NUMERIC(10, 2) NOT NULL CHECK (price_per_kg > 0),
    arrival_volume_kg NUMERIC(12, 2) DEFAULT 0.0 CHECK (arrival_volume_kg >= 0),
    recorded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_market_prices_crop_market_recorded 
ON market_prices(crop, market, recorded_at DESC);


-- 2. Cold Storage Facilities Table
CREATE TABLE IF NOT EXISTS cold_storage (
    id VARCHAR(50) PRIMARY KEY,
    facility_name VARCHAR(200) NOT NULL,
    location VARCHAR(200) NOT NULL,
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    total_capacity_kg NUMERIC(14, 2) NOT NULL CHECK (total_capacity_kg >= 0),
    available_capacity_kg NUMERIC(14, 2) NOT NULL CHECK (available_capacity_kg >= 0),
    storage_rate_per_kg_per_day NUMERIC(8, 4) NOT NULL CHECK (storage_rate_per_kg_per_day >= 0),
    distance_km NUMERIC(8, 2) NOT NULL CHECK (distance_km >= 0),
    transit_cost_per_kg NUMERIC(8, 4) DEFAULT 0.0 CHECK (transit_cost_per_kg >= 0),
    rating NUMERIC(3, 2) DEFAULT 4.5 CHECK (rating >= 0.0 AND rating <= 5.0),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_cold_storage_location_active 
ON cold_storage(location, is_active);


-- 3. Commercial Buyers Table
CREATE TABLE IF NOT EXISTS buyers (
    id VARCHAR(50) PRIMARY KEY,
    buyer_name VARCHAR(200) NOT NULL,
    buyer_type VARCHAR(100) NOT NULL,
    crop VARCHAR(100) NOT NULL,
    market_location VARCHAR(200),
    demand_score NUMERIC(5, 2) NOT NULL CHECK (demand_score >= 0 AND demand_score <= 100),
    capacity_kg NUMERIC(14, 2) NOT NULL CHECK (capacity_kg >= 0),
    offered_price_per_kg NUMERIC(10, 2) NOT NULL CHECK (offered_price_per_kg >= 0),
    distance_km NUMERIC(8, 2) NOT NULL CHECK (distance_km >= 0),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_buyers_crop_location_active 
ON buyers(crop, market_location, is_active);


-- 4. Farmers Persistence Table (Optional MVP Logging)
CREATE TABLE IF NOT EXISTS farmers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    location VARCHAR(200),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- ====================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ====================================================================

ALTER TABLE market_prices ENABLE ROW LEVEL SECURITY;
ALTER TABLE cold_storage ENABLE ROW LEVEL SECURITY;
ALTER TABLE buyers ENABLE ROW LEVEL SECURITY;
ALTER TABLE farmers ENABLE ROW LEVEL SECURITY;

-- Allow public read access to reference data
CREATE POLICY "Allow public read access to market_prices" 
ON market_prices FOR SELECT USING (true);

CREATE POLICY "Allow public read access to cold_storage" 
ON cold_storage FOR SELECT USING (true);

CREATE POLICY "Allow public read access to buyers" 
ON buyers FOR SELECT USING (true);
