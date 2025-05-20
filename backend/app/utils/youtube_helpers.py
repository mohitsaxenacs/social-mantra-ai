from typing import Dict, List, Any, Callable, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

from .api_helpers import make_youtube_request, safe_int

logger = logging.getLogger(__name__)

# YouTube API Category names mapping
CATEGORY_NAMES = {
    "1": "Film & Animation",
    "2": "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "18": "Short Movies",
    "19": "Travel & Events",
    "20": "Gaming",
    "21": "Videoblogging",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "Howto & Style",
    "27": "Education",
    "28": "Science & Technology",
    "29": "Nonprofits & Activism",
    "30": "Movies",
    "31": "Anime/Animation",
    "32": "Action/Adventure",
    "33": "Classics",
    "34": "Comedy",
    "35": "Documentary",
    "36": "Drama",
    "37": "Family",
    "38": "Foreign",
    "39": "Horror",
    "40": "Sci-Fi/Fantasy",
    "41": "Thriller",
    "42": "Shorts",
    "43": "Shows",
    "44": "Trailers",
}

def get_youtube_client(api_key: str):
    """Create and return a YouTube client using the provided API key."""
    try:
        return build('youtube', 'v3', developerKey=api_key, cache_discovery=False)
    except Exception as e:
        logger.error(f"Error creating YouTube client: {e}")
        raise Exception(f"Failed to create YouTube client: {str(e)}")

def get_trending_videos(api_key: str, region_code: str = 'US', max_results: int = 50) -> List[Dict[str, Any]]:
    """Fetch trending videos from the YouTube API.
    
    Args:
        api_key: YouTube API key
        region_code: 2-letter country code (ISO 3166-1 alpha-2)
        max_results: Maximum number of results to return
        
    Returns:
        List of trending video data
    """
    youtube = get_youtube_client(api_key)
    
    try:
        # Define the request function
        def request_func():
            return youtube.videos().list(
                part='snippet,contentDetails,statistics',
                chart='mostPopular',
                regionCode=region_code,
                maxResults=max_results
            ).execute()
        
        # Make the request with retry logic
        response = make_youtube_request(request_func)
        
        if 'items' not in response:
            logger.warning("No items found in trending videos response")
            return []
            
        return response['items']
        
    except Exception as e:
        logger.error(f"Error fetching trending videos: {e}")
        raise Exception(f"Failed to fetch trending videos: {str(e)}")

def search_videos(api_key: str, query: str, region_code: str = 'US', max_results: int = 50) -> List[Dict[str, Any]]:
    """Search for videos on YouTube.
    
    Args:
        api_key: YouTube API key
        query: Search query
        region_code: 2-letter country code (ISO 3166-1 alpha-2)
        max_results: Maximum number of results to return
        
    Returns:
        List of video search results with details
    """
    youtube = get_youtube_client(api_key)
    video_ids = []
    
    try:
        # First search for video IDs only (more efficient)
        def search_request():
            return youtube.search().list(
                part='id',
                q=query,
                type='video',
                videoEmbeddable='true',
                regionCode=region_code,
                relevanceLanguage='en',
                maxResults=max_results
            ).execute()
        
        search_response = make_youtube_request(search_request)
        
        if 'items' not in search_response:
            logger.warning(f"No items found for query: {query}")
            return []
            
        # Extract video IDs
        for item in search_response['items']:
            if 'videoId' in item.get('id', {}):
                video_ids.append(item['id']['videoId'])
                
        if not video_ids:
            logger.warning(f"No valid video IDs found for query: {query}")
            return []
            
        # Get detailed information for each video ID
        def video_details_request():
            return youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(video_ids)
            ).execute()
            
        video_response = make_youtube_request(video_details_request)
        
        if 'items' not in video_response:
            logger.warning(f"No video details found for IDs: {video_ids}")
            return []
            
        return video_response['items']
        
    except Exception as e:
        logger.error(f"Error searching videos: {e}")
        raise Exception(f"Failed to search videos: {str(e)}")

def get_video_categories(api_key: str, region_code: str = 'US') -> Dict[str, str]:
    """Fetch video categories from the YouTube API.
    
    If the API request fails, fall back to the predefined category names.
    
    Args:
        api_key: YouTube API key
        region_code: 2-letter country code (ISO 3166-1 alpha-2)
        
    Returns:
        Dictionary mapping category IDs to names
    """
    youtube = get_youtube_client(api_key)
    
    try:
        # Define the request function
        def request_func():
            return youtube.videoCategories().list(
                part='snippet',
                regionCode=region_code
            ).execute()
        
        # Make the request with retry logic
        response = make_youtube_request(request_func)
        
        categories = {}
        if 'items' in response:
            for item in response['items']:
                category_id = item.get('id')
                if category_id:
                    categories[category_id] = item.get('snippet', {}).get('title', f"Category {category_id}")
        
        # Merge with predefined categories for any missing IDs
        combined_categories = {**CATEGORY_NAMES, **categories}
        return combined_categories
        
    except Exception as e:
        logger.error(f"Error fetching video categories, using defaults: {e}")
        # Return predefined categories as fallback
        return CATEGORY_NAMES
        
