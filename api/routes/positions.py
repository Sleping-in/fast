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


@router.get("/positions/{year}/{event_name}/{session_type}/changes", response_model=ResponseWrapper)
def get_position_changes(
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
def get_overtakes(
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


@router.get("/positions/{year}/{event_name}/{session_type}/lap-by-lap", response_model=ResponseWrapper)
def get_lap_positions(
    year: int,
    event_name: str,
    session_type: str
):
    """
    Get position of each driver at the end of each lap.
    """
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty or 'Position' not in laps.columns:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "POSITIONS_NOT_FOUND",
                    "message": f"No position data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        # Select relevant columns
        pos_data = laps[['Driver', 'DriverNumber', 'LapNumber', 'Position']].copy()
        
        # Sort by LapNumber and Position
        pos_data = pos_data.sort_values(['LapNumber', 'Position'])
        
        # Convert to list of dicts
        pos_list = dataframe_to_dict_list(pos_data)
        
        return ResponseWrapper(
            data=pos_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(pos_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "POSITIONS_ERROR",
                "message": f"Could not retrieve lap positions for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/positions/{year}/{event_name}/{session_type}", response_model=ResponseWrapper)
def get_positions(
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
        session.load(telemetry=True)
        
        if not hasattr(session, 'pos_data') or session.pos_data is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "POSITION_DATA_NOT_FOUND",
                    "message": f"No position data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        pos_data = session.pos_data
        result_data = {}
        
        # Filter by time if provided
        for driver_num, driver_pos in pos_data.items():
            if time:
                try:
                    from datetime import datetime
                    time_dt = datetime.fromisoformat(time.replace('Z', '+00:00'))
                    driver_pos = driver_pos[driver_pos['Date'] <= time_dt]
                except Exception:
                    pass # Ignore time filter errors for now or handle better
            
            if not driver_pos.empty:
                result_data[driver_num] = dataframe_to_dict_list(driver_pos)
        
        if not result_data:
             raise HTTPException(
                status_code=404,
                detail={
                    "code": "POSITION_DATA_NOT_FOUND",
                    "message": f"No position data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )

        return ResponseWrapper(
            data=result_data,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": sum(len(v) for v in result_data.values())
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
def get_driver_positions(
    year: int,
    event_name: str,
    session_type: str,
    driver: str
):
    """Get position data for a specific driver."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load(telemetry=True)
        
        if not hasattr(session, 'pos_data') or session.pos_data is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "POSITION_DATA_NOT_FOUND",
                    "message": f"No position data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        pos_data = session.pos_data
        driver_positions = None
        
        # Try to find driver in pos_data keys
        if driver in pos_data:
            driver_positions = pos_data[driver]
        else:
            # Try to resolve driver abbreviation to number
            try:
                # Check if driver is an abbreviation
                results = session.results
                driver_row = results[results['Abbreviation'] == driver.upper()]
                if not driver_row.empty:
                    driver_num = str(driver_row.iloc[0]['DriverNumber'])
                    if driver_num in pos_data:
                        driver_positions = pos_data[driver_num]
            except Exception:
                pass
        
        if driver_positions is None or driver_positions.empty:
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


