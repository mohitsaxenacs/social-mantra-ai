"""YouTube API specific helper functions."""
from typing import List, Dict, Any, Optional
import googleapiclient.discovery
import os
import json
from datetime import datetime, timedelta

# Use absolute imports
from ui.utils.api_helpers import make_youtube_request
from ui.utils.config import DEFAULT_REGION

def get_trending_videos(youtube, max_results: int, region_code: str = DEFAULT_REGION) -> List[Dict[str, Any]]:
    """Get trending videos with pagination support.
    
    Args:
        youtube: Initialized YouTube API client
        max_results: Maximum number of videos to return
        region_code: ISO 3166-1 alpha-2 country code
        
    Returns:
        List of video dictionaries
    """
    videos = []
    next_page_token = None
    
    try:
        while len(videos) < max_results:
            request = youtube.videos().list(
                part="snippet,statistics,contentDetails,topicDetails",
                chart="mostPopular",
                regionCode=region_code,
                maxResults=min(50, max_results - len(videos)),
                pageToken=next_page_token
            )
            
            print(f"[DEBUG] Making API request with region: {region_code}")
            response = make_youtube_request(request.execute)
            
            if not response:
                print("[DEBUG] No response received from YouTube API")
                break
                
            if 'items' not in response:
                print(f"[DEBUG] No 'items' in response. Full response: {response}")
                break
                
            items = response['items']
            print(f"[DEBUG] Received {len(items)} videos in response")
            
            if not items:
                print("[DEBUG] No videos found in the response")
                break
                
            videos.extend(items)
            print(f"[DEBUG] Total videos collected: {len(videos)}")
            
            if 'nextPageToken' not in response or len(videos) >= max_results:
                break
                
            next_page_token = response['nextPageToken']
            
    except Exception as e:
        print(f"[ERROR] Error in get_trending_videos: {str(e)}")
        print(f"[ERROR] Region code: {region_code}, Max results: {max_results}")
        import traceback
        traceback.print_exc()
        
    print(f"[DEBUG] Returning {len(videos)} videos")
    return videos[:max_results]

def get_category_details(youtube, category_ids: List[str], region_code: str = DEFAULT_REGION) -> Dict[str, str]:
    """Get category names for the given category IDs with persistent storage.
    
    Args:
        youtube: Initialized YouTube API client
        category_ids: List of category IDs to look up
        region_code: ISO 3166-1 alpha-2 country code
        
    Returns:
        Dictionary mapping category IDs to their names
    """
    # Standard YouTube category ID to name mapping as fallback
    STANDARD_CATEGORY_MAP = {
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
        "44": "Trailers"
    }
    
    if not category_ids:
        return {}
    
    # Convert all IDs to strings for consistency
    str_category_ids = [str(cid) for cid in category_ids]
    print(f"[DEBUG] Processing category IDs: {str_category_ids}")
    
    # Path for storing category mappings
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    category_cache_file = os.path.join(cache_dir, f'category_map_{region_code}.json')
    
    # Check if we have a recent cached mapping
    cached_map = {}
    cache_is_fresh = False
    
    try:
        if os.path.exists(category_cache_file):
            # Check if cache is recent (less than 1 day old)
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(category_cache_file))
            if datetime.now() - file_mod_time < timedelta(days=1):
                with open(category_cache_file, 'r') as f:
                    cached_map = json.load(f)
                print(f"[DEBUG] Loaded {len(cached_map)} categories from cache: {category_cache_file}")
                cache_is_fresh = True
            else:
                print(f"[DEBUG] Cache file exists but is outdated: {category_cache_file}")
    except Exception as e:
        print(f"[WARNING] Error reading category cache: {str(e)}")
    
    # If we have all the categories we need in the cache, use those
    missing_ids = [cid for cid in str_category_ids if cid not in cached_map]
    if cache_is_fresh and not missing_ids:
        print(f"[DEBUG] Using cached category map for all {len(str_category_ids)} categories")
        return {cid: cached_map[cid] for cid in str_category_ids if cid in cached_map}
    
    # We need to fetch from the API
    try:
        api_map = {}
        
        # Only request IDs we don't already have cached
        if missing_ids:
            print(f"[DEBUG] Requesting {len(missing_ids)} categories from API: {missing_ids}")
            response = youtube.videoCategories().list(
                part='snippet',
                id=','.join(missing_ids),
                regionCode=region_code
            ).execute()
            
            # Add new mappings to our cache
            for item in response.get('items', []):
                category_id = str(item['id'])
                category_name = item['snippet']['title']
                api_map[category_id] = category_name
                cached_map[category_id] = category_name  # Update the cache
                print(f"[DEBUG] API provided name for ID {category_id}: '{category_name}'")
        
        # Save the updated cache
        try:
            with open(category_cache_file, 'w') as f:
                json.dump(cached_map, f)
            print(f"[DEBUG] Saved updated category map to {category_cache_file}")
        except Exception as e:
            print(f"[WARNING] Could not save category cache: {str(e)}")
    except Exception as e:
        print(f"[ERROR] Failed to fetch categories from API: {str(e)}")
    
    # Create the final mapping, with fallbacks
    result_map = {}
    for category_id in str_category_ids:
        # Try cache first (which now includes any new API results)
        if category_id in cached_map:
            result_map[category_id] = cached_map[category_id]
        # Then try API results directly
        elif category_id in api_map:
            result_map[category_id] = api_map[category_id]
        # Then try standard mapping
        elif category_id in STANDARD_CATEGORY_MAP:
            result_map[category_id] = STANDARD_CATEGORY_MAP[category_id]
        # Finally use a generic fallback
        else:
            result_map[category_id] = f"Category {category_id}"
    
    print(f"[DEBUG] Final category map: {result_map}")
    return result_map

