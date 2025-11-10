"""
Event and session information endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import fastf1
import pandas as pd
from api.models.schemas import EventInfo, SessionInfo, ResponseWrapper
from utils.serialization import datetime_to_iso8601

router = APIRouter()


@router.get("/events/{year}", response_model=ResponseWrapper)
async def get_events(year: int):
    """
    Get all events for a specific year.
    """
    try:
        schedule = fastf1.get_event_schedule(year)
        
        events = []
        for _, event in schedule.iterrows():
            events.append({
                "event_name": event.get("EventName", ""),
                "event_date": datetime_to_iso8601(event.get("EventDate")),
                "event_format": event.get("EventFormat", ""),
                "location": event.get("Location", ""),
                "country": event.get("Country", ""),
                "timezone": event.get("Timezone", ""),
                "round_number": int(event.get("RoundNumber", 0)) if pd.notna(event.get("RoundNumber")) else None
            })
        
        return ResponseWrapper(
            data=events,
            meta={"year": year, "count": len(events)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "EVENTS_NOT_FOUND",
                "message": f"Could not retrieve events for year {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/events/{year}/{event_name}", response_model=ResponseWrapper)
async def get_event(year: int, event_name: str):
    """
    Get specific event details.
    """
    try:
        session = fastf1.get_session(year, event_name, 'R')  # Use race session to get event info
        session.load()
        
        event_data = {
            "event_name": session.event.get("EventName", ""),
            "event_date": datetime_to_iso8601(session.event.get("EventDate")),
            "event_format": session.event.get("EventFormat", ""),
            "location": session.event.get("Location", ""),
            "country": session.event.get("Country", ""),
            "timezone": session.event.get("Timezone", ""),
            "round_number": session.event.get("RoundNumber")
        }
        
        return ResponseWrapper(data=event_data)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "EVENT_NOT_FOUND",
                "message": f"Event '{event_name}' not found for year {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/sessions/{year}/{event_name}/{session_type}", response_model=ResponseWrapper)
async def get_session_info(
    year: int,
    event_name: str,
    session_type: str = Query(..., description="Session type: FP1, FP2, FP3, Q, R, S")
):
    """
    Get session information.
    Session types: FP1, FP2, FP3 (Free Practice), Q (Qualifying), R (Race), S (Sprint)
    """
    valid_types = ['FP1', 'FP2', 'FP3', 'Q', 'R', 'S']
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
        
        session_data = {
            "session_name": session.name,
            "session_date": datetime_to_iso8601(session.date),
            "session_type": session_type.upper(),
            "event_name": session.event.get("EventName", ""),
            "year": year,
            "session_status": session.status
        }
        
        return ResponseWrapper(data=session_data)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "SESSION_NOT_FOUND",
                "message": f"Session '{session_type}' not found for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

