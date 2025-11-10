"""
Race results endpoints.
"""
from fastapi import APIRouter, HTTPException
import fastf1
import pandas as pd
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list, datetime_to_iso8601

router = APIRouter()


@router.get("/results/{year}/{event_name}", response_model=ResponseWrapper)
async def get_race_results(year: int, event_name: str):
    """
    Get race results for a specific event.
    """
    try:
        session = fastf1.get_session(year, event_name, 'R')
        session.load()
        
        results = session.results
        
        if results is None or results.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "RESULTS_NOT_FOUND",
                    "message": f"No race results found for {event_name} {year}",
                    "details": {}
                }
            )
        
        # Convert to list of dicts
        results_list = dataframe_to_dict_list(results)
        
        return ResponseWrapper(
            data=results_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": "Race",
                "count": len(results_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "RESULTS_ERROR",
                "message": f"Could not retrieve race results for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/results/{year}/{event_name}/qualifying", response_model=ResponseWrapper)
async def get_qualifying_results(year: int, event_name: str):
    """
    Get qualifying results for a specific event.
    """
    try:
        session = fastf1.get_session(year, event_name, 'Q')
        session.load()
        
        results = session.results
        
        if results is None or results.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "RESULTS_NOT_FOUND",
                    "message": f"No qualifying results found for {event_name} {year}",
                    "details": {}
                }
            )
        
        results_list = dataframe_to_dict_list(results)
        
        return ResponseWrapper(
            data=results_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": "Qualifying",
                "count": len(results_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "RESULTS_ERROR",
                "message": f"Could not retrieve qualifying results for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/results/{year}/{event_name}/sprint", response_model=ResponseWrapper)
async def get_sprint_results(year: int, event_name: str):
    """
    Get sprint results for a specific event.
    """
    try:
        session = fastf1.get_session(year, event_name, 'S')
        session.load()
        
        results = session.results
        
        if results is None or results.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "RESULTS_NOT_FOUND",
                    "message": f"No sprint results found for {event_name} {year}",
                    "details": {}
                }
            )
        
        results_list = dataframe_to_dict_list(results)
        
        return ResponseWrapper(
            data=results_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": "Sprint",
                "count": len(results_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "RESULTS_ERROR",
                "message": f"Could not retrieve sprint results for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

