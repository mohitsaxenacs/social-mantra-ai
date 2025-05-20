"""YouTube API helper functions with retry and error handling."""
import time
import logging
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import googleapiclient.errors
from ui.utils.config import API_CONFIG

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retry configuration
RETRY_CONFIG = {
    'stop': stop_after_attempt(API_CONFIG['max_retries']),
    'wait': wait_exponential(
        multiplier=1,
        min=API_CONFIG['base_delay'],
        max=API_CONFIG['max_delay']
    ),
    'retry': retry_if_exception_type((
        googleapiclient.errors.HttpError,
        ConnectionError,
        TimeoutError
    )),
    'reraise': True
}

def log_api_call(endpoint, params, result_count=0, error=None):
    """Log API call details."""
    log_data = {
        'endpoint': endpoint,
        'params': {k: v for k, v in params.items() if k != 'key'},  # Don't log API key
        'result_count': result_count,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if error:
        log_data['error'] = str(error)
        logger.error("API Error: %s", log_data)
    else:
        logger.info("API Call: %s", log_data)

def make_youtube_request(request_func, max_retries=3, retry_delay=1):
    """Execute a YouTube API request with automatic retry and error handling.
    
    Args:
        request_func: The function to execute (usually the execute method of a request object)
        max_retries: Maximum number of retries before giving up
        retry_delay: Delay in seconds between retries
        
    Returns:
        Response data or None if request failed
    """
    import time
    
    for attempt in range(max_retries):
        try:
            response = request_func()
            
            # Check for API key error in response
            if isinstance(response, dict) and 'error' in response:
                error = response['error']
                error_message = error.get('message', 'Unknown error')
                
                if 'API key' in error_message or 'apiKey' in error_message:
                    print(f"[ERROR] YouTube API key issue: {error_message}")
                    return None
                    
                if 'quota' in error_message.lower():
                    print(f"[ERROR] YouTube API quota exceeded: {error_message}")
                    return None
                    
                print(f"[ERROR] YouTube API error: {error_message}")
                # For other errors, try again after delay
                time.sleep(retry_delay * (attempt + 1))
                continue
                
            return response
            
        except Exception as e:
            error_str = str(e)
            print(f"[ERROR] YouTube API request failed (attempt {attempt+1}/{max_retries}): {error_str}")
            
            # If it's an API key issue, don't retry
            if 'API key' in error_str or 'apiKey' in error_str:
                print("[ERROR] API key issue detected, not retrying")
                return None
                
            # If it's a quota issue, don't retry
            if 'quota' in error_str.lower():
                print("[ERROR] Quota exceeded, not retrying")
                return None
                
            # For network issues, retry after delay
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))
            else:
                print("[ERROR] Max retries reached, giving up")
                return None
    
    return None

def get_cached_data(cache_key, max_age_minutes=None):
    """Get data from cache if it exists and is not expired."""
    if cache_key not in st.session_state:
        return None
        
    data, timestamp = st.session_state[cache_key]
    max_age = timedelta(minutes=max_age_minutes or API_CONFIG['cache_ttl_minutes'])
    
    if datetime.now() - timestamp < max_age:
        return data
    return None

def set_cached_data(cache_key, data):
    """Store data in cache with current timestamp."""
    st.session_state[cache_key] = (data, datetime.now())

def safe_parse_duration(duration_str):
    """Safely parse ISO 8601 duration string to seconds."""
    try:
        # Simple parser for PT#M#S format
        if 'PT' not in duration_str:
            return 0
            
        duration_str = duration_str[2:]  # Remove 'PT' prefix
        total_seconds = 0
        
        # Handle hours
        if 'H' in duration_str:
            hours, duration_str = duration_str.split('H')
            total_seconds += int(hours) * 3600
            
        # Handle minutes
        if 'M' in duration_str:
            minutes, duration_str = duration_str.split('M')
            total_seconds += int(minutes) * 60
            
        # Handle seconds
        if 'S' in duration_str:
            seconds = duration_str.split('S')[0]
            total_seconds += int(seconds)
            
        return total_seconds
    except (ValueError, AttributeError):
        return 0

def safe_int(value, default=0):
    """Safely convert value to int with default fallback."""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
