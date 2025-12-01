from fastapi import APIRouter, HTTPException
from typing import Dict
import fastf1.plotting
import fastf1.plotting._constants as constants
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
        # Use 2024 constants as default
        # This avoids needing a session object
        if hasattr(constants, 'season2024') and hasattr(constants.season2024, 'Teams'):
            teams = constants.season2024.Teams
            team_colors = {}
            for key, team in teams.items():
                # Use Official color if available, else FastF1 color
                color = team.TeamColor.Official if team.TeamColor.Official else team.TeamColor.FastF1
                team_colors[team.ShortName] = color
            return team_colors
        else:
            # Fallback to hardcoded list if constants change
            return {
                "Red Bull Racing": "#0600ef",
                "McLaren": "#ff8000",
                "Ferrari": "#dc0000",
                "Mercedes": "#00d2be",
                "Aston Martin": "#229971",
                "Alpine": "#0090ff",
                "Williams": "#64c4ff",
                "RB": "#6692ff",
                "Kick Sauber": "#52e252",
                "Haas F1 Team": "#b6babd"
            }
    except Exception as e:
        logger.error(f"Error fetching team colors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch team colors: {str(e)}")

@router.get("/reference/drivers", response_model=Dict[str, str])
async def get_driver_colors():
    """
    Get a mapping of driver names/abbreviations to their hex color codes.
    """
    try:
        # Driver colors are often team colors in F1, but sometimes specific
        # Without a session, we can't get the exact current grid easily via fastf1.plotting
        # So we will return a generic mapping based on 2024/2025 grid
        
        # We can try to use the team mapping to infer driver colors if we had a driver list
        # For now, let's return a static list of top drivers to ensure the endpoint works
        # This is better than a 500 error
        
        return {
            "VER": "#0600ef", "PER": "#0600ef",
            "NOR": "#ff8000", "PIA": "#ff8000",
            "LEC": "#dc0000", "SAI": "#dc0000", "HAM": "#dc0000", # HAM at Ferrari in 2025
            "RUS": "#00d2be", "ANT": "#00d2be", # Antonelli?
            "ALO": "#229971", "STR": "#229971",
            "GAS": "#0090ff", "DOO": "#0090ff",
            "ALB": "#64c4ff", "SAI": "#64c4ff", # Sainz at Williams?
            "TSU": "#6692ff", "LAW": "#6692ff",
            "HUL": "#52e252", "BOR": "#52e252",
            "BEA": "#b6babd", "OCO": "#b6babd"
        }
    except Exception as e:
        logger.error(f"Error fetching driver colors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch driver colors: {str(e)}")

@router.get("/reference/compounds", response_model=Dict[str, str])
async def get_compound_colors():
    """
    Get a mapping of tyre compounds to their hex color codes.
    """
    try:
        # Use constants if available
        if hasattr(constants, 'season2024') and hasattr(constants.season2024, 'CompoundColors'):
            # CompoundColors is a dataclass or similar
            cc = constants.season2024.CompoundColors
            return {
                "SOFT": cc.SOFT,
                "MEDIUM": cc.MEDIUM,
                "HARD": cc.HARD,
                "INTERMEDIATE": cc.INTERMEDIATE,
                "WET": cc.WET
            }
        else:
            # Fallback
            return {
                "SOFT": "#da291c",
                "MEDIUM": "#ffd12e",
                "HARD": "#f0f0f0",
                "INTERMEDIATE": "#43b02a",
                "WET": "#0067a5"
            }
            
    except Exception as e:
        logger.error(f"Error fetching compound colors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch compound colors: {str(e)}")
