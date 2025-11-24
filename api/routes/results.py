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
def get_race_results(year: int, event_name: str):
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
def get_qualifying_results(year: int, event_name: str):
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
def get_sprint_results(year: int, event_name: str):
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


@router.get("/results/{year}/{event_name}/sprint-qualifying", response_model=ResponseWrapper)
def get_sprint_qualifying_results(year: int, event_name: str):
    """
    Get sprint qualifying (sprint shootout) results for a specific event.
    Sprint qualifying determines the grid for the sprint race.
    """
    try:
        session = fastf1.get_session(year, event_name, 'SQ')
        session.load()
        
        results = session.results
        
        if results is None or results.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "RESULTS_NOT_FOUND",
                    "message": f"No sprint qualifying results found for {event_name} {year}",
                    "details": {}
                }
            )
        
        results_list = dataframe_to_dict_list(results)
        
        return ResponseWrapper(
            data=results_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": "Sprint Qualifying",
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
                "message": f"Could not retrieve sprint qualifying results for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )



@router.get("/results/{year}/{event_name}/qualifying/q1", response_model=ResponseWrapper)
def get_q1_results(year: int, event_name: str):
    """Get Q1 qualifying results."""
    try:
        session = fastf1.get_session(year, event_name, 'Q')
        # Load only results, not all telemetry/laps
        session.load(weather=False, messages=False, telemetry=False, laps=False)
        results = session.results
        
        if results is None or results.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "RESULTS_NOT_FOUND",
                    "message": f"No Q1 results found for {event_name} {year}",
                    "details": {}
                }
            )
        
        if 'Q1' in results.columns:
            q1_results = results[['DriverNumber', 'Abbreviation', 'FullName', 'TeamName', 'Q1']].copy()
            q1_results = q1_results[pd.notna(q1_results['Q1'])]
            q1_results = q1_results.sort_values('Q1')
            results_list = dataframe_to_dict_list(q1_results)
        else:
            results_list = dataframe_to_dict_list(results)
        
        return ResponseWrapper(
            data=results_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": "Q1",
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
                "message": f"Could not retrieve Q1 results for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/results/{year}/{event_name}/qualifying/q2", response_model=ResponseWrapper)
def get_q2_results(year: int, event_name: str):
    """Get Q2 qualifying results."""
    try:
        session = fastf1.get_session(year, event_name, 'Q')
        # Load only results, not all telemetry/laps
        session.load(weather=False, messages=False, telemetry=False, laps=False)
        results = session.results
        
        if results is None or results.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "RESULTS_NOT_FOUND",
                    "message": f"No Q2 results found for {event_name} {year}",
                    "details": {}
                }
            )
        
        if 'Q2' in results.columns:
            q2_results = results[['DriverNumber', 'Abbreviation', 'FullName', 'TeamName', 'Q2']].copy()
            q2_results = q2_results[pd.notna(q2_results['Q2'])]
            q2_results = q2_results.sort_values('Q2')
            results_list = dataframe_to_dict_list(q2_results)
        else:
            results_list = dataframe_to_dict_list(results)
        
        return ResponseWrapper(
            data=results_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": "Q2",
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
                "message": f"Could not retrieve Q2 results for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/results/{year}/{event_name}/qualifying/q3", response_model=ResponseWrapper)
def get_q3_results(year: int, event_name: str):
    """Get Q3 qualifying results."""
    try:
        session = fastf1.get_session(year, event_name, 'Q')
        # Load only results, not all telemetry/laps
        session.load(weather=False, messages=False, telemetry=False, laps=False)
        results = session.results
        
        if results is None or results.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "RESULTS_NOT_FOUND",
                    "message": f"No Q3 results found for {event_name} {year}",
                    "details": {}
                }
            )
        
        if 'Q3' in results.columns:
            q3_results = results[['DriverNumber', 'Abbreviation', 'FullName', 'TeamName', 'Q3']].copy()
            q3_results = q3_results[pd.notna(q3_results['Q3'])]
            q3_results = q3_results.sort_values('Q3')
            results_list = dataframe_to_dict_list(q3_results)
        else:
            results_list = dataframe_to_dict_list(results)
        
        return ResponseWrapper(
            data=results_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": "Q3",
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
                "message": f"Could not retrieve Q3 results for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/grid/{year}/{event_name}", response_model=ResponseWrapper)
def get_grid_positions(year: int, event_name: str):
    """Get starting grid positions."""
    try:
        session = fastf1.get_session(year, event_name, 'R')
        # Load only results, not all telemetry/laps
        session.load(weather=False, messages=False, telemetry=False, laps=False)
        results = session.results
        
        if results is None or results.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "GRID_NOT_FOUND",
                    "message": f"No grid data found for {event_name} {year}",
                    "details": {}
                }
            )
        
        grid_col = 'GridPosition' if 'GridPosition' in results.columns else 'Position'
        grid_data = results[['DriverNumber', 'Abbreviation', 'FullName', 'TeamName', grid_col]].copy()
        grid_data = grid_data.sort_values(grid_col)
        grid_list = dataframe_to_dict_list(grid_data)
        
        return ResponseWrapper(
            data=grid_list,
            meta={
                "year": year,
                "event_name": event_name,
                "count": len(grid_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "GRID_ERROR",
                "message": f"Could not retrieve grid positions for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )
