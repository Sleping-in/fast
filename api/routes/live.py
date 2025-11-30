from fastapi import APIRouter, HTTPException, Query
from api.services.live_timing import recorder
from api.services.live_state import live_state
from api.models.schemas import ResponseWrapper
import os
import json

router = APIRouter()

@router.post("/live/start", response_model=ResponseWrapper)
def start_live_recording(filename: str = Query(None, description="Optional filename for the recording")):
    """
    Start recording live timing data from F1 SignalR API.
    This starts a background process that connects to the live stream.
    """
    result = recorder.start_recording(filename)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result)
    
    return ResponseWrapper(
        data=result,
        meta={"action": "start_recording"}
    )

@router.post("/live/stop", response_model=ResponseWrapper)
def stop_live_recording():
    """
    Stop the live recording.
    """
    result = recorder.stop_recording()
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result)
    
    return ResponseWrapper(
        data=result,
        meta={"action": "stop_recording"}
    )

@router.get("/live/status", response_model=ResponseWrapper)
def get_live_status():
    """
    Get the current status of the live recorder.
    """
    status = recorder.get_status()
    return ResponseWrapper(
        data=status,
        meta={"action": "get_status"}
    )

@router.get("/live/leaderboard", response_model=ResponseWrapper)
def get_live_leaderboard():
    """
    Get the current live leaderboard with positions, lap times, and gaps.
    """
    leaderboard = live_state.get_leaderboard()
    return ResponseWrapper(
        data=leaderboard,
        meta={
            "last_updated": live_state.last_updated.isoformat(),
            "count": len(leaderboard)
        }
    )

@router.get("/live/weather", response_model=ResponseWrapper)
def get_live_weather():
    """
    Get the current live weather data.
    """
    return ResponseWrapper(
        data=live_state.weather,
        meta={"last_updated": live_state.last_updated.isoformat()}
    )

@router.get("/live/track-status", response_model=ResponseWrapper)
def get_live_track_status():
    """
    Get the current track status (flags, safety car, etc.).
    """
    return ResponseWrapper(
        data=live_state.track_status,
        meta={"last_updated": live_state.last_updated.isoformat()}
    )

@router.get("/live/session-status", response_model=ResponseWrapper)
def get_live_session_status():
    """
    Get the current session status.
    """
    return ResponseWrapper(
        data=live_state.session_status,
        meta={"last_updated": live_state.last_updated.isoformat()}
    )

@router.get("/live/log", response_model=ResponseWrapper)
def get_live_log(lines: int = Query(10, description="Number of last lines to retrieve")):
    """
    Get the latest raw log lines from the current recording file.
    Useful for debugging or getting raw stream data.
    """
    status = recorder.get_status()
    if not status["current_file"] or not os.path.exists(status["current_file"]):
        raise HTTPException(status_code=404, detail="No active recording file found")
    
    try:
        with open(status["current_file"], 'r') as f:
            # Simple tail implementation
            # Note: This is not efficient for huge files, but fine for live buffers
            all_lines = f.readlines()
            last_lines = all_lines[-lines:] if lines > 0 else []
            
            # Try to parse JSON if possible
            parsed_lines = []
            for line in last_lines:
                try:
                    parsed_lines.append(json.loads(line))
                except:
                    parsed_lines.append(line.strip())
            
            return ResponseWrapper(
                data=parsed_lines,
                meta={
                    "file": status["current_file"],
                    "count": len(parsed_lines),
                    "total_lines": len(all_lines)
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
