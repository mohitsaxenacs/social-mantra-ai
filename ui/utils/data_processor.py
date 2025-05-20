"""Data processing utilities for YouTube video and category data."""
from datetime import datetime, timedelta
import math
from typing import Dict, List, Optional, Any

# Import from the same package using absolute imports
from ui.utils.api_helpers import safe_int, safe_parse_duration
from ui.utils.config import API_CONFIG, REGIONS, DEFAULT_REGION

def process_video_metrics(video: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and process metrics from a video."""
    snippet = video.get('snippet', {})
    stats = video.get('statistics', {})
    content_details = video.get('contentDetails', {})
    
    # Safely parse metrics
    metrics = {
        'views': safe_int(stats.get('viewCount', 0)),
        'likes': safe_int(stats.get('likeCount', 0)),
        'comments': safe_int(stats.get('commentCount', 0)),
        'duration': safe_parse_duration(content_details.get('duration', 'PT0S')),
        'published_at': snippet.get('publishedAt'),
        'channel_id': snippet.get('channelId'),
        'category_id': snippet.get('categoryId')
    }
    
    # Calculate engagement rate
    if metrics['views'] > 0:
        metrics['engagement_rate'] = (
            (metrics['likes'] + metrics['comments']) / metrics['views']
        ) * 100
    else:
        metrics['engagement_rate'] = 0
    
    return metrics

def aggregate_category_metrics(videos: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Aggregate metrics by category."""
    category_metrics = {}
    
    for video in videos:
        metrics = process_video_metrics(video)
        category_id = metrics['category_id']
        
        if not category_id:
            continue
            
        if category_id not in category_metrics:
            category_metrics[category_id] = {
                'videos': 0,
                'total_views': 0,
                'total_likes': 0,
                'total_comments': 0,
                'total_duration': 0,
                'publish_dates': [],
                'channel_ids': set(),
                'engagement_rates': []
            }
        
        # Update metrics
        cat_metrics = category_metrics[category_id]
        cat_metrics['videos'] += 1
        cat_metrics['total_views'] += metrics['views']
        cat_metrics['total_likes'] += metrics['likes']
        cat_metrics['total_comments'] += metrics['comments']
        cat_metrics['total_duration'] += metrics['duration']
        cat_metrics['engagement_rates'].append(metrics['engagement_rate'])
        
        if metrics['published_at']:
            cat_metrics['publish_dates'].append(metrics['published_at'])
        if metrics['channel_id']:
            cat_metrics['channel_ids'].add(metrics['channel_id'])
    
    return category_metrics

def calculate_category_scores(category_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Calculate scores for each category."""
    now = datetime.utcnow()
    results = []
    
    for category_id, metrics in category_metrics.items():
        if metrics['videos'] < 3:  # Skip categories with too few videos
            continue
            
        # Calculate averages
        avg_views = metrics['total_views'] / metrics['videos']
        avg_engagement = sum(metrics['engagement_rates']) / len(metrics['engagement_rates'])
        
        # Calculate recency score
        recent_count = 0
        for date_str in metrics['publish_dates']:
            try:
                publish_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                if (now - publish_date) < timedelta(days=30):
                    recent_count += 1
            except (ValueError, TypeError):
                continue
        
        recency_score = (recent_count / metrics['videos']) * 100 if metrics['videos'] > 0 else 0
        
        # Calculate competition score (simplified for now)
        competition = min(100, 15 * math.log10(avg_views / 1000)) if avg_views > 0 else 50
        
        # Calculate overall score (0-100)
        view_score = min(1.0, avg_views / 100000) * 30
        engagement_score = min(1.0, avg_engagement / 20) * 30
        recency_score_normalized = (recency_score / 100) * 20
        competition_score = (1 - (competition / 100)) * 20
        
        overall_score = view_score + engagement_score + recency_score_normalized + competition_score
        
        # Always store category_id as a string to avoid type mismatches
        str_category_id = str(category_id)
        
        results.append({
            'category_id': str_category_id,
            'name': f"Category {str_category_id}",  # Will be updated with actual names later
            'niche_name': f"Category {str_category_id}",  # Add this explicitly for consistent access
            'avg_views': avg_views,
            'engagement': avg_engagement,
            'competition': competition,
            'recency_score': recency_score,
            'score': overall_score,
            'video_count': metrics['videos'],
            'unique_channels': len(metrics['channel_ids'])
        })
    
    return sorted(results, key=lambda x: x['score'], reverse=True)

def format_views(views):
    """Format view count in a human-readable format (K, M, etc)."""
    if isinstance(views, str):
        return views
    
    try:
        if views >= 1_000_000:
            return f"{views/1_000_000:.1f}M"
        elif views >= 1_000:
            return f"{views/1_000:.1f}K"
        return str(views)
    except (TypeError, ValueError):
        return "N/A"

def update_category_names(categories: List[Dict[str, Any]], youtube, region_code: str) -> List[Dict[str, Any]]:
    """Update category names using YouTube API."""
    if not categories:
        return []
    
    try:
        # Get category details
        category_ids = [cat['category_id'] for cat in categories]
        response = youtube.videoCategories().list(
            part='snippet',
            id=','.join(category_ids),
            regionCode=region_code
        ).execute()
        
        # Create mapping of category IDs to names
        category_map = {
            item['id']: item['snippet']['title']
            for item in response.get('items', [])
        }
        
        # Update category names
        for category in categories:
            category['name'] = category_map.get(category['category_id'], f"Category {category['category_id']}")
            
    except Exception as e:
        print(f"Warning: Could not fetch category names: {e}")
        # If we can't get the names, use generic ones
        for category in categories:
            category['name'] = f"Category {category['category_id']}"
    
    return categories
