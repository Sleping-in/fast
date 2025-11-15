"""
Position data endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import fastf1
import pandas as pd
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list, datetime_to_iso8601

router = APIRouter()


@router.get("/positions/{year}/{event_name}/{session_type}", response_model=ResponseWrapper)
async def get_positions(
    year: int,
    event_name: str,
    session_type: str,
    time: Optional[str] = Query(None, description="Specific timestamp (ISO 8601 format)")
):
    """
    Get position data for all drivers in a session.
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
        
        if not hasattr(session, 'position_data') or session.position_data is None or session.position_data.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "POSITION_DATA_NOT_FOUND",
                    "message": f"No position data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        position_data = session.position_data
        
        # Filter by time if provided
        if time:
            try:
                from datetime import datetime
                time_dt = datetime.fromisoformat(time.replace('Z', '+00:00'))
                position_data = position_data[position_data.index <= time_dt]
                if position_data.empty:
                    raise HTTPException(
                        status_code=404,
                        detail={
                            "code": "POSITION_DATA_NOT_FOUND",
                            "message": f"No position data found at time {time}",
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
        
        positions_list = dataframe_to_dict_list(position_data)
        
        return ResponseWrapper(
            data=positions_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(positions_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "POSITION_DATA_ERROR",
                "message": f"Could not retrieve position data for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/positions/{year}/{event_name}/{session_type}/{driver}", response_model=ResponseWrapper)
async def get_driver_positions(
    year: int,
    event_name: str,
    session_type: str,
    driver: str
):
    """Get position data for a specific driver."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        if not hasattr(session, 'position_data') or session.position_data is None or session.position_data.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "POSITION_DATA_NOT_FOUND",
                    "message": f"No position data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        position_data = session.position_data
        
        # Try to filter by driver number or abbreviation
        try:
            driver_num = int(driver)
            if driver_num in position_data.columns:
                driver_positions = position_data[[driver_num]]
            else:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "code": "DRIVER_NOT_FOUND",
                        "message": f"Driver {driver} not found in position data",
                        "details": {}
                    }
                )
        except ValueError:
            # Not a number, need to get driver number from results
            results = session.results
            driver_row = results[results['Abbreviation'] == driver.upper()]
            if driver_row.empty:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "code": "DRIVER_NOT_FOUND",
                        "message": f"Driver {driver} not found",
                        "details": {}
                    }
                )
            driver_num = int(driver_row.iloc[0]['DriverNumber'])
            if driver_num in position_data.columns:
                driver_positions = position_data[[driver_num]]
            else:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "code": "DRIVER_NOT_FOUND",
                        "message": f"Driver {driver} not found in position data",
                        "details": {}
                    }
                )
        
        positions_list = dataframe_to_dict_list(driver_positions)
        
        return ResponseWrapper(
            data=positions_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "driver": driver,
                "count": len(positions_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "POSITION_DATA_ERROR",
                "message": f"Could not retrieve position data for driver {driver}",
                "details": {"error": str(e)}
            }
        )


@router.get("/positions/{year}/{event_name}/{session_type}/changes", response_model=ResponseWrapper)
async def get_position_changes(
    year: int,
    event_name: str,
    session_type: str
):
    """Get all position changes during the session."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        # Use laps data to get position changes
        laps = session.laps
        if laps is None or laps.empty or 'Position' not in laps.columns:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "POSITION_CHANGES_NOT_FOUND",
                    "message": f"No position data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        # Get position changes by comparing consecutive laps
        changes = []
        for driver in laps['DriverNumber'].unique():
            driver_laps = laps[laps['DriverNumber'] == driver].sort_values('LapNumber')
            for i in range(1, len(driver_laps)):
                prev_pos = driver_laps.iloc[i-1]['Position']
                curr_pos = driver_laps.iloc[i]['Position']
                if pd.notna(prev_pos) and pd.notna(curr_pos) and prev_pos != curr_pos:
                    changes.append({
                        "driver_number": int(driver),
                        "driver": driver_laps.iloc[i]['Driver'],
                        "lap": int(driver_laps.iloc[i]['LapNumber']),
                        "previous_position": float(prev_pos),
                        "current_position": float(curr_pos),
                        "change": float(prev_pos - curr_pos)  # Positive = gained positions
                    })
        
        return ResponseWrapper(
            data=changes,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(changes)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "POSITION_CHANGES_ERROR",
                "message": f"Could not retrieve position changes for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/positions/{year}/{event_name}/{session_type}/overtakes", response_model=ResponseWrapper)
async def get_overtakes(
    year: int,
    event_name: str,
    session_type: str
):
    """Get all overtakes (position gains)."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty or 'Position' not in laps.columns:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "OVERTAKES_NOT_FOUND",
                    "message": f"No position data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        # Get overtakes (position gains)
        overtakes = []
        for driver in laps['DriverNumber'].unique():
            driver_laps = laps[laps['DriverNumber'] == driver].sort_values('LapNumber')
            for i in range(1, len(driver_laps)):
                prev_pos = driver_laps.iloc[i-1]['Position']
                curr_pos = driver_laps.iloc[i]['Position']
                if pd.notna(prev_pos) and pd.notna(curr_pos) and prev_pos > curr_pos:  # Gained position
                    overtakes.append({
                        "driver_number": int(driver),
                        "driver": driver_laps.iloc[i]['Driver'],
                        "lap": int(driver_laps.iloc[i]['LapNumber']),
                        "previous_position": float(prev_pos),
                        "current_position": float(curr_pos),
                        "positions_gained": float(prev_pos - curr_pos)
                    })
        
        return ResponseWrapper(
            data=overtakes,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(overtakes)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "OVERTAKES_ERROR",
                "message": f"Could not retrieve overtakes for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

