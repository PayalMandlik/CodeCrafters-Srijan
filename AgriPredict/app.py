"""
AgriPredict AI Engine - FastAPI Application Entry Point
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes.health import router as health_router
from routes.analysis import router as analysis_router
from routes.market import router as market_router
from routes.storage import router as storage_router
from routes.buyers import router as buyers_router

app = FastAPI(
    title="AgriPredict AI Engine",
    description="AI-powered agricultural supply-chain and decision-support platform MVP",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directory path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Register API Routers
app.include_router(health_router)
app.include_router(analysis_router)
app.include_router(market_router)
app.include_router(storage_router)
app.include_router(buyers_router)

@app.get("/", response_class=FileResponse)
def read_root():
    """
    Serves the main AgriPredict HTML dashboard.
    """
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    return FileResponse(index_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
