from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List, Dict, Any, Optional
import logging

from app.core.config import settings
from app.utils.youtube_helpers import (
    get_trending_videos,
    search_videos,
    get_video_categories,
    get_channel_info,
    get_ai_friendly_niches
)
from app.utils.data_processor import (
    process_video_metrics, 
    aggregate_category_metrics, 
    calculate_category_scores,
    format_views
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/youtube", tags=["YouTube"])

@router.get("/trending-niches")
async def get_trending_niches(
    api_key: str,
    region_code: str = Query(settings.DEFAULT_REGION, description="ISO 3166-1 alpha-2 country code"),
    max_results: int = Query(50, description="Maximum number of videos to analyze", le=100)
) -> Dict[str, Any]:
    """Get trending niches based on popular videos.
    
    Returns niches with traffic, engagement, and competition metrics.
    """
    try:
        # Get trending videos
        trending_videos = get_trending_videos(api_key, region_code, max_results)
        
        # Get video categories
        category_names = get_video_categories(api_key, region_code)
        
        # Process metrics
        processed_videos = process_video_metrics(trending_videos)
        
        # Aggregate by category
        categories = aggregate_category_metrics(processed_videos)
        
        # Calculate niche scores
        niches = calculate_category_scores(categories, category_names)
        
        # Format for display
        formatted_niches = []
        for niche in niches:
            formatted_niches.append({
                **niche,
                "avg_views_formatted": format_views(niche.get("avg_views")),
                "examples": [v for v in processed_videos if v.get("category_id") == niche.get("category_id")][:3]
            })
            
        return {
            "success": True,
            "niches": formatted_niches,
            "total_niches": len(formatted_niches),
            "analyzed_videos": len(processed_videos)
        }
        
    except Exception as e:
        logger.error(f"Error getting trending niches: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/low-competition-niches")
async def get_low_competition_niches(
    api_key: str,
    region_code: str = Query(settings.DEFAULT_REGION, description="ISO 3166-1 alpha-2 country code"),
    max_results: int = Query(50, description="Maximum number of videos to analyze", le=100)
) -> Dict[str, Any]:
    """Get low competition niches based on trending videos.
    
    Analyzes trending videos and ranks niches by lowest competition score.
    """
    try:
        # Get trending videos
        trending_videos = get_trending_videos(api_key, region_code, max_results)
        
        # Get video categories
        category_names = get_video_categories(api_key, region_code)
        
        # Process metrics
        processed_videos = process_video_metrics(trending_videos)
        
        # Aggregate by category
        categories = aggregate_category_metrics(processed_videos)
        
        # Calculate niche scores
        niches = calculate_category_scores(categories, category_names)
        
        # Sort by competition (low to high)
        niches = sorted(
            [n for n in niches if n.get("competition") is not None],
            key=lambda x: x.get("competition", 100)
        )
        
        # Format for display
        formatted_niches = []
        for niche in niches:
            formatted_niches.append({
                **niche,
                "avg_views_formatted": format_views(niche.get("avg_views")),
                "examples": [v for v in processed_videos if v.get("category_id") == niche.get("category_id")][:3]
            })
            
        return {
            "success": True,
            "niches": formatted_niches,
            "total_niches": len(formatted_niches),
            "analyzed_videos": len(processed_videos)
        }
        
    except Exception as e:
        logger.error(f"Error getting low competition niches: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai-friendly-niches")
async def get_ai_friendly_niches() -> Dict[str, Any]:
    """Get AI-friendly niches for faceless content creation.
    
    Returns a list of niches specifically selected for AI automation.
    """
    try:
        niches = get_ai_friendly_niches()
        
        return {
            "success": True,
            "niches": niches,
            "total_niches": len(niches)
        }
        
    except Exception as e:
        logger.error(f"Error getting AI-friendly niches: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search-niche")
async def search_niche(
    api_key: str,
    query: str,
    region_code: str = Query(settings.DEFAULT_REGION, description="ISO 3166-1 alpha-2 country code"),
    max_results: int = Query(30, description="Maximum number of videos to analyze", le=50)
) -> Dict[str, Any]:
    """Analyze a custom niche based on search query.
    
    Searches for videos matching the query and calculates niche metrics.
    """
    try:
        # Search for videos
        videos = search_videos(api_key, query, region_code, max_results)
        
        if not videos:
            return {
                "success": True,
                "message": "No videos found for this query.",
                "niche": None,
                "videos": []
            }
        
        # Process metrics
        processed_videos = process_video_metrics(videos)
        
        # Calculate aggregate metrics
        total_views = 0
        total_engagement = 0
        views_list = []
        
        for video in processed_videos:
            views = video.get("views")
            if views is not None:
                total_views += views
                views_list.append(views)
                
            engagement = video.get("engagement_rate")
            if engagement is not None:
                total_engagement += engagement
        
        video_count = len(processed_videos)
        
        # Calculate averages
        avg_views = total_views / video_count if video_count > 0 else None
        avg_engagement = total_engagement / video_count if video_count > 0 else None
        
        # Calculate competition metrics
        competition_score = None
        if views_list:
            # Standard deviation indicates competition
            mean = sum(views_list) / len(views_list)
            variance = sum((x - mean) ** 2 for x in views_list) / len(views_list) if len(views_list) > 1 else 0
            
            # Calculate normalized metrics
            video_count_factor = min(video_count * 2, 100)
            
            # Gini coefficient for view distribution
            sorted_views = sorted(views_list) 
            n = len(sorted_views)
            if n > 1 and sum(sorted_views) > 0:
                cumulative_views = [sum(sorted_views[:i+1]) for i in range(n)]
                area_under_lorenz = sum(cumulative_views) / (cumulative_views[-1] * n)
                gini = 1 - 2 * area_under_lorenz
            else:
                gini = 0
                
            gini_factor = gini * 100
            
            # Coefficient of variation
            cv = (variance ** 0.5) / mean if mean > 0 else 0
            variance_factor = min(cv * 25, 100)
            
            # Combine factors
            competition_score = (
                (video_count_factor * 0.4) +
                (gini_factor * 0.4) +
                (variance_factor * 0.2)
            )
        
        # Calculate traffic score (normalized to 100)
        max_views_threshold = 5000000  # Threshold for 100% score
        traffic_score = min((avg_views or 0) / max_views_threshold * 100, 100) if avg_views is not None else None
        
        # Calculate opportunity score
        opportunity_score = None
        if traffic_score is not None and competition_score is not None:
            opportunity_score = (traffic_score * 0.6) + ((100 - competition_score) * 0.4)
        
        # Format the niche data
        niche = {
            "name": query,
            "avg_views": avg_views,
            "avg_views_formatted": format_views(avg_views),
            "engagement": avg_engagement,
            "competition": competition_score,
            "traffic_potential": traffic_score,
            "score": opportunity_score,
            "video_count": video_count,
            "data_quality": "high" if video_count >= 10 else "medium" if video_count >= 5 else "low"
        }
        
        return {
            "success": True,
            "niche": niche,
            "videos": processed_videos,
            "analyzed_videos": video_count
        }
        
    except Exception as e:
        logger.error(f"Error analyzing niche: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/channel/{channel_id}")
async def get_channel(
    channel_id: str,
    api_key: str
) -> Dict[str, Any]:
    """Get information about a YouTube channel."""
    try:
        channel_info = get_channel_info(api_key, channel_id)
        
        if not channel_info:
            raise HTTPException(status_code=404, detail=f"Channel with ID {channel_id} not found")
        
        # Format subscriber count
        subscriber_count = channel_info.get("subscriber_count")
        if subscriber_count is not None:
            if subscriber_count >= 1000000:
                formatted_subs = f"{subscriber_count/1000000:.1f}M"
            elif subscriber_count >= 1000:
                formatted_subs = f"{subscriber_count/1000:.1f}K"
            else:
                formatted_subs = str(subscriber_count)
            channel_info["subscriber_count_formatted"] = formatted_subs
        else:
            channel_info["subscriber_count_formatted"] = "N/A"
        
        return {
            "success": True,
            "channel": channel_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting channel info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
