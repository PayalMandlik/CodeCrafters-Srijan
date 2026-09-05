# AgriPredict AI Engine MVP

AgriPredict is an AI-powered agricultural supply-chain and decision-support platform designed to solve information asymmetry, harvest-time market gluts, and post-harvest produce spoilage.

## Architecture

- **Backend Framework:** FastAPI (Python 3.10+)
- **Database:** Supabase (Hosted PostgreSQL)
- **Frontend Stack:** HTML5, Modern CSS3, Vanilla JavaScript
- **AI/ML Engine:** Python (Arbitrage Constraint Solver, Time-Series Price Forecaster, Buyer Matchmaker)

## Running Locally

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure `.env`:
   ```bash
   cp .env.example .env
   ```
3. Start the application:
   ```bash
   uvicorn app:app --reload
   ```
4. Access dashboard at `http://127.0.0.1:8000`.
