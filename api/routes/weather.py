"""
Weather data endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import fastf1
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list, datetime_to_iso8601

router = APIRouter()


@router.get("/weather/{year}/{event_name}/{session_type}", response_model=ResponseWrapper)
def get_weather(
    year: int,
    event_name: str,
    session_type: str,
    time: Optional[str] = Query(None, description="Specific timestamp (ISO 8601 format)")
):
    """
    Get weather data for a session.
    Session types: FP1, FP2, FP3, Q, R, S, SQ
    """
    valid_types = ['FP1', 'FP2', 'FP3', 'Q', 'R', 'S', 'SQ']
    if session_type.upper() not in valid_types:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_SESSION_TYPE",
                "message": f"Invalid session type. Must be one of: {', '.join(valid_types)}",
                "details": {"provided": session_type}
            }
        )
    
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        if not hasattr(session, 'weather') or session.weather is None or session.weather.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "WEATHER_NOT_FOUND",
                    "message": f"No weather data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        weather_data = session.weather
        
        # Filter by time if provided
        if time:
            try:
                from datetime import datetime
                time_dt = datetime.fromisoformat(time.replace('Z', '+00:00'))
                weather_data = weather_data[weather_data.index <= time_dt]
                if weather_data.empty:
                    raise HTTPException(
                        status_code=404,
                        detail={
                            "code": "WEATHER_NOT_FOUND",
                            "message": f"No weather data found at time {time}",
                            "details": {}
                        }
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "code": "INVALID_TIME_FORMAT",
                        "message": "Invalid time format. Use ISO 8601 format.",
                        "details": {"error": str(e)}
                    }
                )
        
        weather_list = dataframe_to_dict_list(weather_data)
        
        return ResponseWrapper(
            data=weather_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(weather_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "WEATHER_ERROR",
                "message": f"Could not retrieve weather data for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/weather/{year}/{event_name}/{session_type}/summary", response_model=ResponseWrapper)
def get_weather_summary(
    year: int,
    event_name: str,
    session_type: str
):
    """
    Get weather summary (min/max/average) for a session.
    """
    valid_types = ['FP1', 'FP2', 'FP3', 'Q', 'R', 'S', 'SQ']
    if session_type.upper() not in valid_types:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_SESSION_TYPE",
                "message": f"Invalid session type. Must be one of: {', '.join(valid_types)}",
                "details": {"provided": session_type}
            }
        )
    
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        if not hasattr(session, 'weather') or session.weather is None or session.weather.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "WEATHER_NOT_FOUND",
                    "message": f"No weather data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        weather_data = session.weather
        
        # Calculate summary statistics
        summary = {}
        numeric_cols = weather_data.select_dtypes(include=['float64', 'int64']).columns
        
        for col in numeric_cols:
            summary[col] = {
                "min": float(weather_data[col].min()) if not weather_data[col].isna().all() else None,
                "max": float(weather_data[col].max()) if not weather_data[col].isna().all() else None,
                "mean": float(weather_data[col].mean()) if not weather_data[col].isna().all() else None,
                "std": float(weather_data[col].std()) if not weather_data[col].isna().all() else None
            }
        
        return ResponseWrapper(
            data=summary,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper()
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "WEATHER_ERROR",
                "message": f"Could not retrieve weather summary for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

