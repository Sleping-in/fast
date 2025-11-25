"""
Ergast API integration endpoints for historical data.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import pandas as pd
from fastf1.ergast import Ergast
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list

router = APIRouter()
ergast = Ergast()

@router.get("/historical/{year}/events", response_model=ResponseWrapper)
def get_historical_events(year: int):
    """
    Get historical events (races) for a specific year using Ergast API.
    """
    try:
        schedule = ergast.get_race_schedule(season=year)
        
        if schedule is None or schedule.empty:
             raise HTTPException(
                status_code=404,
                detail={
                    "code": "EVENTS_NOT_FOUND",
                    "message": f"No historical events found for year {year}",
                    "details": {}
                }
            )
            
        events_list = dataframe_to_dict_list(schedule)
        
        return ResponseWrapper(
            data=events_list,
            meta={
                "year": year,
                "count": len(events_list),
                "source": "Ergast API"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ERGAST_ERROR",
                "message": f"Error retrieving historical events for {year}",
                "details": {"error": str(e)}
            }
        )

@router.get("/historical/{year}/results", response_model=ResponseWrapper)
def get_historical_results(
    year: int, 
    round: Optional[int] = Query(None, description="Round number"),
    driver: Optional[str] = Query(None, description="Driver ID")
):
    """
    Get historical race results for a specific year using Ergast API.
    """
    try:
        results = ergast.get_race_results(season=year, round=round, driver=driver)
        
        if results is None or results.content is None or (hasattr(results.content, 'empty') and results.content.empty):
             raise HTTPException(
                status_code=404,
                detail={
                    "code": "RESULTS_NOT_FOUND",
                    "message": f"No historical results found for year {year}",
                    "details": {"round": round, "driver": driver}
                }
            )
        
        # Ergast response content is usually a list of Race objects or a DataFrame depending on the call
        # fastf1.ergast.Ergast.get_race_results returns an ErgastResponse
        # The content property holds the data
        
        data = results.content
        results_list = []
        
        if isinstance(data, pd.DataFrame):
             results_list = dataframe_to_dict_list(data)
        elif isinstance(data, list):
             for item in data:
                 # Check if it's a DataFrame-like object (ErgastResultFrame)
                 if hasattr(item, 'to_dict') and hasattr(item, 'columns'):
                     try:
                         # Convert DataFrame to list of records
                         records = dataframe_to_dict_list(item)
                         results_list.extend(records)
                     except Exception as e:
                         print(f"Error converting item: {e}")
                 elif isinstance(item, dict):
                     results_list.append(item)
                 else:
                     try:
                         results_list.append(vars(item))
                     except:
                         results_list.append(str(item))
        else:
             # Fallback if it's a DataFrame but not caught above
             try:
                 results_list = dataframe_to_dict_list(data)
             except:
                 results_list = []

        return ResponseWrapper(
            data=results_list,
            meta={
                "year": year,
                "round": round,
                "driver": driver,
                "source": "Ergast API"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ERGAST_ERROR",
                "message": f"Error retrieving historical results for {year}",
                "details": {"error": str(e)}
            }
        )

@router.get("/historical/{year}/drivers", response_model=ResponseWrapper)
def get_historical_drivers(
    year: int,
    round: Optional[int] = Query(None, description="Round number")
):
    """
    Get historical drivers for a specific year using Ergast API.
    """
    try:
        drivers = ergast.get_driver_info(season=year, round=round)
        
        if drivers is None or drivers.empty:
             raise HTTPException(
                status_code=404,
                detail={
                    "code": "DRIVERS_NOT_FOUND",
                    "message": f"No historical drivers found for year {year}",
                    "details": {}
                }
            )
            
        drivers_list = dataframe_to_dict_list(drivers)
        
        return ResponseWrapper(
            data=drivers_list,
            meta={
                "year": year,
                "round": round,
                "count": len(drivers_list),
                "source": "Ergast API"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ERGAST_ERROR",
                "message": f"Error retrieving historical drivers for {year}",
                "details": {"error": str(e)}
            }
        )

@router.get("/historical/{year}/constructors", response_model=ResponseWrapper)
def get_historical_constructors(
    year: int,
    round: Optional[int] = Query(None, description="Round number")
):
    """
    Get historical constructors for a specific year using Ergast API.
    """
    try:
        constructors = ergast.get_constructor_info(season=year, round=round)
        
        if constructors is None or constructors.empty:
             raise HTTPException(
                status_code=404,
                detail={
                    "code": "CONSTRUCTORS_NOT_FOUND",
                    "message": f"No historical constructors found for year {year}",
                    "details": {}
                }
            )
            
        constructors_list = dataframe_to_dict_list(constructors)
        
        return ResponseWrapper(
            data=constructors_list,
            meta={
                "year": year,
                "round": round,
                "count": len(constructors_list),
                "source": "Ergast API"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ERGAST_ERROR",
                "message": f"Error retrieving historical constructors for {year}",
                "details": {"error": str(e)}
            }
        )

@router.get("/historical/{year}/standings/drivers", response_model=ResponseWrapper)
def get_historical_driver_standings(
    year: int,
    round: Optional[int] = Query(None, description="Round number")
):
    """
    Get historical driver standings for a specific year using Ergast API.
    """
    try:
        standings = ergast.get_driver_standings(season=year, round=round)
        
        if standings is None or standings.content is None or (hasattr(standings.content, 'empty') and standings.content.empty):
             raise HTTPException(
                status_code=404,
                detail={
                    "code": "STANDINGS_NOT_FOUND",
                    "message": f"No historical driver standings found for year {year}",
                    "details": {}
                }
            )
            
        data = standings.content
        standings_list = []
        if hasattr(data, 'to_dict'):
             standings_list = dataframe_to_dict_list(data)
        else:
             # Fallback
             try:
                 standings_list = dataframe_to_dict_list(data)
             except:
                 standings_list = []

        return ResponseWrapper(
            data=standings_list,
            meta={
                "year": year,
                "round": round,
                "source": "Ergast API"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ERGAST_ERROR",
                "message": f"Error retrieving historical driver standings for {year}",
                "details": {"error": str(e)}
            }
        )

@router.get("/historical/{year}/standings/constructors", response_model=ResponseWrapper)
def get_historical_constructor_standings(
    year: int,
    round: Optional[int] = Query(None, description="Round number")
):
    """
    Get historical constructor standings for a specific year using Ergast API.
    """
    try:
        standings = ergast.get_constructor_standings(season=year, round=round)
        
        if standings is None or standings.content is None or (hasattr(standings.content, 'empty') and standings.content.empty):
             raise HTTPException(
                status_code=404,
                detail={
                    "code": "STANDINGS_NOT_FOUND",
                    "message": f"No historical constructor standings found for year {year}",
                    "details": {}
                }
            )
            
        data = standings.content
        standings_list = []
        if hasattr(data, 'to_dict'):
             standings_list = dataframe_to_dict_list(data)
        else:
             # Fallback
             try:
                 standings_list = dataframe_to_dict_list(data)
             except:
                 standings_list = []

        return ResponseWrapper(
            data=standings_list,
            meta={
                "year": year,
                "round": round,
                "source": "Ergast API"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ERGAST_ERROR",
                "message": f"Error retrieving historical constructor standings for {year}",
                "details": {"error": str(e)}
            }
        )
