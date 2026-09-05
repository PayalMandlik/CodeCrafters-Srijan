-- ====================================================================
-- AgriPredict AI Engine - Synthetic Seed Data (Supabase)
-- NOTE: SYNTHETIC DEMO DATA for testing & demonstration purposes.
-- ====================================================================

-- Clear existing records
TRUNCATE TABLE market_prices, cold_storage, buyers, farmers RESTART IDENTITY;

-- 1. Seed Market Prices (Historical Price Trajectory Series)
-- Tomato - Nashik Mandi (Glut recovery curve: 16.50 to 20.00)
INSERT INTO market_prices (crop, variety, market, market_location, price_per_kg, arrival_volume_kg, recorded_at) VALUES
('Tomato', 'Roma', 'Nashik Mandi', 'Nashik Regional Mandi', 16.50, 220000.0, NOW() - INTERVAL '7 days'),
('Tomato', 'Roma', 'Nashik Mandi', 'Nashik Regional Mandi', 17.00, 210000.0, NOW() - INTERVAL '6 days'),
('Tomato', 'Roma', 'Nashik Mandi', 'Nashik Regional Mandi', 17.50, 205000.0, NOW() - INTERVAL '5 days'),
('Tomato', 'Roma', 'Nashik Mandi', 'Nashik Regional Mandi', 18.00, 200000.0, NOW() - INTERVAL '4 days'),
('Tomato', 'Roma', 'Nashik Mandi', 'Nashik Regional Mandi', 18.50, 195000.0, NOW() - INTERVAL '3 days'),
('Tomato', 'Roma', 'Nashik Mandi', 'Nashik Regional Mandi', 19.00, 190000.0, NOW() - INTERVAL '2 days'),
('Tomato', 'Roma', 'Nashik Mandi', 'Nashik Regional Mandi', 19.50, 185000.0, NOW() - INTERVAL '1 days'),
('Tomato', 'Roma', 'Nashik Mandi', 'Nashik Regional Mandi', 20.00, 180500.0, NOW());

-- Potato - Agra Wholesale Market (Stable market: 18.00)
INSERT INTO market_prices (crop, variety, market, market_location, price_per_kg, arrival_volume_kg, recorded_at) VALUES
('Potato', 'Desi', 'Agra Wholesale Market', 'Agra Wholesale Market', 18.00, 320000.0, NOW() - INTERVAL '7 days'),
('Potato', 'Desi', 'Agra Wholesale Market', 'Agra Wholesale Market', 18.10, 320000.0, NOW() - INTERVAL '6 days'),
('Potato', 'Desi', 'Agra Wholesale Market', 'Agra Wholesale Market', 17.90, 325000.0, NOW() - INTERVAL '5 days'),
('Potato', 'Desi', 'Agra Wholesale Market', 'Agra Wholesale Market', 18.00, 320000.0, NOW() - INTERVAL '4 days'),
('Potato', 'Desi', 'Agra Wholesale Market', 'Agra Wholesale Market', 18.20, 318000.0, NOW() - INTERVAL '3 days'),
('Potato', 'Desi', 'Agra Wholesale Market', 'Agra Wholesale Market', 18.00, 320000.0, NOW() - INTERVAL '2 days'),
('Potato', 'Desi', 'Agra Wholesale Market', 'Agra Wholesale Market', 17.90, 322000.0, NOW() - INTERVAL '1 days'),
('Potato', 'Desi', 'Agra Wholesale Market', 'Agra Wholesale Market', 18.00, 320000.0, NOW());

-- Onion - Lasalgaon Mandi (Rising trend: 24.00 to 32.00)
INSERT INTO market_prices (crop, variety, market, market_location, price_per_kg, arrival_volume_kg, recorded_at) VALUES
('Onion', 'Nasik Red', 'Lasalgaon Mandi', 'Lasalgaon Mandi', 24.00, 250000.0, NOW() - INTERVAL '7 days'),
('Onion', 'Nasik Red', 'Lasalgaon Mandi', 'Lasalgaon Mandi', 25.50, 240000.0, NOW() - INTERVAL '6 days'),
('Onion', 'Nasik Red', 'Lasalgaon Mandi', 'Lasalgaon Mandi', 27.00, 230000.0, NOW() - INTERVAL '5 days'),
('Onion', 'Nasik Red', 'Lasalgaon Mandi', 'Lasalgaon Mandi', 28.20, 225000.0, NOW() - INTERVAL '4 days'),
('Onion', 'Nasik Red', 'Lasalgaon Mandi', 'Lasalgaon Mandi', 29.50, 220000.0, NOW() - INTERVAL '3 days'),
('Onion', 'Nasik Red', 'Lasalgaon Mandi', 'Lasalgaon Mandi', 30.50, 215000.0, NOW() - INTERVAL '2 days'),
('Onion', 'Nasik Red', 'Lasalgaon Mandi', 'Lasalgaon Mandi', 31.20, 212000.0, NOW() - INTERVAL '1 days'),
('Onion', 'Nasik Red', 'Lasalgaon Mandi', 'Lasalgaon Mandi', 32.00, 210000.0, NOW());

-- 2. Seed Cold Storage Facilities
INSERT INTO cold_storage (id, facility_name, location, latitude, longitude, total_capacity_kg, available_capacity_kg, storage_rate_per_kg_per_day, distance_km, transit_cost_per_kg, rating, is_active) VALUES
('CS-101', 'AgroChill Cold Logistics Hub', 'Nashik Highway Zone B', 19.9975, 73.7898, 500000.0, 145000.0, 0.0714, 12.4, 0.298, 4.8, TRUE),
('CS-102', 'Kisan Vault Warehouse', 'District Sector 4', 20.0050, 73.8100, 300000.0, 80000.0, 0.0500, 28.1, 0.612, 4.5, TRUE),
('CS-103', 'EcoPreserve Rural Storage', 'Green Agri Corridor', 19.9800, 73.7500, 200000.0, 95000.0, 0.0850, 8.5, 0.220, 4.6, TRUE);

-- 3. Seed Commercial Buyers
INSERT INTO buyers (id, buyer_name, buyer_type, crop, market_location, demand_score, capacity_kg, offered_price_per_kg, distance_km, is_active) VALUES
('BY-301', 'FreshFoods Processing Ltd', 'Food Processor', 'Tomato', 'Nashik Agro Corridor', 94.5, 25000.0, 26.50, 35.0, TRUE),
('BY-302', 'GreenGrocer Hypermarket Chain', 'Retail Chain', 'Tomato', 'Nashik Agro Corridor', 88.0, 15000.0, 25.00, 18.5, TRUE),
('BY-303', 'AgriExport Global Traders', 'Institutional Exporter', 'Tomato', 'Nashik Agro Corridor', 91.0, 50000.0, 27.20, 50.0, TRUE),
('BY-304', 'Agra Chips & Flakes Plant', 'Food Processor', 'Potato', 'Agra Sector 4', 85.0, 40000.0, 18.20, 22.0, TRUE),
('BY-305', 'National Retail Mart', 'Retail Chain', 'Potato', 'Agra Sector 4', 80.0, 20000.0, 18.00, 15.0, TRUE),
('BY-306', 'Global Spice Exporters', 'Institutional Exporter', 'Onion', 'Lasalgaon Mandi', 95.0, 60000.0, 33.50, 40.0, TRUE);
