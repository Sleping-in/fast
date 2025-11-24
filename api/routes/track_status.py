"""
Track status endpoints.
"""
from fastapi import APIRouter, HTTPException
import fastf1
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list

router = APIRouter()


@router.get("/track-status/{year}/{event_name}/{session_type}", response_model=ResponseWrapper)
def get_track_status(
    year: int,
    event_name: str,
    session_type: str
):
    """
    Get track status data for a session (flags, safety car, VSC, etc.).
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
        
        if not hasattr(session, 'track_status_data') or session.track_status_data is None or session.track_status_data.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TRACK_STATUS_NOT_FOUND",
                    "message": f"No track status data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        track_status = session.track_status_data
        status_list = dataframe_to_dict_list(track_status)
        
        return ResponseWrapper(
            data=status_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(status_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TRACK_STATUS_ERROR",
                "message": f"Could not retrieve track status for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/track-status/{year}/{event_name}/{session_type}/safety-car", response_model=ResponseWrapper)
def get_safety_car_periods(
    year: int,
    event_name: str,
    session_type: str
):
    """Get all safety car periods."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        if not hasattr(session, 'track_status_data') or session.track_status_data is None or session.track_status_data.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TRACK_STATUS_NOT_FOUND",
                    "message": f"No track status data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        track_status = session.track_status_data
        # Filter for safety car periods (Status == 4 typically)
        sc_periods = track_status[track_status['Status'] == 4] if 'Status' in track_status.columns else track_status[track_status['Status'].str.contains('SC', case=False, na=False)]
        
        periods_list = dataframe_to_dict_list(sc_periods)
        
        return ResponseWrapper(
            data=periods_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(periods_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TRACK_STATUS_ERROR",
                "message": f"Could not retrieve safety car periods for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/track-status/{year}/{event_name}/{session_type}/vsc", response_model=ResponseWrapper)
def get_vsc_periods(
    year: int,
    event_name: str,
    session_type: str
):
    """Get all Virtual Safety Car periods."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        if not hasattr(session, 'track_status_data') or session.track_status_data is None or session.track_status_data.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TRACK_STATUS_NOT_FOUND",
                    "message": f"No track status data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        track_status = session.track_status_data
        # Filter for VSC periods (Status == 6 typically)
        vsc_periods = track_status[track_status['Status'] == 6] if 'Status' in track_status.columns else track_status[track_status['Status'].str.contains('VSC', case=False, na=False)]
        
        periods_list = dataframe_to_dict_list(vsc_periods)
        
        return ResponseWrapper(
            data=periods_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(periods_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TRACK_STATUS_ERROR",
                "message": f"Could not retrieve VSC periods for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/track-status/{year}/{event_name}/{session_type}/red-flags", response_model=ResponseWrapper)
def get_red_flag_periods(
    year: int,
    event_name: str,
    session_type: str
):
    """Get all red flag periods."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        if not hasattr(session, 'track_status_data') or session.track_status_data is None or session.track_status_data.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TRACK_STATUS_NOT_FOUND",
                    "message": f"No track status data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        track_status = session.track_status_data
        # Filter for red flags (Status == 5 typically)
        red_flags = track_status[track_status['Status'] == 5] if 'Status' in track_status.columns else track_status[track_status['Status'].str.contains('RED', case=False, na=False)]
        
        flags_list = dataframe_to_dict_list(red_flags)
        
        return ResponseWrapper(
            data=flags_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(flags_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TRACK_STATUS_ERROR",
                "message": f"Could not retrieve red flag periods for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/track-status/{year}/{event_name}/{session_type}/yellow-flags", response_model=ResponseWrapper)
def get_yellow_flag_periods(
    year: int,
    event_name: str,
    session_type: str
):
    """Get all yellow flag periods."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        if not hasattr(session, 'track_status_data') or session.track_status_data is None or session.track_status_data.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "TRACK_STATUS_NOT_FOUND",
                    "message": f"No track status data found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        track_status = session.track_status_data
        # Filter for yellow flags (Status == 2 typically)
        yellow_flags = track_status[track_status['Status'] == 2] if 'Status' in track_status.columns else track_status[track_status['Status'].str.contains('YELLOW', case=False, na=False)]
        
        flags_list = dataframe_to_dict_list(yellow_flags)
        
        return ResponseWrapper(
            data=flags_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(flags_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TRACK_STATUS_ERROR",
                "message": f"Could not retrieve yellow flag periods for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

