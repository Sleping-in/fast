"""
Championship standings endpoints.
"""
from fastapi import APIRouter, HTTPException
import fastf1
import pandas as pd
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list

router = APIRouter()


@router.get("/standings/{year}/drivers", response_model=ResponseWrapper)
def get_driver_standings(year: int):
    """Get driver championship standings for a year."""
    try:
        schedule = fastf1.get_event_schedule(year)
        if schedule is None or schedule.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "STANDINGS_NOT_FOUND",
                    "message": f"No schedule found for year {year}",
                    "details": {}
                }
            )
        
        # Calculate standings from all race results
        # Optimize by loading only results, not all data
        driver_points = {}
        
        for _, event in schedule.iterrows():
            try:
                session = fastf1.get_session(year, event['EventName'], 'R')
                # Load only results to speed up
                session.load(weather=False, messages=False, telemetry=False, laps=False)
                results = session.results
                
                if results is not None and not results.empty:
                    for _, result in results.iterrows():
                        driver = result.get('Abbreviation')
                        points = result.get('Points')
                        
                        if driver and pd.notna(points):
                            if driver not in driver_points:
                                driver_points[driver] = {
                                    "driver": driver,
                                    "full_name": result.get('FullName'),
                                    "team": result.get('TeamName'),
                                    "points": 0.0,
                                    "wins": 0,
                                    "podiums": 0
                                }
                            
                            driver_points[driver]["points"] += float(points)
                            
                            position = result.get('Position')
                            if pd.notna(position):
                                if position == 1:
                                    driver_points[driver]["wins"] += 1
                                if position <= 3:
                                    driver_points[driver]["podiums"] += 1
            except Exception as e:
                # Skip events that fail to load
                continue
        
        # Sort by points
        standings = sorted(driver_points.values(), key=lambda x: x["points"], reverse=True)
        
        # Add position
        for i, standing in enumerate(standings, 1):
            standing["position"] = i
        
        return ResponseWrapper(
            data=standings,
            meta={
                "year": year,
                "count": len(standings)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "STANDINGS_ERROR",
                "message": f"Could not retrieve driver standings for year {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/standings/{year}/constructors", response_model=ResponseWrapper)
def get_constructor_standings(year: int):
    """Get constructor championship standings for a year."""
    try:
        schedule = fastf1.get_event_schedule(year)
        if schedule is None or schedule.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "STANDINGS_NOT_FOUND",
                    "message": f"No schedule found for year {year}",
                    "details": {}
                }
            )
        
        # Calculate standings from all race results
        # Optimize by loading only results, not all data
        team_points = {}
        
        for _, event in schedule.iterrows():
            try:
                session = fastf1.get_session(year, event['EventName'], 'R')
                # Load only results to speed up
                session.load(weather=False, messages=False, telemetry=False, laps=False)
                results = session.results
                
                if results is not None and not results.empty:
                    for _, result in results.iterrows():
                        team = result.get('TeamName')
                        points = result.get('Points')
                        
                        if team and pd.notna(points):
                            if team not in team_points:
                                team_points[team] = {
                                    "team": team,
                                    "points": 0.0,
                                    "wins": 0
                                }
                            
                            team_points[team]["points"] += float(points)
                            
                            position = result.get('Position')
                            if pd.notna(position) and position == 1:
                                team_points[team]["wins"] += 1
            except Exception as e:
                # Skip events that fail to load
                continue
        
        # Sort by points
        standings = sorted(team_points.values(), key=lambda x: x["points"], reverse=True)
        
        # Add position
        for i, standing in enumerate(standings, 1):
            standing["position"] = i
        
        return ResponseWrapper(
            data=standings,
            meta={
                "year": year,
                "count": len(standings)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "STANDINGS_ERROR",
                "message": f"Could not retrieve constructor standings for year {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/standings/{year}/drivers/after/{event_name}", response_model=ResponseWrapper)
def get_driver_standings_after_event(year: int, event_name: str):
    """Get driver standings after a specific event."""
    try:
        schedule = fastf1.get_event_schedule(year)
        if schedule is None or schedule.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "STANDINGS_NOT_FOUND",
                    "message": f"No schedule found for year {year}",
                    "details": {}
                }
            )
        
        # Find event index
        event_index = None
        for i, event in schedule.iterrows():
            if event_name.lower() in event['EventName'].lower():
                event_index = i
                break
        
        if event_index is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "EVENT_NOT_FOUND",
                    "message": f"Event {event_name} not found for year {year}",
                    "details": {}
                }
            )
        
        # Calculate standings up to and including this event
        driver_points = {}
        
        for i, event in schedule.iterrows():
            if i > event_index:
                break
            
            try:
                session = fastf1.get_session(year, event['EventName'], 'R')
                # Load only results to speed up
                session.load(weather=False, messages=False, telemetry=False, laps=False)
                results = session.results
                
                if results is not None and not results.empty:
                    for _, result in results.iterrows():
                        driver = result.get('Abbreviation')
                        points = result.get('Points')
                        
                        if driver and pd.notna(points):
                            if driver not in driver_points:
                                driver_points[driver] = {
                                    "driver": driver,
                                    "full_name": result.get('FullName'),
                                    "team": result.get('TeamName'),
                                    "points": 0.0
                                }
                            
                            driver_points[driver]["points"] += float(points)
            except Exception as e:
                # Skip events that fail to load
                continue
        
        # Sort by points
        standings = sorted(driver_points.values(), key=lambda x: x["points"], reverse=True)
        
        # Add position
        for i, standing in enumerate(standings, 1):
            standing["position"] = i
        
        return ResponseWrapper(
            data=standings,
            meta={
                "year": year,
                "event_name": event_name,
                "count": len(standings)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "STANDINGS_ERROR",
                "message": f"Could not retrieve driver standings after {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/standings/{year}/constructors/after/{event_name}", response_model=ResponseWrapper)
def get_constructor_standings_after_event(year: int, event_name: str):
    """Get constructor standings after a specific event."""
    try:
        schedule = fastf1.get_event_schedule(year)
        if schedule is None or schedule.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "STANDINGS_NOT_FOUND",
                    "message": f"No schedule found for year {year}",
                    "details": {}
                }
            )
        
        # Find event index
        event_index = None
        for i, event in schedule.iterrows():
            if event_name.lower() in event['EventName'].lower():
                event_index = i
                break
        
        if event_index is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "EVENT_NOT_FOUND",
                    "message": f"Event {event_name} not found for year {year}",
                    "details": {}
                }
            )
        
        # Calculate standings up to and including this event
        team_points = {}
        
        for i, event in schedule.iterrows():
            if i > event_index:
                break
            
            try:
                session = fastf1.get_session(year, event['EventName'], 'R')
                # Load only results to speed up
                session.load(weather=False, messages=False, telemetry=False, laps=False)
                results = session.results
                
                if results is not None and not results.empty:
                    for _, result in results.iterrows():
                        team = result.get('TeamName')
                        points = result.get('Points')
                        
                        if team and pd.notna(points):
                            if team not in team_points:
                                team_points[team] = {
                                    "team": team,
                                    "points": 0.0
                                }
                            
                            team_points[team]["points"] += float(points)
            except Exception as e:
                # Skip events that fail to load
                continue
        
        # Sort by points
        standings = sorted(team_points.values(), key=lambda x: x["points"], reverse=True)
        
        # Add position
        for i, standing in enumerate(standings, 1):
            standing["position"] = i
        
        return ResponseWrapper(
            data=standings,
            meta={
                "year": year,
                "event_name": event_name,
                "count": len(standings)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "STANDINGS_ERROR",
                "message": f"Could not retrieve constructor standings after {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