def get_channel_info(api_key: str, channel_id: str) -> Dict[str, Any]:
    """Get information about a YouTube channel.
    
    Args:
        api_key: YouTube API key
        channel_id: YouTube channel ID
        
    Returns:
        Dictionary with channel information
    """
    youtube = get_youtube_client(api_key)
    
    try:
        # Define the request function
        def request_func():
            return youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            ).execute()
        
        # Make the request with retry logic
        response = make_youtube_request(request_func)
        
        if 'items' not in response or not response['items']:
            logger.warning(f"No channel found for ID: {channel_id}")
            return {}
            
        channel = response['items'][0]
        snippet = channel.get('snippet', {})
        statistics = channel.get('statistics', {})
        
        return {
            'id': channel.get('id', ''),
            'title': snippet.get('title', 'Unknown'),
            'description': snippet.get('description', ''),
            'custom_url': snippet.get('customUrl', ''),
            'published_at': snippet.get('publishedAt', ''),
            'thumbnail': snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
            'subscriber_count': safe_int(statistics.get('subscriberCount')),
            'video_count': safe_int(statistics.get('videoCount')),
            'view_count': safe_int(statistics.get('viewCount'))
        }
        
    except Exception as e:
        logger.error(f"Error fetching channel info: {e}")
        raise Exception(f"Failed to fetch channel info: {str(e)}")

def get_ai_friendly_niches() -> List[Dict[str, Any]]:
    """Get a list of AI-friendly niches that work well for faceless channels.
    
    These are specifically selected niches that can be easily automated with AI
    and don't require real-world footage or personal appearances.
    
    Returns:
        List of AI-friendly niches with descriptions
    """
    return [
        {
            "name": "Data Storytelling",
            "description": "Videos that tell stories through data visualization, charts, and graphs.",
            "ai_advantage": "AI can easily generate data visualizations and narrative scripts.",
            "example_topics": ["Trending Statistics", "Historical Data Analysis", "Visual Data Comparisons"]
        },
        {
            "name": "Historical Event Animations",
            "description": "Animated retellings of historical events, battles, and milestones.",
            "ai_advantage": "AI can generate historical images, maps, and animation sequences.",
            "example_topics": ["Ancient Civilizations", "Famous Battles", "Historical Mysteries"]
        },
        {
            "name": "Educational Explainers",
            "description": "Videos that explain complex topics using simple animations and graphics.",
            "ai_advantage": "AI excels at generating educational scripts and simple explanatory visuals.",
            "example_topics": ["Science Concepts", "Math Explainers", "Technology Breakdowns"]
        },
        {
            "name": "Fact Compilation Videos",
            "description": "Collections of interesting facts on specific topics with supporting visuals.",
            "ai_advantage": "AI can research facts and generate appropriate imagery for each point.",
            "example_topics": ["Amazing Animal Facts", "Space Discoveries", "Historical Coincidences"]
        },
        {
            "name": "AI Art Showcases",
            "description": "Videos featuring AI-generated artwork with narration about the themes or concepts.",
            "ai_advantage": "AI directly generates the main visual content with high uniqueness.",
            "example_topics": ["Fantasy Landscapes", "Character Designs", "Art Style Transformations"]
        },
        {
            "name": "Ambient Soundscapes",
            "description": "Relaxing videos with AI-generated landscapes and soundscapes for study, sleep, or relaxation.",
            "ai_advantage": "AI can create endless variations of scenes and accompanying audio.",
            "example_topics": ["Study Ambience", "Sleep Soundscapes", "Meditation Backgrounds"]
        },
        {
            "name": "Quote Collections",
            "description": "Inspirational or thematic quotes with supporting visuals and music.",
            "ai_advantage": "AI can generate visuals for each quote and compile them seamlessly.",
            "example_topics": ["Motivational Quotes", "Famous Author Quotes", "Life Advice"]
        },
        {
            "name": "Digital Storytelling",
            "description": "Short stories or narratives illustrated with AI-generated scenes.",
            "ai_advantage": "AI can create story scripts and matching visual representations.",
            "example_topics": ["Short Tales", "Modern Fables", "Sci-Fi Stories"]
        },
        {
            "name": "News Summaries",
            "description": "Summaries of current events with supporting graphics and data visualization.",
            "ai_advantage": "AI can compile news from sources and create explanatory graphics.",
            "example_topics": ["Daily News Roundup", "Weekly Tech News", "Sports Highlights"]
        },
        {
            "name": "Top 10 Lists",
            "description": "Countdown-style videos on various topics with explanations and visuals for each item.",
            "ai_advantage": "AI can research topics and generate appropriate visuals for each list item.",
            "example_topics": ["Amazing Discoveries", "Strange Natural Phenomena", "Historical Mysteries"]
        }
    ]
