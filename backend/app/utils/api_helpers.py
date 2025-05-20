from typing import Callable, Any, Dict, Optional
import time
import logging

logger = logging.getLogger(__name__)

def make_youtube_request(request_func: Callable, max_retries: int = 3, retry_delay: int = 1) -> Dict[str, Any]:
    """Execute a YouTube API request with retry logic.
    
    Args:
        request_func: Function that executes the API request
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        API response as a dictionary
    """
    retry_count = 0
    last_error = None
    
    while retry_count < max_retries:
        try:
            response = request_func()
            return response
        except Exception as e:
            last_error = e
            error_message = str(e).lower()
            
            # Check for specific errors
            if "quota" in error_message:
                logger.error("YouTube API quota exceeded")
                raise Exception("YouTube API quota exceeded. Please try again tomorrow or use a different API key.")
            elif "keyinvalid" in error_message:
                logger.error("Invalid YouTube API key")
                raise Exception("Invalid YouTube API key. Please check your API key and try again.")
            elif "disabled" in error_message:
                logger.error("YouTube API is disabled")
                raise Exception("The YouTube Data API v3 is not enabled for this API key. Please enable it in the Google Cloud Console.")
            
            # Increment retry count and delay
            retry_count += 1
            logger.warning(f"API request failed, attempt {retry_count}/{max_retries}: {str(e)}")
            time.sleep(retry_delay)
    
    # If we've exhausted all retries, raise the last error
    logger.error(f"API request failed after {max_retries} attempts: {str(last_error)}")
    raise last_error

def safe_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    """Convert value to integer safely.
    
    Returns None instead of a default value if conversion fails,
    to be transparent about missing data.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_parse_duration(duration: str) -> Optional[int]:
    """Parse ISO 8601 duration format to seconds.
    
    Returns None if duration can't be parsed, to be transparent about missing data.
    """
    if not duration:
        return None
        
    seconds = 0
    # Parse PT1H2M3S format (example)
    try:
        if "H" in duration:
            hours = int(duration.split("H")[0].split("T")[1])
            seconds += hours * 3600
            
        if "M" in duration:
            if "H" in duration:
                minutes = int(duration.split("H")[1].split("M")[0])
            else:
                minutes = int(duration.split("T")[1].split("M")[0])
            seconds += minutes * 60
            
        if "S" in duration:
            if "M" in duration:
                s = int(duration.split("M")[1].split("S")[0])
            elif "H" in duration:
                s = int(duration.split("H")[1].split("S")[0])
            else:
                s = int(duration.split("T")[1].split("S")[0])
            seconds += s
            
        return seconds
    except (ValueError, IndexError):
        return None
