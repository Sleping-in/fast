"""
Sector times endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
import fastf1
import pandas as pd
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list, series_to_dict

router = APIRouter()


@router.get("/sectors/{year}/{event_name}/{session_type}", response_model=ResponseWrapper)
def get_sectors(
    year: int,
    event_name: str,
    session_type: str
):
    """
    Get all sector times for a session.
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
                    "code": "SECTORS_NOT_FOUND",
                    "message": f"No lap data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        # Filter for sectors
        sector_cols = ['Sector1Time', 'Sector2Time', 'Sector3Time']
        available_cols = [col for col in sector_cols if col in laps.columns]
        
        if not available_cols:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "SECTORS_NOT_FOUND",
                    "message": f"No sector time data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        sectors_list = dataframe_to_dict_list(laps[['DriverNumber', 'Driver', 'LapNumber'] + available_cols])
        
        return ResponseWrapper(
            data=sectors_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(sectors_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "SECTORS_ERROR",
                "message": f"Could not retrieve sector times for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/sectors/{year}/{event_name}/fastest/sector1", response_model=ResponseWrapper)
def get_fastest_sector1(
    year: int,
    event_name: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ")
):
    """Get fastest sector 1 time."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty or 'Sector1Time' not in laps.columns:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "SECTORS_NOT_FOUND",
                    "message": f"No sector 1 data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        # Filter out invalid times
        valid_sectors = laps[pd.notna(laps['Sector1Time'])]
        if valid_sectors.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "SECTORS_NOT_FOUND",
                    "message": f"No valid sector 1 times found",
                    "details": {}
                }
            )
        
        fastest = valid_sectors.loc[valid_sectors['Sector1Time'].idxmin()]
        fastest_dict = series_to_dict(fastest)
        
        return ResponseWrapper(
            data=fastest_dict,
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
                "code": "SECTORS_ERROR",
                "message": f"Could not retrieve fastest sector 1 for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/sectors/{year}/{event_name}/fastest/sector2", response_model=ResponseWrapper)
def get_fastest_sector2(
    year: int,
    event_name: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ")
):
    """Get fastest sector 2 time."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty or 'Sector2Time' not in laps.columns:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "SECTORS_NOT_FOUND",
                    "message": f"No sector 2 data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        valid_sectors = laps[pd.notna(laps['Sector2Time'])]
        if valid_sectors.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "SECTORS_NOT_FOUND",
                    "message": f"No valid sector 2 times found",
                    "details": {}
                }
            )
        
        fastest = valid_sectors.loc[valid_sectors['Sector2Time'].idxmin()]
        fastest_dict = series_to_dict(fastest)
        
        return ResponseWrapper(
            data=fastest_dict,
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
                "code": "SECTORS_ERROR",
                "message": f"Could not retrieve fastest sector 2 for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/sectors/{year}/{event_name}/fastest/sector3", response_model=ResponseWrapper)
def get_fastest_sector3(
    year: int,
    event_name: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ")
):
    """Get fastest sector 3 time."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty or 'Sector3Time' not in laps.columns:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "SECTORS_NOT_FOUND",
                    "message": f"No sector 3 data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        valid_sectors = laps[pd.notna(laps['Sector3Time'])]
        if valid_sectors.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "SECTORS_NOT_FOUND",
                    "message": f"No valid sector 3 times found",
                    "details": {}
                }
            )
        
        fastest = valid_sectors.loc[valid_sectors['Sector3Time'].idxmin()]
        fastest_dict = series_to_dict(fastest)
        
        return ResponseWrapper(
            data=fastest_dict,
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
                "code": "SECTORS_ERROR",
                "message": f"Could not retrieve fastest sector 3 for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/sectors/{year}/{event_name}/{session_type}/{driver}", response_model=ResponseWrapper)
def get_driver_sectors(
    year: int,
    event_name: str,
    session_type: str,
    driver: str
):
    """Get sector times for a specific driver."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "SECTORS_NOT_FOUND",
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
        
        sector_cols = ['Sector1Time', 'Sector2Time', 'Sector3Time']
        available_cols = [col for col in sector_cols if col in driver_laps.columns]
        
        sectors_list = dataframe_to_dict_list(driver_laps[['LapNumber'] + available_cols])
        
        return ResponseWrapper(
            data=sectors_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "driver": driver,
                "count": len(sectors_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "SECTORS_ERROR",
                "message": f"Could not retrieve sector times for driver {driver}",
                "details": {"error": str(e)}
            }
        )

