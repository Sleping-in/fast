"""
Driver information endpoints.
"""
from fastapi import APIRouter, HTTPException
import fastf1
import pandas as pd
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list

router = APIRouter()


@router.get("/drivers/{year}", response_model=ResponseWrapper)
def get_drivers(year: int):
    """
    Get list of all drivers for a specific year.
    """
    try:
        # Get a recent event to fetch driver list
        schedule = fastf1.get_event_schedule(year)
        
        if schedule.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "YEAR_NOT_FOUND",
                    "message": f"No events found for year {year}",
                    "details": {}
                }
            )
        
        # Get first event to fetch driver list
        first_event = schedule.iloc[0]
        event_name = first_event['EventName']
        
        session = fastf1.get_session(year, event_name, 'R')
        session.load()
        
        # Get unique drivers from results
        results = session.results
        
        if results is None or results.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "DRIVERS_NOT_FOUND",
                    "message": f"Could not retrieve driver list for year {year}",
                    "details": {}
                }
            )
        
        # Extract driver information
        drivers_list = []
        for _, row in results.iterrows():
            driver_info = {
                "driver_number": int(row.get("DriverNumber", 0)) if pd.notna(row.get("DriverNumber")) else None,
                "abbreviation": row.get("Abbreviation", ""),
                "full_name": row.get("FullName", ""),
                "team_name": row.get("TeamName", ""),
                "country_code": row.get("CountryCode", ""),
            }
            # Avoid duplicates
            if driver_info not in drivers_list:
                drivers_list.append(driver_info)
        
        return ResponseWrapper(
            data=drivers_list,
            meta={"year": year, "count": len(drivers_list)}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "DRIVERS_ERROR",
                "message": f"Could not retrieve drivers for year {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/drivers/{year}/{event_name}", response_model=ResponseWrapper)
def get_event_drivers(year: int, event_name: str):
    """
    Get list of drivers for a specific event.
    """
    try:
        session = fastf1.get_session(year, event_name, 'R')
        session.load()
        
        results = session.results
        
        if results is None or results.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "DRIVERS_NOT_FOUND",
                    "message": f"Could not retrieve drivers for {event_name} {year}",
                    "details": {}
                }
            )
        
        # Extract driver information
        drivers_list = []
        for _, row in results.iterrows():
            driver_info = {
                "driver_number": int(row.get("DriverNumber", 0)) if pd.notna(row.get("DriverNumber")) else None,
                "abbreviation": row.get("Abbreviation", ""),
                "full_name": row.get("FullName", ""),
                "team_name": row.get("TeamName", ""),
                "country_code": row.get("CountryCode", ""),
                "position": int(row.get("Position", 0)) if pd.notna(row.get("Position")) else None,
                "points": float(row.get("Points", 0)) if pd.notna(row.get("Points")) else None
            }
            drivers_list.append(driver_info)
        
        return ResponseWrapper(
            data=drivers_list,
            meta={
                "year": year,
                "event_name": event_name,
                "count": len(drivers_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "DRIVERS_ERROR",
                "message": f"Could not retrieve drivers for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

