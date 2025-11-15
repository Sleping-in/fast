"""
Pit stop endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import fastf1
import pandas as pd
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list, datetime_to_iso8601

router = APIRouter()


@router.get("/pit-stops/{year}/{event_name}/{session_type}", response_model=ResponseWrapper)
async def get_pit_stops(
    year: int,
    event_name: str,
    session_type: str,
    include_duration: bool = Query(False, description="Include pit stop duration")
):
    """
    Get all pit stops for a session.
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
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "PIT_STOPS_NOT_FOUND",
                    "message": f"No lap data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        # Filter laps with pit stops
        pit_stops = laps[pd.notna(laps['PitInTime']) | pd.notna(laps['PitOutTime'])].copy()
        
        if pit_stops.empty:
            return ResponseWrapper(
                data=[],
                meta={
                    "year": year,
                    "event_name": event_name,
                    "session_type": session_type.upper(),
                    "count": 0
                }
            )
        
        # Calculate duration if requested
        if include_duration and 'PitInTime' in pit_stops.columns and 'PitOutTime' in pit_stops.columns:
            pit_stops['PitDuration'] = (pit_stops['PitOutTime'] - pit_stops['PitInTime']).dt.total_seconds()
        
        pit_stops_list = dataframe_to_dict_list(pit_stops)
        
        return ResponseWrapper(
            data=pit_stops_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(pit_stops_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "PIT_STOPS_ERROR",
                "message": f"Could not retrieve pit stops for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/pit-stops/{year}/{event_name}/{session_type}/{driver}", response_model=ResponseWrapper)
async def get_driver_pit_stops(
    year: int,
    event_name: str,
    session_type: str,
    driver: str,
    include_duration: bool = Query(False, description="Include pit stop duration")
):
    """Get pit stops for a specific driver."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "PIT_STOPS_NOT_FOUND",
                    "message": f"No lap data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        # Filter by driver
        try:
            driver_num = int(driver)
            driver_laps = laps[laps['DriverNumber'] == driver_num]
        except ValueError:
            driver_laps = laps[laps['Driver'] == driver.upper()]
        
        if driver_laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "DRIVER_NOT_FOUND",
                    "message": f"Driver {driver} not found",
                    "details": {}
                }
            )
        
        # Filter laps with pit stops
        pit_stops = driver_laps[pd.notna(driver_laps['PitInTime']) | pd.notna(driver_laps['PitOutTime'])].copy()
        
        if pit_stops.empty:
            return ResponseWrapper(
                data=[],
                meta={
                    "year": year,
                    "event_name": event_name,
                    "session_type": session_type.upper(),
                    "driver": driver,
                    "count": 0
                }
            )
        
        # Calculate duration if requested
        if include_duration and 'PitInTime' in pit_stops.columns and 'PitOutTime' in pit_stops.columns:
            pit_stops['PitDuration'] = (pit_stops['PitOutTime'] - pit_stops['PitInTime']).dt.total_seconds()
        
        pit_stops_list = dataframe_to_dict_list(pit_stops)
        
        return ResponseWrapper(
            data=pit_stops_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "driver": driver,
                "count": len(pit_stops_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "PIT_STOPS_ERROR",
                "message": f"Could not retrieve pit stops for driver {driver}",
                "details": {"error": str(e)}
            }
        )


@router.get("/pit-stops/{year}/{event_name}/{session_type}/fastest", response_model=ResponseWrapper)
async def get_fastest_pit_stop(
    year: int,
    event_name: str,
    session_type: str
):
    """Get the fastest pit stop in the session."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "PIT_STOPS_NOT_FOUND",
                    "message": f"No lap data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        # Filter laps with pit stops
        pit_stops = laps[pd.notna(laps['PitInTime']) & pd.notna(laps['PitOutTime'])].copy()
        
        if pit_stops.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "PIT_STOPS_NOT_FOUND",
                    "message": f"No pit stops found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        # Calculate duration
        pit_stops['PitDuration'] = (pit_stops['PitOutTime'] - pit_stops['PitInTime']).dt.total_seconds()
        
        # Find fastest
        fastest = pit_stops.loc[pit_stops['PitDuration'].idxmin()]
        fastest_dict = fastest.to_dict()
        
        # Convert to serializable format
        from utils.serialization import series_to_dict
        fastest_data = series_to_dict(fastest)
        
        return ResponseWrapper(
            data=fastest_data,
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
                "code": "PIT_STOPS_ERROR",
                "message": f"Could not retrieve fastest pit stop for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/pit-stops/{year}/{event_name}/{session_type}/strategy", response_model=ResponseWrapper)
async def get_pit_stop_strategy(
    year: int,
    event_name: str,
    session_type: str
):
    """Get pit stop strategy analysis."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "PIT_STOPS_NOT_FOUND",
                    "message": f"No lap data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        strategy = []
        for driver in laps['DriverNumber'].unique():
            driver_laps = laps[laps['DriverNumber'] == driver].sort_values('LapNumber')
            driver_name = driver_laps.iloc[0]['Driver'] if 'Driver' in driver_laps.columns else None
            
            pit_laps = driver_laps[pd.notna(driver_laps['PitInTime'])].copy()
            
            if not pit_laps.empty:
                pit_stops = []
                for _, pit_lap in pit_laps.iterrows():
                    pit_stops.append({
                        "lap": int(pit_lap['LapNumber']),
                        "pit_in_time": datetime_to_iso8601(pit_lap.get('PitInTime')),
                        "pit_out_time": datetime_to_iso8601(pit_lap.get('PitOutTime')),
                        "compound_before": pit_lap.get('Compound'),
                        "compound_after": driver_laps[driver_laps['LapNumber'] > pit_lap['LapNumber']].iloc[0].get('Compound') if len(driver_laps[driver_laps['LapNumber'] > pit_lap['LapNumber']]) > 0 else None
                    })
                
                strategy.append({
                    "driver_number": int(driver),
                    "driver": driver_name,
                    "total_pit_stops": len(pit_stops),
                    "pit_stops": pit_stops
                })
        
        return ResponseWrapper(
            data=strategy,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(strategy)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "PIT_STOPS_ERROR",
                "message": f"Could not retrieve pit stop strategy for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

