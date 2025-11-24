"""
Race control messages endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import fastf1
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list

router = APIRouter()


@router.get("/race-control/{year}/{event_name}/{session_type}", response_model=ResponseWrapper)
def get_race_control_messages(
    year: int,
    event_name: str,
    session_type: str,
    category: Optional[str] = Query(None, description="Filter by category (penalty, investigation, etc.)")
):
    """
    Get race control messages (penalties, investigations, announcements).
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
        
        if not hasattr(session, 'race_control_messages') or session.race_control_messages is None or session.race_control_messages.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "RACE_CONTROL_NOT_FOUND",
                    "message": f"No race control messages found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        messages = session.race_control_messages
        
        # Filter by category if provided
        if category:
            if 'Category' in messages.columns:
                messages = messages[messages['Category'].str.contains(category, case=False, na=False)]
            elif 'Message' in messages.columns:
                messages = messages[messages['Message'].str.contains(category, case=False, na=False)]
        
        messages_list = dataframe_to_dict_list(messages)
        
        return ResponseWrapper(
            data=messages_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(messages_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "RACE_CONTROL_ERROR",
                "message": f"Could not retrieve race control messages for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/race-control/{year}/{event_name}/{session_type}/penalties", response_model=ResponseWrapper)
def get_penalties(
    year: int,
    event_name: str,
    session_type: str
):
    """Get all penalties issued."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        if not hasattr(session, 'race_control_messages') or session.race_control_messages is None or session.race_control_messages.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "RACE_CONTROL_NOT_FOUND",
                    "message": f"No race control messages found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        messages = session.race_control_messages
        
        # Filter for penalties
        if 'Category' in messages.columns:
            penalties = messages[messages['Category'].str.contains('penalty', case=False, na=False)]
        elif 'Message' in messages.columns:
            penalties = messages[messages['Message'].str.contains('penalty', case=False, na=False)]
        else:
            penalties = messages
        
        penalties_list = dataframe_to_dict_list(penalties)
        
        return ResponseWrapper(
            data=penalties_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(penalties_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "RACE_CONTROL_ERROR",
                "message": f"Could not retrieve penalties for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/race-control/{year}/{event_name}/{session_type}/investigations", response_model=ResponseWrapper)
def get_investigations(
    year: int,
    event_name: str,
    session_type: str
):
    """Get all investigations."""
    try:
        session = fastf1.get_session(year, event_name, session_type.upper())
        session.load()
        
        if not hasattr(session, 'race_control_messages') or session.race_control_messages is None or session.race_control_messages.empty:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "RACE_CONTROL_NOT_FOUND",
                    "message": f"No race control messages found for {event_name} {year} {session_type}",
                    "details": {}
                }
            )
        
        messages = session.race_control_messages
        
        # Filter for investigations
        if 'Category' in messages.columns:
            investigations = messages[messages['Category'].str.contains('investigation', case=False, na=False)]
        elif 'Message' in messages.columns:
            investigations = messages[messages['Message'].str.contains('investigation', case=False, na=False)]
        else:
            investigations = messages
        
        investigations_list = dataframe_to_dict_list(investigations)
        
        return ResponseWrapper(
            data=investigations_list,
            meta={
                "year": year,
                "event_name": event_name,
                "session_type": session_type.upper(),
                "count": len(investigations_list)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "RACE_CONTROL_ERROR",
                "message": f"Could not retrieve investigations for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

