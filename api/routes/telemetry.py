"""
Telemetry data endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import fastf1
import pandas as pd
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list

router = APIRouter()


@router.get("/telemetry/{year}/{event_name}/{driver}", response_model=ResponseWrapper)
def get_driver_telemetry(
    year: int,
    event_name: str,
    driver: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ"),
    lap: Optional[int] = Query(None, description="Specific lap number (optional)")
):
    """
    Get telemetry data for a specific driver.
    Driver can be specified by abbreviation (e.g., 'VER', 'HAM') or driver number.
    Optionally filter by lap number.
    """
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        # Get driver's laps to identify driver number
        laps = session.laps
        
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "SESSION_DATA_NOT_FOUND",
                    "message": f"No session data found for {event_name} {year}",
                    "details": {}
                }
            )
        
        # Find driver number
        try:
            driver_num = int(driver)
        except ValueError:
            # Not a number, try abbreviation
            driver_laps = laps[laps['Driver'] == driver.upper()]
            if driver_laps.empty:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "code": "DRIVER_NOT_FOUND",
                        "message": f"Driver '{driver}' not found in {event_name} {year}",
                        "details": {}
                    }
                )
            driver_num = driver_laps.iloc[0]['DriverNumber']
        
        # Get telemetry
        if lap is not None:
            # Get specific lap
            lap_data = laps[(laps['DriverNumber'] == driver_num) & (laps['LapNumber'] == lap)]
            if lap_data.empty:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "code": "LAP_NOT_FOUND",
                        "message": f"Lap {lap} not found for driver {driver} in {event_name} {year}",
                        "details": {}
                    }
                )
            telemetry = session.laps.pick_drivers(driver_num).pick_lap(lap).get_telemetry()
        else:
            # Get all telemetry for driver
            telemetry = session.laps.pick_drivers(driver_num).get_telemetry()
        
        if telemetry is None or telemetry.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TELEMETRY_NOT_FOUND",
                    "message": f"No telemetry data found for driver '{driver}' in {event_name} {year}",
                    "details": {}
                }
            )
        
        telemetry_list = dataframe_to_dict_list(telemetry)
        
        return ResponseWrapper(
            data=telemetry_list,
            meta={
                "year": year,
                "event_name": event_name,
                "driver": driver,
                "driver_number": int(driver_num),
                "session_type": session_type.upper(),
                "lap": lap,
                "count": len(telemetry_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TELEMETRY_ERROR",
                "message": f"Could not retrieve telemetry for driver '{driver}' in {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/car-data/{year}/{event_name}/{driver}", response_model=ResponseWrapper)
def get_car_data(
    year: int,
    event_name: str,
    driver: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ")
):
    """
    Get car data (speed, throttle, brake, DRS, gear, etc.) for a specific driver.
    """
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        # Get driver's laps to identify driver number
        laps = session.laps
        
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "SESSION_DATA_NOT_FOUND",
                    "message": f"No session data found for {event_name} {year}",
                    "details": {}
                }
            )
        
        # Find driver number
        try:
            driver_num = int(driver)
        except ValueError:
            # Not a number, try abbreviation
            driver_laps = laps[laps['Driver'] == driver.upper()]
            if driver_laps.empty:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "code": "DRIVER_NOT_FOUND",
                        "message": f"Driver '{driver}' not found in {event_name} {year}",
                        "details": {}
                    }
                )
            driver_num = driver_laps.iloc[0]['DriverNumber']
        
        # Get car data
        car_data = session.laps.pick_drivers(driver_num).get_car_data()
        
        if car_data is None or car_data.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "CAR_DATA_NOT_FOUND",
                    "message": f"No car data found for driver '{driver}' in {event_name} {year}",
                    "details": {}
                }
            )
        
        car_data_list = dataframe_to_dict_list(car_data)
        
        return ResponseWrapper(
            data=car_data_list,
            meta={
                "year": year,
                "event_name": event_name,
                "driver": driver,
                "driver_number": int(driver_num),
                "session_type": session_type.upper(),
                "count": len(car_data_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "CAR_DATA_ERROR",
                "message": f"Could not retrieve car data for driver '{driver}' in {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/telemetry/{year}/{event_name}/{driver}/drs", response_model=ResponseWrapper)
def get_drs_data(
    year: int,
    event_name: str,
    driver: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ"),
    lap: Optional[int] = Query(None, description="Specific lap number (optional)")
):
    """
    Get DRS activation data for a specific driver.
    """
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(status_code=404, detail={"code": "SESSION_DATA_NOT_FOUND", "message": "No session data found"})
            
        # Find driver number
        try:
            driver_num = int(driver)
        except ValueError:
            driver_laps = laps[laps['Driver'] == driver.upper()]
            if driver_laps.empty:
                raise HTTPException(status_code=404, detail={"code": "DRIVER_NOT_FOUND", "message": f"Driver {driver} not found"})
            driver_num = driver_laps.iloc[0]['DriverNumber']
            
        # Get telemetry
        if lap:
            lap_data = laps[(laps['DriverNumber'] == driver_num) & (laps['LapNumber'] == lap)]
            if lap_data.empty:
                raise HTTPException(status_code=404, detail={"code": "LAP_NOT_FOUND", "message": f"Lap {lap} not found"})
            telemetry = session.laps.pick_drivers(driver_num).pick_lap(lap).get_telemetry()
        else:
            telemetry = session.laps.pick_drivers(driver_num).get_telemetry()
            
        if telemetry is None or telemetry.empty or 'DRS' not in telemetry.columns:
             raise HTTPException(status_code=404, detail={"code": "TELEMETRY_NOT_FOUND", "message": "No DRS data found"})
             
        # Filter for DRS data (Time, Distance, DRS)
        drs_data = telemetry[['Date', 'Time', 'Distance', 'DRS']].copy()
        
        # Convert to list
        drs_list = dataframe_to_dict_list(drs_data)
        
        return ResponseWrapper(
            data=drs_list,
            meta={
                "year": year,
                "event_name": event_name,
                "driver": driver,
                "session_type": session_type.upper(),
                "lap": lap,
                "count": len(drs_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TELEMETRY_ERROR",
                "message": f"Could not retrieve DRS data for driver {driver}",
                "details": {"error": str(e)}
            }
        )


@router.get("/telemetry/{year}/{event_name}/{driver}/speed", response_model=ResponseWrapper)
def get_speed_data(
    year: int,
    event_name: str,
    driver: str,
    session_type: str = Query("R", description="Session type: FP1, FP2, FP3, Q, R, S, SQ"),
    lap: Optional[int] = Query(None, description="Specific lap number (optional)")
):
    """
    Get speed data for a specific driver.
    """
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(status_code=404, detail={"code": "SESSION_DATA_NOT_FOUND", "message": "No session data found"})
            
        # Find driver number
        try:
            driver_num = int(driver)
        except ValueError:
            driver_laps = laps[laps['Driver'] == driver.upper()]
            if driver_laps.empty:
                raise HTTPException(status_code=404, detail={"code": "DRIVER_NOT_FOUND", "message": f"Driver {driver} not found"})
            driver_num = driver_laps.iloc[0]['DriverNumber']
            
        # Get telemetry
        if lap:
            lap_data = laps[(laps['DriverNumber'] == driver_num) & (laps['LapNumber'] == lap)]
            if lap_data.empty:
                raise HTTPException(status_code=404, detail={"code": "LAP_NOT_FOUND", "message": f"Lap {lap} not found"})
            telemetry = session.laps.pick_drivers(driver_num).pick_lap(lap).get_telemetry()
        else:
            telemetry = session.laps.pick_drivers(driver_num).get_telemetry()
            
        if telemetry is None or telemetry.empty or 'Speed' not in telemetry.columns:
             raise HTTPException(status_code=404, detail={"code": "TELEMETRY_NOT_FOUND", "message": "No speed data found"})
             
        # Filter for Speed data
        speed_data = telemetry[['Date', 'Time', 'Distance', 'Speed']].copy()
        
        # Convert to list
        speed_list = dataframe_to_dict_list(speed_data)
        
        return ResponseWrapper(
            data=speed_list,
            meta={
                "year": year,
                "event_name": event_name,
                "driver": driver,
                "session_type": session_type.upper(),
                "lap": lap,
                "count": len(speed_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TELEMETRY_ERROR",
                "message": f"Could not retrieve speed data for driver {driver}",
                "details": {"error": str(e)}
            }
        )


@router.get("/telemetry/{year}/{event_name}/{session_type}/channels", response_model=ResponseWrapper)
def get_telemetry_channels(
    year: int,
    event_name: str,
    session_type: str
):
    """
    Get available telemetry channels for a session.
    """
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load(telemetry=True)
        
        laps = session.laps
        if laps is None or laps.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TELEMETRY_NOT_FOUND",
                    "message": f"No telemetry data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        # Get telemetry for the first lap of the winner (or first driver) to check columns
        try:
            first_lap = laps.pick_fastest()
            telemetry = first_lap.get_telemetry()
            channels = list(telemetry.columns)
        except:
            # Fallback
            channels = ['Speed', 'RPM', 'Gear', 'Throttle', 'Brake', 'DRS', 'Date', 'Time', 'SessionTime', 'Distance', 'RelativeDistance', 'X', 'Y', 'Z']
        
        return ResponseWrapper(
            data=channels,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(channels)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TELEMETRY_ERROR",
                "message": f"Could not retrieve telemetry channels for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

