"""
Pydantic models for API request/response validation.
Designed for Swift Codable compatibility.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ErrorDetail(BaseModel):
    """Error detail model for consistent error responses."""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: ErrorDetail


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    page: int
    per_page: int
    total: int
    has_next: bool
    has_prev: bool


class EventInfo(BaseModel):
    """Event information model."""
    event_name: str = Field(alias="EventName")
    event_date: Optional[str] = Field(None, alias="EventDate")
    event_format: Optional[str] = Field(None, alias="EventFormat")
    location: Optional[str] = Field(None, alias="Location")
    country: Optional[str] = Field(None, alias="Country")
    timezone: Optional[str] = Field(None, alias="Timezone")
    
    class Config:
        populate_by_name = True


class SessionInfo(BaseModel):
    """Session information model."""
    session_name: str
    session_date: Optional[str] = None
    session_type: str
    event_name: Optional[str] = None
    year: int


class DriverInfo(BaseModel):
    """Driver information model."""
    abbreviation: str
    full_name: str
    team_name: Optional[str] = None
    team_color: Optional[str] = None
    country_code: Optional[str] = None


class LapTime(BaseModel):
    """Lap time data model."""
    driver_number: Optional[int] = None
    driver: Optional[str] = None
    lap_number: Optional[int] = None
    lap_time: Optional[float] = None
    sector1_time: Optional[float] = None
    sector2_time: Optional[float] = None
    sector3_time: Optional[float] = None
    is_personal_best: Optional[bool] = None
    is_fastest_lap: Optional[bool] = None
    compound: Optional[str] = None
    tyre_life: Optional[int] = None


class RaceResult(BaseModel):
    """Race result model."""
    position: Optional[int] = None
    driver_number: Optional[int] = None
    abbreviation: Optional[str] = None
    full_name: Optional[str] = None
    team_name: Optional[str] = None
    points: Optional[float] = None
    time: Optional[str] = None
    status: Optional[str] = None
    fastest_lap: Optional[bool] = None


class TelemetryPoint(BaseModel):
    """Single telemetry data point."""
    time: Optional[float] = None
    session_time: Optional[float] = None
    distance: Optional[float] = None
    rpm: Optional[int] = None
    speed: Optional[float] = None
    throttle: Optional[float] = None
    brake: Optional[bool] = None
    drs: Optional[int] = None
    gear: Optional[int] = None
    brake_pressure: Optional[float] = None
    steering_angle: Optional[float] = None
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None


class ResponseWrapper(BaseModel):
    """Generic response wrapper for consistent API responses."""
    data: Any
    meta: Optional[Dict[str, Any]] = None


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    data: List[Any]
    pagination: PaginationMeta

