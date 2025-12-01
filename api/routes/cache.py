from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import fastf1
import os
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/cache/info", response_model=Dict[str, Any])
async def get_cache_info():
    """
    Get information about the current FastF1 cache.
    """
    cache_dir = os.getenv("FASTF1_CACHE_DIR")
    
    if not cache_dir:
        return {
            "enabled": False,
            "location": None,
            "size_mb": 0
        }
        
    try:
        # Calculate cache size
        total_size = 0
        if os.path.exists(cache_dir):
            for dirpath, dirnames, filenames in os.walk(cache_dir):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
        
        size_mb = round(total_size / (1024 * 1024), 2)
        
        return {
            "enabled": True,
            "location": cache_dir,
            "size_mb": size_mb
        }
    except Exception as e:
        logger.error(f"Error getting cache info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get cache info: {str(e)}")

@router.post("/cache/clear")
async def clear_cache(background_tasks: BackgroundTasks):
    """
    Clear the FastF1 cache.
    """
    cache_dir = os.getenv("FASTF1_CACHE_DIR")
    
    if not cache_dir:
        raise HTTPException(status_code=400, detail="Cache is not enabled or configured.")
        
    if not os.path.exists(cache_dir):
         return {"message": "Cache directory does not exist, nothing to clear."}

    try:
        # We use fastf1's clear_cache if available, or manual deletion
        # fastf1.Cache.clear_cache(cache_dir) # This might not exist in all versions or work as expected
        
        # Manual deletion is safer to ensure it's gone
        shutil.rmtree(cache_dir)
        os.makedirs(cache_dir, exist_ok=True)
        
        # Re-enable cache
        fastf1.Cache.enable_cache(cache_dir)
        
        return {"message": "Cache cleared successfully."}
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")
