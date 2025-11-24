"""
Tyre strategy endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
import fastf1
import pandas as pd
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list

router = APIRouter()


@router.get("/tyres/{year}/{event_name}/{session_type}/compounds", response_model=ResponseWrapper)
def get_tyre_compounds(
    year: int,
    event_name: str,
    session_type: str
):
    """
    Get list of tyre compounds used in the session.
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
        if laps is None or laps.empty or 'Compound' not in laps.columns:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TYRE_DATA_NOT_FOUND",
                    "message": f"No tyre data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        compounds = laps['Compound'].dropna().unique().tolist()
        
        return ResponseWrapper(
            data={"compounds": compounds},
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(compounds)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TYRE_ERROR",
                "message": f"Could not retrieve tyre compounds for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/tyres/{year}/{event_name}/{session_type}/strategy", response_model=ResponseWrapper)
def get_tyre_strategy(
    year: int,
    event_name: str,
    session_type: str
):
    """Get tyre strategy analysis for all drivers."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TYRE_DATA_NOT_FOUND",
                    "message": f"No lap data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        strategy = []
        for driver in laps['DriverNumber'].unique():
            driver_laps = laps[laps['DriverNumber'] == driver].sort_values('LapNumber')
            driver_name = driver_laps.iloc[0]['Driver'] if 'Driver' in driver_laps.columns else None
            
            if 'Stint' in driver_laps.columns and 'Compound' in driver_laps.columns:
                stints = []
                for stint_num in driver_laps['Stint'].dropna().unique():
                    stint_laps = driver_laps[driver_laps['Stint'] == stint_num]
                    if not stint_laps.empty:
                        stints.append({
                            "stint": int(stint_num),
                            "compound": stint_laps.iloc[0].get('Compound'),
                            "start_lap": int(stint_laps['LapNumber'].min()),
                            "end_lap": int(stint_laps['LapNumber'].max()),
                            "laps": int(len(stint_laps)),
                            "average_tyre_life": float(stint_laps['TyreLife'].mean()) if 'TyreLife' in stint_laps.columns and pd.notna(stint_laps['TyreLife']).any() else None
                        })
                
                strategy.append({
                    "driver_number": int(driver),
                    "driver": driver_name,
                    "total_stints": len(stints),
                    "stints": stints
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
                "code": "TYRE_ERROR",
                "message": f"Could not retrieve tyre strategy for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/tyres/{year}/{event_name}/{session_type}/{driver}/stints", response_model=ResponseWrapper)
def get_driver_stints(
    year: int,
    event_name: str,
    session_type: str,
    driver: str
):
    """Get stint information for a specific driver."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TYRE_DATA_NOT_FOUND",
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
        
        driver_laps = driver_laps.sort_values('LapNumber')
        stints = []
        
        if 'Stint' in driver_laps.columns and 'Compound' in driver_laps.columns:
            for stint_num in driver_laps['Stint'].dropna().unique():
                stint_laps = driver_laps[driver_laps['Stint'] == stint_num]
                if not stint_laps.empty:
                    stints.append({
                        "stint": int(stint_num),
                        "compound": stint_laps.iloc[0].get('Compound'),
                        "start_lap": int(stint_laps['LapNumber'].min()),
                        "end_lap": int(stint_laps['LapNumber'].max()),
                        "laps": int(len(stint_laps)),
                        "average_tyre_life": float(stint_laps['TyreLife'].mean()) if 'TyreLife' in stint_laps.columns and pd.notna(stint_laps['TyreLife']).any() else None
                    })
        
        return ResponseWrapper(
            data=stints,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "driver": driver,
                "count": len(stints)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TYRE_ERROR",
                "message": f"Could not retrieve stints for driver {driver}",
                "details": {"error": str(e)}
            }
        )


@router.get("/tyres/{year}/{event_name}/{session_type}/life-analysis", response_model=ResponseWrapper)
def get_tyre_life_analysis(
    year: int,
    event_name: str,
    session_type: str
):
    """Get tyre life vs performance analysis."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty or 'TyreLife' not in laps.columns:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TYRE_DATA_NOT_FOUND",
                    "message": f"No tyre life data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        analysis = []
        for driver in laps['DriverNumber'].unique():
            driver_laps = laps[laps['DriverNumber'] == driver]
            driver_name = driver_laps.iloc[0]['Driver'] if 'Driver' in driver_laps.columns else None
            
            if 'TyreLife' in driver_laps.columns and 'LapTime' in driver_laps.columns:
                valid_laps = driver_laps[pd.notna(driver_laps['TyreLife']) & pd.notna(driver_laps['LapTime'])]
                if not valid_laps.empty:
                    analysis.append({
                        "driver_number": int(driver),
                        "driver": driver_name,
                        "average_tyre_life": float(valid_laps['TyreLife'].mean()),
                        "average_lap_time": float(valid_laps['LapTime'].dt.total_seconds().mean()) if hasattr(valid_laps['LapTime'].iloc[0], 'total_seconds') else None,
                        "laps_analyzed": int(len(valid_laps))
                    })
        
        return ResponseWrapper(
            data=analysis,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(analysis)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TYRE_ERROR",
                "message": f"Could not retrieve tyre life analysis for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

