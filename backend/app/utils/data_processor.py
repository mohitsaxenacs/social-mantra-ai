from typing import Dict, List, Any, Optional
import logging
from .api_helpers import safe_int

logger = logging.getLogger(__name__)

def process_video_metrics(videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process raw video data to extract metrics.
    
    All metrics are based strictly on real data from the YouTube API.
    No hardcoded values or simulations are used.
    """
    processed_videos = []
    
    for video in videos:
        try:
            snippet = video.get('snippet', {})
            statistics = video.get('statistics', {})
            content_details = video.get('contentDetails', {})
            
            # Use safe_int to handle missing data transparently
            views = safe_int(statistics.get('viewCount'))
            likes = safe_int(statistics.get('likeCount'))
            comments = safe_int(statistics.get('commentCount'))
            
            # Calculate engagement rate only if we have valid view data
            engagement_rate = None
            if views is not None and views > 0:
                # Calculate engagement only if we have valid likes and comments
                if likes is not None and comments is not None:
                    engagement_rate = ((likes + comments) / views) * 100
                
            processed_videos.append({
                'id': video.get('id', ''),
                'title': snippet.get('title', 'Unknown'),
                'channel_id': snippet.get('channelId', ''),
                'channel_title': snippet.get('channelTitle', 'Unknown'),
                'category_id': snippet.get('categoryId', '0'),
                'views': views,
                'likes': likes,
                'comments': comments,
                'engagement_rate': engagement_rate,
                'published_at': snippet.get('publishedAt', ''),
                'thumbnail': snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
            })
        except Exception as e:
            logger.error(f"Error processing video metrics: {str(e)}")
            continue
            
    return processed_videos

def aggregate_category_metrics(videos: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Aggregate metrics by category.
    
    Analyzes videos to extract category-level metrics for niche research.
    """
    categories = {}
    
    for video in videos:
        category_id = video.get('category_id', '0')
        
        if category_id not in categories:
            categories[category_id] = {
                'videos': [],
                'total_views': 0,
                'total_engagement': 0,
                'video_count': 0,
                'views_by_video': []
            }
            
        # Add video to category collection
        categories[category_id]['videos'].append(video)
        
        # Sum up metrics, being careful with None values
        views = video.get('views')
        if views is not None:
            categories[category_id]['total_views'] += views
            categories[category_id]['views_by_video'].append(views)
            
        engagement = video.get('engagement_rate')
        if engagement is not None:
            categories[category_id]['total_engagement'] += engagement
            
        categories[category_id]['video_count'] += 1
        
    # Calculate averages and variances for each category
    for category_id, data in categories.items():
        video_count = data['video_count']
        if video_count > 0:
            # Calculate average views
            if data['total_views'] > 0:
                data['avg_views'] = data['total_views'] / video_count
            else:
                data['avg_views'] = None
                
            # Calculate average engagement
            if 'total_engagement' in data and data['total_engagement'] > 0:
                data['avg_engagement'] = data['total_engagement'] / video_count
            else:
                data['avg_engagement'] = None
                
            # Calculate competition metrics based on view distribution
            views_list = data['views_by_video']
            if views_list:
                # Standard deviation of views indicates competition level
                mean = sum(views_list) / len(views_list)
                variance = sum((x - mean) ** 2 for x in views_list) / len(views_list)
                data['view_variance'] = variance
                
                # Calculate the Gini coefficient to measure view concentration
                # High Gini = few videos dominate views = high competition
                sorted_views = sorted(views_list)
                n = len(sorted_views)
                if n > 1 and sum(sorted_views) > 0:
                    cumulative_views = [sum(sorted_views[:i+1]) for i in range(n)]
                    # Calculate Gini coefficient
                    area_under_lorenz = sum(cumulative_views) / (cumulative_views[-1] * n)
                    data['gini_coefficient'] = 1 - 2 * area_under_lorenz
                else:
                    data['gini_coefficient'] = 0
            
    return categories

def calculate_category_scores(categories: Dict[str, Dict[str, Any]], category_names: Dict[str, str]) -> List[Dict[str, Any]]:
    """Calculate niche scores based on views, engagement, and competition.
    
    Implements sophisticated scoring algorithm that balances traffic potential 
    with competition levels.
    """
    niches = []
    
    # Find max values for normalization
    max_views = 1  # Default to 1 to avoid division by zero
    valid_view_values = [c.get('avg_views', 0) for c in categories.values() if c.get('avg_views') is not None]
    if valid_view_values:
        max_views = max(valid_view_values)
    
    for category_id, data in categories.items():
        # Skip categories with insufficient data
        if data['video_count'] < 3:
            continue
            
        # Get average views, handling None values
        avg_views = data.get('avg_views')
        if avg_views is None:
            traffic_score = None
        else:
            # Calculate traffic score (normalized views on a 0-100 scale)
            traffic_score = min((avg_views / max_views) * 100, 100)
        
        # Calculate competition score based on multiple factors
        competition_score = None
        
        # 1. Number of videos (more videos = more competition)
        video_count_factor = min(data['video_count'] * 2, 100)
        
        # 2. Gini coefficient (more unequal distribution = more competition)
        gini_factor = data.get('gini_coefficient', 0) * 100
        
        # 3. View variance (higher variance = more established players)
        variance_factor = 0
        if data.get('view_variance') is not None and data.get('avg_views') is not None:
            # Coefficient of variation (normalized variance)
            if data['avg_views'] > 0:
                cv = (data['view_variance'] ** 0.5) / data['avg_views']
                variance_factor = min(cv * 25, 100)  # Scale and cap
        
        # Combine competition factors
        if video_count_factor is not None:
            # Weight the factors
            competition_score = (
                (video_count_factor * 0.4) +  # 40% weight to video count
                (gini_factor * 0.4) +        # 40% weight to view concentration
                (variance_factor * 0.2)      # 20% weight to view variance
            )
        
        # Calculate opportunity score only if we have both traffic and competition
        opportunity_score = None
        if traffic_score is not None and competition_score is not None:
            # High traffic + low competition = good opportunity
            opportunity_score = (traffic_score * 0.6) + ((100 - competition_score) * 0.4)
        
        # Get category name, defaulting to category ID if name not available
        name = category_names.get(category_id, f"Category {category_id}")
        
        niches.append({
            'category_id': category_id,
            'name': name,
            'niche_name': name,  # For backwards compatibility
            'avg_views': avg_views,
            'engagement': data.get('avg_engagement'),
            'competition': competition_score,
            'traffic_potential': traffic_score,
            'score': opportunity_score,
            'video_count': data['video_count'],
            'view_concentration': data.get('gini_coefficient'),
            'data_quality': 'high' if data['video_count'] >= 10 else 'medium' if data['video_count'] >= 5 else 'low'
        })
        
    # Sort by opportunity score (or by traffic if score is not available)
    niches = sorted(niches, key=lambda x: (x['score'] if x['score'] is not None else 0), reverse=True)
    return niches

def format_views(views: Optional[int]) -> str:
    """Format view counts for display.
    
    Returns 'N/A' for None values to be transparent about missing data.
    """
    if views is None:
        return 'N/A'
    
    if views >= 1000000:
        return f"{views/1000000:.1f}M"
    elif views >= 1000:
        return f"{views/1000:.1f}K"
    else:
        return str(views)
