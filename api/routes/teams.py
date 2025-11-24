"""
Team/Constructor endpoints.
"""
from fastapi import APIRouter, HTTPException
import fastf1
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list

router = APIRouter()


@router.get("/teams/{year}", response_model=ResponseWrapper)
def get_teams(year: int):
    """Get all teams for a year."""
    try:
        schedule = fastf1.get_event_schedule(year)
        if schedule is None or schedule.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TEAMS_NOT_FOUND",
                    "message": f"No schedule found for year {year}",
                    "details": {}
                }
            )
        
        # Get teams from first event's results
        first_event = schedule.iloc[0]
        try:
            session = fastf1.get_session(year, first_event['EventName'], 'R')
            session.load()
            results = session.results
            
            if results is None or results.empty:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "code": "TEAMS_NOT_FOUND",
                        "message": f"No results found for year {year}",
                        "details": {}
                    }
                )
            
            # Extract unique teams
            teams = results[['TeamName', 'TeamColor']].drop_duplicates() if 'TeamName' in results.columns else []
            teams_list = dataframe_to_dict_list(teams) if hasattr(teams, 'to_dict') else []
            
            return ResponseWrapper(
                data=teams_list,
                meta={
                    "year": year,
                    "count": len(teams_list)
                }
            )
        except:
            # Fallback: return empty list
            return ResponseWrapper(
                data=[],
                meta={
                    "year": year,
                    "count": 0
                }
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TEAMS_ERROR",
                "message": f"Could not retrieve teams for year {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/teams/{year}/{event_name}", response_model=ResponseWrapper)
def get_event_teams(year: int, event_name: str):
    """Get teams for a specific event."""
    try:
        session = fastf1.get_session(year, event_name, 'R')
        # Load only results to speed up
        session.load(weather=False, messages=False, telemetry=False, laps=False)
        results = session.results
        
        if results is None or results.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TEAMS_NOT_FOUND",
                    "message": f"No results found for {event_name} {year}",
                    "details": {}
                }
            )
        
        teams = results[['TeamName', 'TeamColor']].drop_duplicates() if 'TeamName' in results.columns else []
        teams_list = dataframe_to_dict_list(teams) if hasattr(teams, 'to_dict') else []
        
        return ResponseWrapper(
            data=teams_list,
            meta={
                "year": year,
                "event_name": event_name,
                "count": len(teams_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TEAMS_ERROR",
                "message": f"Could not retrieve teams for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/teams/{year}/{team_name}/results", response_model=ResponseWrapper)
def get_team_results(year: int, team_name: str):
    """Get results for a specific team."""
    try:
        schedule = fastf1.get_event_schedule(year)
        if schedule is None or schedule.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TEAMS_NOT_FOUND",
                    "message": f"No schedule found for year {year}",
                    "details": {}
                }
            )
        
        all_results = []
        for _, event in schedule.iterrows():
            try:
                session = fastf1.get_session(year, event['EventName'], 'R')
                # Load only results to speed up
                session.load(weather=False, messages=False, telemetry=False, laps=False)
                results = session.results
                
                if results is not None and not results.empty and 'TeamName' in results.columns:
                    team_results = results[results['TeamName'].str.contains(team_name, case=False, na=False)]
                    if not team_results.empty:
                        for _, result in team_results.iterrows():
                            all_results.append({
                                "event_name": event['EventName'],
                                "driver": result.get('Abbreviation'),
                                "position": float(result.get('Position')) if result.get('Position') is not None else None,
                                "points": float(result.get('Points')) if result.get('Points') is not None else None
                            })
            except:
                continue
        
        return ResponseWrapper(
            data=all_results,
            meta={
                "year": year,
                "team_name": team_name,
                "count": len(all_results)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TEAMS_ERROR",
                "message": f"Could not retrieve team results for {team_name} {year}",
                "details": {"error": str(e)}
            }
        )

