"""
Championship standings endpoints.
"""
from fastapi import APIRouter, HTTPException
import fastf1
from fastf1.ergast import Ergast
import pandas as pd
from api.models.schemas import ResponseWrapper

router = APIRouter()


@router.get("/standings/{year}/drivers", response_model=ResponseWrapper)
def get_driver_standings(year: int):
    """Get driver championship standings for a year."""
    try:
        ergast = Ergast()
        standings_data = ergast.get_driver_standings(season=year)
        
        if standings_data.content and not standings_data.content[0].empty:
            df = standings_data.content[0]
            standings = []
            
            for _, row in df.iterrows():
                # Handle constructor info which might be a list or single value
                team_name = "Unknown"
                if 'constructorNames' in row and row['constructorNames']:
                    team_name = row['constructorNames'][0] if isinstance(row['constructorNames'], list) else row['constructorNames']
                elif 'constructorName' in row:
                    team_name = row['constructorName']
                
                # Handle potential NaN values
                points = row.get('points', 0)
                wins = row.get('wins', 0)
                position = row.get('position', 0)
                
                standings.append({
                    "driver": row.get('driverCode', ''),
                    "full_name": f"{row.get('givenName', '')} {row.get('familyName', '')}",
                    "team": team_name,
                    "points": float(points) if pd.notna(points) else 0.0,
                    "wins": int(wins) if pd.notna(wins) else 0,
                    "podiums": 0, # Ergast doesn't provide podium count directly in standings
                    "position": int(position) if pd.notna(position) else 0
                })
            
            return ResponseWrapper(
                data=standings,
                meta={
                    "year": year,
                    "count": len(standings)
                }
            )
        else:
             raise HTTPException(
                status_code=404,
                detail={
                    "code": "STANDINGS_NOT_FOUND",
                    "message": f"No driver standings found for year {year}",
                    "details": {}
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
        ergast = Ergast()
        standings_data = ergast.get_constructor_standings(season=year)
        
        if standings_data.content and not standings_data.content[0].empty:
            df = standings_data.content[0]
            standings = []
            
            for _, row in df.iterrows():
                points = row.get('points', 0)
                wins = row.get('wins', 0)
                position = row.get('position', 0)

                standings.append({
                    "team": row.get('constructorName', ''),
                    "points": float(points) if pd.notna(points) else 0.0,
                    "wins": int(wins) if pd.notna(wins) else 0,
                    "position": int(position) if pd.notna(position) else 0
                })
            
            return ResponseWrapper(
                data=standings,
                meta={
                    "year": year,
                    "count": len(standings)
                }
            )
        else:
             raise HTTPException(
                status_code=404,
                detail={
                    "code": "STANDINGS_NOT_FOUND",
                    "message": f"No constructor standings found for year {year}",
                    "details": {}
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
        
        # Find event round
        round_number = None
        for _, event in schedule.iterrows():
            if event_name.lower() in event['EventName'].lower():
                round_number = event['RoundNumber']
                break
        
        if round_number is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "EVENT_NOT_FOUND",
                    "message": f"Event {event_name} not found for year {year}",
                    "details": {}
                }
            )
            
        ergast = Ergast()
        standings_data = ergast.get_driver_standings(season=year, round=round_number)
        
        if standings_data.content and not standings_data.content[0].empty:
            df = standings_data.content[0]
            standings = []
            
            for _, row in df.iterrows():
                # Handle constructor info
                team_name = "Unknown"
                if 'constructorNames' in row and row['constructorNames']:
                    team_name = row['constructorNames'][0] if isinstance(row['constructorNames'], list) else row['constructorNames']
                elif 'constructorName' in row:
                    team_name = row['constructorName']

                points = row.get('points', 0)
                wins = row.get('wins', 0)
                position = row.get('position', 0)

                standings.append({
                    "driver": row.get('driverCode', ''),
                    "full_name": f"{row.get('givenName', '')} {row.get('familyName', '')}",
                    "team": team_name,
                    "points": float(points) if pd.notna(points) else 0.0,
                    "wins": int(wins) if pd.notna(wins) else 0,
                    "podiums": 0,
                    "position": int(position) if pd.notna(position) else 0
                })
            
            return ResponseWrapper(
                data=standings,
                meta={
                    "year": year,
                    "event_name": event_name,
                    "round": int(round_number),
                    "count": len(standings)
                }
            )
        else:
             raise HTTPException(
                status_code=404,
                detail={
                    "code": "STANDINGS_NOT_FOUND",
                    "message": f"No driver standings found for year {year} after round {round_number}",
                    "details": {}
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
        
        # Find event round
        round_number = None
        for _, event in schedule.iterrows():
            if event_name.lower() in event['EventName'].lower():
                round_number = event['RoundNumber']
                break
        
        if round_number is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "EVENT_NOT_FOUND",
                    "message": f"Event {event_name} not found for year {year}",
                    "details": {}
                }
            )
            
        ergast = Ergast()
        standings_data = ergast.get_constructor_standings(season=year, round=round_number)
        
        if standings_data.content and not standings_data.content[0].empty:
            df = standings_data.content[0]
            standings = []
            
            for _, row in df.iterrows():
                points = row.get('points', 0)
                wins = row.get('wins', 0)
                position = row.get('position', 0)

                standings.append({
                    "team": row.get('constructorName', ''),
                    "points": float(points) if pd.notna(points) else 0.0,
                    "wins": int(wins) if pd.notna(wins) else 0,
                    "position": int(position) if pd.notna(position) else 0
                })
            
            return ResponseWrapper(
                data=standings,
                meta={
                    "year": year,
                    "event_name": event_name,
                    "round": int(round_number),
                    "count": len(standings)
                }
            )
        else:
             raise HTTPException(
                status_code=404,
                detail={
                    "code": "STANDINGS_NOT_FOUND",
                    "message": f"No constructor standings found for year {year} after round {round_number}",
                    "details": {}
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

