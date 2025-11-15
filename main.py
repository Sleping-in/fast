"""
FastF1 API - Main application entry point.
Provides Formula 1 data via REST API, optimized for Swift app consumption.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from api.routes import events, results, laps, telemetry, drivers, weather, track_status, positions, pit_stops, circuits, race_control, sectors, gaps, tyres, teams, standings
from api.models.schemas import ErrorResponse, ErrorDetail

# Load environment variables
load_dotenv()

# Configure FastF1 cache directory if specified
cache_dir = os.getenv("FASTF1_CACHE_DIR")
if cache_dir:
    import fastf1
    fastf1.Cache.set_cache_dir(cache_dir)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    print("FastF1 API starting up...")
    yield
    # Shutdown
    print("FastF1 API shutting down...")


# Create FastAPI app
app = FastAPI(
    title="FastF1 API",
    description="REST API for Formula 1 data using FastF1 library. Optimized for Swift app consumption.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for Swift app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Swift app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom exception handler for consistent error responses
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent error format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.detail.get("code", "HTTP_ERROR") if isinstance(exc.detail, dict) else "HTTP_ERROR",
                "message": exc.detail.get("message", str(exc.detail)) if isinstance(exc.detail, dict) else str(exc.detail),
                "details": exc.detail.get("details") if isinstance(exc.detail, dict) else None
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred",
                "details": {"type": type(exc).__name__}
            }
        }
    )


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "FastF1 API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


# Include routers
app.include_router(events.router, prefix="/api/v1", tags=["Events"])
app.include_router(results.router, prefix="/api/v1", tags=["Results"])
app.include_router(laps.router, prefix="/api/v1", tags=["Laps"])
app.include_router(telemetry.router, prefix="/api/v1", tags=["Telemetry"])
app.include_router(drivers.router, prefix="/api/v1", tags=["Drivers"])
app.include_router(weather.router, prefix="/api/v1", tags=["Weather"])
app.include_router(track_status.router, prefix="/api/v1", tags=["Track Status"])
app.include_router(positions.router, prefix="/api/v1", tags=["Positions"])
app.include_router(pit_stops.router, prefix="/api/v1", tags=["Pit Stops"])
app.include_router(circuits.router, prefix="/api/v1", tags=["Circuits"])
app.include_router(race_control.router, prefix="/api/v1", tags=["Race Control"])
app.include_router(sectors.router, prefix="/api/v1", tags=["Sectors"])
app.include_router(gaps.router, prefix="/api/v1", tags=["Gaps"])
app.include_router(tyres.router, prefix="/api/v1", tags=["Tyres"])
app.include_router(teams.router, prefix="/api/v1", tags=["Teams"])
app.include_router(standings.router, prefix="/api/v1", tags=["Standings"])


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

