"""
Historical data endpoints using Ergast API (via FastF1).
Supports data for seasons prior to 2018.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from fastf1.ergast import Ergast
from api.models.schemas import ResponseWrapper

router = APIRouter()
ergast = Ergast()

@router.get("/historical/seasons", response_model=ResponseWrapper)
def get_historical_seasons(
    limit: int = Query(30, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get list of historical seasons."""
    try:
        seasons = ergast.get_seasons(limit=limit, offset=offset)
        return ResponseWrapper(
            data=seasons.content[0].to_dict(orient='records') if seasons.content else [],
            meta={
                "total": seasons.total_results,
                "limit": limit,
                "offset": offset
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ERGAST_ERROR",
                "message": "Could not retrieve historical seasons",
                "details": {"error": str(e)}
            }
        )

@router.get("/historical/{year}/races", response_model=ResponseWrapper)
def get_historical_races(
    year: int,
    limit: int = Query(30, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get list of races for a historical season."""
    try:
        races = ergast.get_race_schedule(season=year, limit=limit, offset=offset)
        return ResponseWrapper(
            data=races.content[0].to_dict(orient='records') if races.content else [],
            meta={
                "year": year,
                "total": races.total_results,
                "limit": limit,
                "offset": offset
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ERGAST_ERROR",
                "message": f"Could not retrieve races for {year}",
                "details": {"error": str(e)}
            }
        )

@router.get("/historical/{year}/drivers", response_model=ResponseWrapper)
def get_historical_drivers(
    year: int,
    limit: int = Query(30, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get list of drivers for a historical season."""
    try:
        drivers = ergast.get_driver_info(season=year, limit=limit, offset=offset)
        return ResponseWrapper(
            data=drivers.content[0].to_dict(orient='records') if drivers.content else [],
            meta={
                "year": year,
                "total": drivers.total_results,
                "limit": limit,
                "offset": offset
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ERGAST_ERROR",
                "message": f"Could not retrieve drivers for {year}",
                "details": {"error": str(e)}
            }
        )

@router.get("/historical/{year}/constructors", response_model=ResponseWrapper)
def get_historical_constructors(
    year: int,
    limit: int = Query(30, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get list of constructors for a historical season."""
    try:
        constructors = ergast.get_constructor_info(season=year, limit=limit, offset=offset)
        return ResponseWrapper(
            data=constructors.content[0].to_dict(orient='records') if constructors.content else [],
            meta={
                "year": year,
                "total": constructors.total_results,
                "limit": limit,
                "offset": offset
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ERGAST_ERROR",
                "message": f"Could not retrieve constructors for {year}",
                "details": {"error": str(e)}
            }
        )

@router.get("/historical/{year}/{round}/results", response_model=ResponseWrapper)
def get_historical_results(
    year: int,
    round: int,
    limit: int = Query(30, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get race results for a historical race."""
    try:
        results = ergast.get_race_results(season=year, round=round, limit=limit, offset=offset)
        return ResponseWrapper(
            data=results.content[0].to_dict(orient='records') if results.content else [],
            meta={
                "year": year,
                "round": round,
                "total": results.total_results,
                "limit": limit,
                "offset": offset
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ERGAST_ERROR",
                "message": f"Could not retrieve results for {year} round {round}",
                "details": {"error": str(e)}
            }
        )
