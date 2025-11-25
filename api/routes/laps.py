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


@router.get("/laps/{year}/{event_name}/fastest", response_model=ResponseWrapper)
def get_fastest_lap(
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


@router.get("/laps/{year}/{event_name}/personal-best", response_model=ResponseWrapper)
def get_personal_best_laps(
    year: int,
    event_name: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ")
):
    """Get personal best laps for all drivers."""
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
        
        # Filter for personal best laps
        if 'IsPersonalBest' in laps.columns:
            personal_bests = laps[laps['IsPersonalBest'] == True]
        else:
            # Fallback: find fastest lap per driver
            personal_bests = laps.groupby('DriverNumber').apply(
                lambda x: x.loc[x['LapTime'].idxmin()] 
                if 'LapTime' in x.columns and pd.notna(x['LapTime']).any() 
                else x.iloc[0]
            )
            personal_bests = personal_bests.reset_index(drop=True)
        
        if personal_bests.empty:
            return ResponseWrapper(
                data=[],
                meta={
                    "year": year,
                    "event_name": event_name,
                    "session_type": session_type.upper(),
                    "count": 0
                }
            )
        
        personal_bests_list = dataframe_to_dict_list(personal_bests)
        
        return ResponseWrapper(
            data=personal_bests_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(personal_bests_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "LAPS_ERROR",
                "message": f"Could not retrieve personal best laps for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/laps/{year}/{event_name}/speed-traps", response_model=ResponseWrapper)
def get_speed_traps(
    year: int,
    event_name: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ"),
    driver: Optional[str] = Query(None, description="Filter by driver")
):
    """
    Get speed trap data (SpeedST, SpeedFL, SpeedI1, SpeedI2) for all laps.
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
        
        if driver:
            try:
                driver_num = int(driver)
                laps = laps[laps['DriverNumber'] == driver_num]
            except ValueError:
                laps = laps[laps['Driver'] == driver.upper()]
            
            if laps.empty:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "code": "DRIVER_LAPS_NOT_FOUND",
                        "message": f"No lap data found for driver '{driver}'",
                        "details": {}
                    }
                )
        
        # Select speed columns
        speed_cols = ['Driver', 'LapNumber', 'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST']
        available_cols = [col for col in speed_cols if col in laps.columns]
        
        speed_data = laps[available_cols].copy()
        
        # Convert to list of dicts
        speed_list = dataframe_to_dict_list(speed_data)
        
        return ResponseWrapper(
            data=speed_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "driver": driver,
                "count": len(speed_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "SPEED_TRAPS_ERROR",
                "message": f"Could not retrieve speed trap data for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/laps/{year}/{event_name}", response_model=ResponseWrapper)
def get_laps(
    year: int,
    event_name: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ"),
    quicklaps: bool = Query(False, description="Filter quick laps only (exclude in/out laps)"),
    compound: Optional[str] = Query(None, description="Filter by tyre compound (SOFT, MEDIUM, HARD, etc.)"),
    exclude_pits: bool = Query(False, description="Exclude pit in/out laps"),
    track_status: Optional[int] = Query(None, description="Filter by track status (1=clear, 2=yellow, etc.)"),
    include_deleted: bool = Query(False, description="Include deleted/invalid laps")
):
    """
    Get all lap times for a race session with optional filtering.
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
        
        # Apply filters
        if quicklaps:
            try:
                laps = laps.pick_quicklaps()
            except:
                pass  # If method not available, skip filter
        
        if compound:
            try:
                laps = laps.pick_tyre(compound.upper())
            except:
                # Fallback to manual filtering
                if 'Compound' in laps.columns:
                    laps = laps[laps['Compound'] == compound.upper()]
        
        if exclude_pits:
            try:
                laps = laps.pick_wo_box()
            except:
                # Fallback to manual filtering
                if 'PitInTime' in laps.columns and 'PitOutTime' in laps.columns:
                    laps = laps[pd.isna(laps['PitInTime']) & pd.isna(laps['PitOutTime'])]
        
        if track_status is not None:
            try:
                laps = laps.pick_track_status(track_status)
            except:
                # Fallback to manual filtering
                if 'TrackStatus' in laps.columns:
                    laps = laps[laps['TrackStatus'] == track_status]
        
        if not include_deleted and 'Deleted' in laps.columns:
            laps = laps[laps['Deleted'] != True]
        
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


@router.get("/laps/{year}/{event_name}/{driver}", response_model=ResponseWrapper)
def get_driver_laps(
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


