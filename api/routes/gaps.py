"""
Gap analysis endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import fastf1
import pandas as pd
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list

router = APIRouter()


@router.get("/gaps/{year}/{event_name}/{session_type}", response_model=ResponseWrapper)
def get_gaps(
    year: int,
    event_name: str,
    session_type: str,
    lap: Optional[int] = Query(None, description="Specific lap number")
):
    """
    Get gap to leader for all drivers.
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
                    "code": "GAPS_NOT_FOUND",
                    "message": f"No lap data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        # Filter by lap if provided
        if lap:
            laps = laps[laps['LapNumber'] == lap]
            if laps.empty:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "code": "GAPS_NOT_FOUND",
                        "message": f"No data found for lap {lap}",
                        "details": {}
                    }
                )
        
        # Calculate gaps to leader
        gaps = []
        for driver in laps['DriverNumber'].unique():
            driver_laps = laps[laps['DriverNumber'] == driver]
            if driver_laps.empty:
                continue
            
            # Get leader's time (position 1)
            leader_laps = laps[laps['Position'] == 1]
            if leader_laps.empty:
                continue
            
            # Get same lap for comparison
            for _, driver_lap in driver_laps.iterrows():
                lap_num = driver_lap['LapNumber']
                leader_lap = leader_laps[leader_laps['LapNumber'] == lap_num]
                
                if not leader_lap.empty and pd.notna(driver_lap.get('LapTime')) and pd.notna(leader_lap.iloc[0].get('LapTime')):
                    gap = (driver_lap['LapTime'] - leader_lap.iloc[0]['LapTime']).total_seconds()
                    gaps.append({
                        "driver_number": int(driver),
                        "driver": driver_lap.get('Driver'),
                        "lap": int(lap_num),
                        "position": float(driver_lap.get('Position')) if pd.notna(driver_lap.get('Position')) else None,
                        "gap_to_leader_seconds": gap
                    })
        
        return ResponseWrapper(
            data=gaps,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(gaps)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "GAPS_ERROR",
                "message": f"Could not retrieve gaps for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/gaps/{year}/{event_name}/{session_type}/{driver}", response_model=ResponseWrapper)
def get_driver_gaps(
    year: int,
    event_name: str,
    session_type: str,
    driver: str
):
    """Get gap to leader for a specific driver."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "GAPS_NOT_FOUND",
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
        
        gaps = []
        for _, driver_lap in driver_laps.iterrows():
            lap_num = driver_lap['LapNumber']
            leader_laps = laps[(laps['Position'] == 1) & (laps['LapNumber'] == lap_num)]
            
            if not leader_laps.empty and pd.notna(driver_lap.get('LapTime')) and pd.notna(leader_laps.iloc[0].get('LapTime')):
                gap = (driver_lap['LapTime'] - leader_laps.iloc[0]['LapTime']).total_seconds()
                gaps.append({
                    "lap": int(lap_num),
                    "position": float(driver_lap.get('Position')) if pd.notna(driver_lap.get('Position')) else None,
                    "gap_to_leader_seconds": gap
                })
        
        return ResponseWrapper(
            data=gaps,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "driver": driver,
                "count": len(gaps)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "GAPS_ERROR",
                "message": f"Could not retrieve gaps for driver {driver}",
                "details": {"error": str(e)}
            }
        )


@router.get("/gaps/{year}/{event_name}/{session_type}/{driver}/ahead", response_model=ResponseWrapper)
def get_gap_to_driver_ahead(
    year: int,
    event_name: str,
    session_type: str,
    driver: str
):
    """Get gap to driver ahead."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "GAPS_NOT_FOUND",
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
        
        gaps = []
        for _, driver_lap in driver_laps.iterrows():
            lap_num = driver_lap['LapNumber']
            driver_pos = driver_lap.get('Position')
            
            if pd.notna(driver_pos) and driver_pos > 1:
                ahead_pos = driver_pos - 1
                ahead_laps = laps[(laps['Position'] == ahead_pos) & (laps['LapNumber'] == lap_num)]
                
                if not ahead_laps.empty and pd.notna(driver_lap.get('LapTime')) and pd.notna(ahead_laps.iloc[0].get('LapTime')):
                    gap = (driver_lap['LapTime'] - ahead_laps.iloc[0]['LapTime']).total_seconds()
                    gaps.append({
                        "lap": int(lap_num),
                        "position": float(driver_pos),
                        "gap_to_ahead_seconds": gap,
                        "driver_ahead": ahead_laps.iloc[0].get('Driver')
                    })
        
        return ResponseWrapper(
            data=gaps,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "driver": driver,
                "count": len(gaps)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "GAPS_ERROR",
                "message": f"Could not retrieve gap to driver ahead for {driver}",
                "details": {"error": str(e)}
            }
        )


@router.get("/gaps/{year}/{event_name}/{session_type}/{driver}/behind", response_model=ResponseWrapper)
def get_gap_to_driver_behind(
    year: int,
    event_name: str,
    session_type: str,
    driver: str
):
    """Get gap to driver behind."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "GAPS_NOT_FOUND",
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
        
        gaps = []
        for _, driver_lap in driver_laps.iterrows():
            lap_num = driver_lap['LapNumber']
            driver_pos = driver_lap.get('Position')
            
            if pd.notna(driver_pos):
                behind_pos = driver_pos + 1
                behind_laps = laps[(laps['Position'] == behind_pos) & (laps['LapNumber'] == lap_num)]
                
                if not behind_laps.empty and pd.notna(driver_lap.get('LapTime')) and pd.notna(behind_laps.iloc[0].get('LapTime')):
                    gap = (behind_laps.iloc[0]['LapTime'] - driver_lap['LapTime']).total_seconds()
                    gaps.append({
                        "lap": int(lap_num),
                        "position": float(driver_pos),
                        "gap_to_behind_seconds": gap,
                        "driver_behind": behind_laps.iloc[0].get('Driver')
                    })
        
        return ResponseWrapper(
            data=gaps,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "driver": driver,
                "count": len(gaps)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "GAPS_ERROR",
                "message": f"Could not retrieve gap to driver behind for {driver}",
                "details": {"error": str(e)}
            }
        )

