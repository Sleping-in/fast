"""
Lap time endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import fastf1
import pandas as pd
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list, series_to_dict

router = APIRouter()


@router.get("/laps/{year}/{event_name}", response_model=ResponseWrapper)
async def get_laps(
    year: int,
    event_name: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ")
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
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ")
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
        
        # Get fastest lap - pick_fastest() returns a Series, convert to dict
        fastest_lap = laps.pick_fastest()
        
        if fastest_lap is None or (hasattr(fastest_lap, 'empty') and fastest_lap.empty):
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "FASTEST_LAP_NOT_FOUND",
                    "message": f"Fastest lap not found for {event_name} {year}",
                    "details": {}
                }
            )
        
        # Convert Series to dict - handle both Series and DataFrame
        try:
            if hasattr(fastest_lap, 'to_dict') and not hasattr(fastest_lap, 'columns'):
                # It's a Series
                fastest_lap_dict = series_to_dict(fastest_lap)
            else:
                # It's a DataFrame, convert to list and take first
                fastest_lap_list = dataframe_to_dict_list(fastest_lap)
                fastest_lap_dict = fastest_lap_list[0] if fastest_lap_list else {}
            
            # Ensure all values are JSON serializable
            import json
            json.dumps(fastest_lap_dict)  # Test serialization
            
            return ResponseWrapper(
                data=fastest_lap_dict,
                meta={
                    "year": year,
                    "event_name": event_name,
                    "session_type": session_type.upper()
                }
            )
        except Exception as serialization_error:
            # If serialization fails, return error with details
            raise HTTPException(
                status_code=500,
                detail={
                    "code": "SERIALIZATION_ERROR",
                    "message": f"Could not serialize fastest lap data",
                    "details": {"error": str(serialization_error)}
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


@router.get("/laps/{year}/{event_name}/{driver}", response_model=ResponseWrapper)
async def get_driver_laps(
    year: int,
    event_name: str,
    driver: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ")
):
    """
    Get lap times for a specific driver.
    Driver can be specified by abbreviation (e.g., 'VER', 'HAM') or driver number.
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
        
        # Try to filter by driver abbreviation first, then by driver number
        try:
            driver_num = int(driver)
            driver_laps = laps[laps['DriverNumber'] == driver_num]
        except ValueError:
            # Not a number, try abbreviation
            driver_laps = laps[laps['Driver'] == driver.upper()]
        
        if driver_laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "DRIVER_LAPS_NOT_FOUND",
                    "message": f"No lap data found for driver '{driver}' in {event_name} {year}",
                    "details": {}
                }
            )
        
        laps_list = dataframe_to_dict_list(driver_laps)
        
        return ResponseWrapper(
            data=laps_list,
            meta={
                "year": year,
                "event_name": event_name,
                "driver": driver,
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
                "message": f"Could not retrieve lap data for driver '{driver}' in {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

