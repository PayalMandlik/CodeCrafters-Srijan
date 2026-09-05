# AgriPredict AI Engine - MVP & Interactive Dashboard

AgriPredict is an AI-powered agricultural supply-chain decision-support platform designed to solve information asymmetry, harvest-time market gluts, and post-harvest perishability loss.

## Technology Stack

- **Backend:** Python (FastAPI 0.100+)
- **Primary Data Layer:** Supabase (Hosted PostgreSQL Database)
- **Fallback Data Layer:** Local `data/demo_data.json` deterministic dataset
- **Frontend Stack:** HTML5, Modern CSS3, Vanilla JavaScript (Zero build tools, zero node dependencies)
- **AI/ML Engine:** Python (Cold-Storage Arbitrage Constraint Solver, Time-Series Price Forecaster, Buyer Matchmaker)

## Core Architecture & Data Flow

```text
Dashboard (HTML/CSS/JS)
   │
   ▼
FastAPI Routes (/api/analyze)
   │
   ▼
Data Services (MarketService, StorageService, BuyerService)
   │
   ├──────► Primary: Supabase PostgreSQL Database (schema.sql / seed.sql)
   │        (If configured, accessible, and populated)
   │
   └──────► Fallback: data/demo_data.json
            (If Supabase is unconfigured, offline, or empty)
   │
   ▼
AI Processing Core (PriceForecaster, ArbitrageEngine, BuyerMatcher)
   │
   ▼
Recommendation Engine (STORE & HOLD or SELL IMMEDIATELY)
   │
   ▼
Complete Analysis JSON Response -> Dashboard Render
```

## Supabase PostgreSQL Setup Instructions

1. **Create Supabase Project:** Log in to [Supabase](https://supabase.com) and create a new project.
2. **Execute Database Schema:**
   - Navigate to **SQL Editor** in the Supabase Dashboard.
   - Open `database/schema.sql` and run the script to create tables (`market_prices`, `cold_storage`, `buyers`, `farmers`), indexes, and Row Level Security (RLS) policies.
3. **Seed Synthetic Data:**
   - Open `database/seed.sql` in SQL Editor and run the script to populate deterministic historical price trajectories, cold storage facilities, and buyers.
4. **Configure Environment Credentials:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Set your project URL and Anon key in `.env`:
     ```env
     SUPABASE_URL=https://your-project.supabase.co
     SUPABASE_KEY=your-supabase-anon-key
     ```
5. **Run Application & Test Suite:**
   ```bash
   python run_tests.py
   uvicorn app:app --reload
   ```

## Running Locally (With or Without Supabase)

If Supabase credentials are not provided in `.env`, the application automatically operates in **Demo Fallback Mode** using `data/demo_data.json`.

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run automated test suite:
   ```bash
   python run_tests.py
   ```
3. Start server:
   ```bash
   uvicorn app:app --reload
   ```
4. Access dashboard at `http://127.0.0.1:8000`.

## API Endpoints

- `GET /health` — Health check endpoint.
- `GET /` — Serves the interactive AgriPredict dashboard.
- `POST /api/analyze` — Executes full end-to-end AI decision optimization pipeline.
- `GET /api/markets` — Retrieves spot prices and arrival volume trends.
- `GET /api/storage` — Retrieves cold storage facilities.
- `GET /api/buyers` — Retrieves ranked commercial buyers.