def get_channel_metrics(youtube, channel_ids: List[str]) -> Dict[str, Dict[str, int]]:
    """Get metrics for multiple channels.
    
    Args:
        youtube: Initialized YouTube API client
        channel_ids: List of channel IDs to look up
        
    Returns:
        Dictionary mapping channel IDs to their metrics
    """
    if not channel_ids:
        return {}
    
    try:
        response = youtube.channels().list(
            part='statistics',
            id=','.join(channel_ids[:50])  # API limit is 50 channels per request
        ).execute()
        
        return {
            item['id']: {
                'subscribers': int(item['statistics'].get('subscriberCount', 0)),
                'videos': int(item['statistics'].get('videoCount', 0)),
                'views': int(item['statistics'].get('viewCount', 0))
            }
            for item in response.get('items', [])
            if 'statistics' in item
        }
    except Exception as e:
        print(f"Error fetching channel metrics: {e}")
        return {}

def get_category_examples(youtube, category_id: str, region_code: str = DEFAULT_REGION, max_examples: int = 5) -> List[Dict[str, str]]:
    """Get example channels and videos for a specific category.
    
    Args:
        youtube: Initialized YouTube API client
        category_id: The category ID to get examples for
        region_code: ISO 3166-1 alpha-2 country code
        max_examples: Maximum number of examples to return
        
    Returns:
        List of dictionaries with channel and video information
    """
    try:
        # Get trending videos for this category
        search_request = youtube.search().list(
            part="snippet",
            type="video",
            videoCategoryId=category_id,
            regionCode=region_code,
            maxResults=max_examples * 2,  # Request more to ensure we get enough
            relevanceLanguage="en",  # Prefer English content
            order="viewCount"  # Sort by view count to get popular content
        )
        
        response = make_youtube_request(search_request.execute)
        if not response or 'items' not in response:
            print(f"[WARNING] No search results for category {category_id}")
            return []
            
        results = []
        seen_channels = set()
        
        for item in response.get('items', []):
            if len(results) >= max_examples:
                break
                
            snippet = item.get('snippet', {})
            video_id = item.get('id', {}).get('videoId')
            channel_id = snippet.get('channelId')
            channel_title = snippet.get('channelTitle', 'Unknown Channel')
            video_title = snippet.get('title', 'Unknown Video')
            
            # Skip duplicates from the same channel
            if channel_id in seen_channels:
                continue
                
            if channel_id and video_id:
                seen_channels.add(channel_id)
                
                results.append({
                    'channel_id': channel_id,
                    'channel_name': channel_title,
                    'channel_url': f"https://www.youtube.com/channel/{channel_id}",
                    'video_id': video_id,
                    'video_title': video_title,
                    'video_url': f"https://www.youtube.com/watch?v={video_id}",
                    'thumbnail_url': snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
                })
        
        print(f"[DEBUG] Found {len(results)} examples for category {category_id}")
        return results
        
    except Exception as e:
        print(f"[ERROR] Failed to get category examples: {str(e)}")
        return []
