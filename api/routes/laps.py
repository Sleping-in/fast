"""
Lap time endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import fastf1
import pandas as pd
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list

router = APIRouter()


@router.get("/laps/{year}/{event_name}", response_model=ResponseWrapper)
async def get_laps(
    year: int,
    event_name: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S")
):
    """
    Get all lap times for a race session.
    """
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "LAPS_NOT_FOUND",
                    "message": f"No lap data found for {event_name} {year}",
                    "details": {}
                }
            )
        
        laps_list = dataframe_to_dict_list(laps)
        
        return ResponseWrapper(
            data=laps_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(laps_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "LAPS_ERROR",
                "message": f"Could not retrieve lap data for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/laps/{year}/{event_name}/fastest", response_model=ResponseWrapper)
async def get_fastest_lap(
    year: int,
    event_name: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S")
):
    """
    Get fastest lap information for a session.
    """
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "LAPS_NOT_FOUND",
                    "message": f"No lap data found for {event_name} {year}",
                    "details": {}
                }
            )
        
        # Get fastest lap
        fastest_lap = laps.pick_fastest()
        
        if fastest_lap is None or fastest_lap.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "FASTEST_LAP_NOT_FOUND",
                    "message": f"Fastest lap not found for {event_name} {year}",
                    "details": {}
                }
            )
        
        fastest_lap_dict = dataframe_to_dict_list(fastest_lap)
        
        return ResponseWrapper(
            data=fastest_lap_dict[0] if fastest_lap_dict else {},
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
                "code": "FASTEST_LAP_ERROR",
                "message": f"Could not retrieve fastest lap for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

