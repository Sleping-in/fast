"""
Circuit information endpoints.
"""
from fastapi import APIRouter, HTTPException
import fastf1
from api.models.schemas import ResponseWrapper
from utils.serialization import dataframe_to_dict_list

router = APIRouter()


@router.get("/circuits/{year}/{event_name}", response_model=ResponseWrapper)
def get_circuit_info(
    year: int,
    event_name: str
):
    """
    Get circuit information (layout, corners, marshal sectors, track length).
    """
    try:
        session = fastf1.get_session(year, event_name, 'R')
        session.load(laps=True, telemetry=True, weather=False, messages=False)
        circuit_info = session.get_circuit_info()
        
        if circuit_info is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "CIRCUIT_NOT_FOUND",
                    "message": f"Circuit information not found for {event_name} {year}",
                    "details": {}
                }
            )
        
        # Convert to dict
        if hasattr(circuit_info, 'to_dict'):
            circuit_dict = circuit_info.to_dict()
        else:
            circuit_dict = dataframe_to_dict_list(circuit_info) if hasattr(circuit_info, '__iter__') else {"data": str(circuit_info)}
        
        return ResponseWrapper(
            data=circuit_dict,
            meta={
                "year": year,
                "event_name": event_name
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "CIRCUIT_ERROR",
                "message": f"Could not retrieve circuit information for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/circuits/{year}/{event_name}/drs-zones", response_model=ResponseWrapper)
def get_drs_zones(
    year: int,
    event_name: str
):
    """Get DRS zone locations."""
    try:
        session = fastf1.get_session(year, event_name, 'R')
        session.load(laps=True, telemetry=True, weather=False, messages=False)
        circuit_info = session.get_circuit_info()
        
        if circuit_info is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "CIRCUIT_NOT_FOUND",
                    "message": f"Circuit information not found for {event_name} {year}",
                    "details": {}
                }
            )
        
        # DRS zones are typically in the circuit info
        # This is a simplified version - actual implementation may vary
        drs_zones = []
        if hasattr(circuit_info, 'drs_zones'):
            drs_zones = circuit_info.drs_zones
        elif hasattr(circuit_info, 'DRS'):
            drs_zones = circuit_info.DRS
        
        return ResponseWrapper(
            data=drs_zones if drs_zones else [],
            meta={
                "year": year,
                "event_name": event_name
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "CIRCUIT_ERROR",
                "message": f"Could not retrieve DRS zones for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/circuits/{year}/{event_name}/markers", response_model=ResponseWrapper)
def get_track_markers(
    year: int,
    event_name: str
):
    """Get track markers (corners, marshal sectors, marshal lights)."""
    try:
        session = fastf1.get_session(year, event_name, 'R')
        session.load(laps=True, telemetry=True, weather=False, messages=False)
        circuit_info = session.get_circuit_info()
        
        if circuit_info is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "CIRCUIT_NOT_FOUND",
                    "message": f"Circuit information not found for {event_name} {year}",
                    "details": {}
                }
            )
        
        markers = {}
        if hasattr(circuit_info, 'corners'):
            markers['corners'] = dataframe_to_dict_list(circuit_info.corners) if hasattr(circuit_info.corners, 'to_dict') else circuit_info.corners
        if hasattr(circuit_info, 'marshal_sectors'):
            markers['marshal_sectors'] = dataframe_to_dict_list(circuit_info.marshal_sectors) if hasattr(circuit_info.marshal_sectors, 'to_dict') else circuit_info.marshal_sectors
        
        return ResponseWrapper(
            data=markers,
            meta={
                "year": year,
                "event_name": event_name
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "CIRCUIT_ERROR",
                "message": f"Could not retrieve track markers for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/circuits/{year}/{event_name}/corners", response_model=ResponseWrapper)
def get_corners(
    year: int,
    event_name: str
):
    """Get corner information."""
    try:
        session = fastf1.get_session(year, event_name, 'R')
        session.load(laps=True, telemetry=True, weather=False, messages=False)
        circuit_info = session.get_circuit_info()
        
        if circuit_info is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "CIRCUIT_NOT_FOUND",
                    "message": f"Circuit information not found for {event_name} {year}",
                    "details": {}
                }
            )
        
        corners = []
        if hasattr(circuit_info, 'corners'):
            corners = dataframe_to_dict_list(circuit_info.corners) if hasattr(circuit_info.corners, 'to_dict') else circuit_info.corners
        
        return ResponseWrapper(
            data=corners,
            meta={
                "year": year,
                "event_name": event_name,
                "count": len(corners) if isinstance(corners, list) else 0
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "CIRCUIT_ERROR",
                "message": f"Could not retrieve corners for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )


@router.get("/circuits/{year}/{event_name}/marshal-sectors", response_model=ResponseWrapper)
def get_marshal_sectors(
    year: int,
    event_name: str
):
    """Get marshal sector information."""
    try:
        session = fastf1.get_session(year, event_name, 'R')
        session.load(laps=True, telemetry=True, weather=False, messages=False)
        circuit_info = session.get_circuit_info()
        
        if circuit_info is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "code": "CIRCUIT_NOT_FOUND",
                    "message": f"Circuit information not found for {event_name} {year}",
                    "details": {}
                }
            )
        
        marshal_sectors = []
        if hasattr(circuit_info, 'marshal_sectors'):
            marshal_sectors = dataframe_to_dict_list(circuit_info.marshal_sectors) if hasattr(circuit_info.marshal_sectors, 'to_dict') else circuit_info.marshal_sectors
        
        return ResponseWrapper(
            data=marshal_sectors,
            meta={
                "year": year,
                "event_name": event_name,
                "count": len(marshal_sectors) if isinstance(marshal_sectors, list) else 0
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "CIRCUIT_ERROR",
                "message": f"Could not retrieve marshal sectors for {event_name} {year}",
                "details": {"error": str(e)}
            }
        )

