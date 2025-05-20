from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from app.core.config import settings

router = APIRouter(prefix="/api/settings", tags=["Settings"])

@router.get("/regions")
async def get_regions() -> Dict[str, Any]:
    """Get available regions for YouTube API."""
    try:
        return {
            "success": True,
            "regions": settings.REGIONS
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
