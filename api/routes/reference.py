from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Optional
import fastf1.plotting
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/reference/teams", response_model=Dict[str, str])
async def get_team_colors():
    """
    Get a mapping of team names to their hex color codes.
    """
    try:
        # Ensure matplotlib is setup for fastf1
        fastf1.plotting.setup_mpl(misc_mpl_mods=False)
        
        teams = fastf1.plotting.list_team_names()
        team_colors = {}
        
        for team in teams:
            try:
                color = fastf1.plotting.get_team_color(team, session=None)
                team_colors[team] = color
            except:
                continue
                
        return team_colors
    except Exception as e:
        logger.error(f"Error fetching team colors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch team colors: {str(e)}")

@router.get("/reference/drivers", response_model=Dict[str, str])
async def get_driver_colors():
    """
    Get a mapping of driver names/abbreviations to their hex color codes.
    """
    try:
        # Ensure matplotlib is setup for fastf1
        fastf1.plotting.setup_mpl(misc_mpl_mods=False)
        
        drivers = fastf1.plotting.list_driver_names()
        driver_colors = {}
        
        for driver in drivers:
            try:
                color = fastf1.plotting.get_driver_color(driver, session=None)
                driver_colors[driver] = color
            except:
                continue
                
        return driver_colors
    except Exception as e:
        logger.error(f"Error fetching driver colors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch driver colors: {str(e)}")

@router.get("/reference/compounds", response_model=Dict[str, str])
async def get_compound_colors():
    """
    Get a mapping of tyre compounds to their hex color codes.
    """
    try:
        # Ensure matplotlib is setup for fastf1
        fastf1.plotting.setup_mpl(misc_mpl_mods=False)
        
        # fastf1.plotting.get_compound_mapping returns a dictionary of compound -> color
        # Note: The API might have changed in recent versions, checking available methods
        if hasattr(fastf1.plotting, 'get_compound_mapping'):
            return fastf1.plotting.get_compound_mapping(session=None)
        else:
            # Fallback or manual mapping if needed
            compounds = ["SOFT", "MEDIUM", "HARD", "INTERMEDIATE", "WET"]
            compound_colors = {}
            for compound in compounds:
                try:
                    color = fastf1.plotting.get_compound_color(compound, session=None)
                    compound_colors[compound] = color
                except:
                    continue
            return compound_colors
            
    except Exception as e:
        logger.error(f"Error fetching compound colors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch compound colors: {str(e)}")
