"""Configuration settings for the YouTube API integration."""
from pathlib import Path
import yaml
import os

# Default configuration
DEFAULT_CONFIG = {
    "api": {
        "max_retries": 3,
        "timeout": 30,
        "cache_ttl_minutes": 60,
        "max_results": 50,
        "base_delay": 1,
        "max_delay": 10,
    },
    "regions": {
        "United States": "US",
        "United Kingdom": "GB",
        "Canada": "CA",
        "Australia": "AU",
        "India": "IN",
        "Germany": "DE",
        "France": "FR",
        "Japan": "JP",
        "South Korea": "KR",
        "Brazil": "BR",
        "Mexico": "MX",
        "Russia": "RU",
        "Global": "US"
    }
}

def load_config():
    """Load configuration from file or return defaults."""
    config_path = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or DEFAULT_CONFIG
        except Exception as e:
            print(f"Error loading config file: {e}")
    return DEFAULT_CONFIG

# Load configuration
CONFIG = load_config()

# Export commonly used settings
API_CONFIG = CONFIG.get('api', {})
REGIONS = CONFIG.get('regions', {})
DEFAULT_REGION = REGIONS.get('Global', 'US')

def save_config():
    """Save current configuration to file."""
    config_path = Path(__file__).parent.parent.parent / 'config'
    config_path.mkdir(parents=True, exist_ok=True)
    
    with open(config_path / 'config.yaml', 'w') as f:
        yaml.safe_dump(CONFIG, f)

# Make sure these are available for import
__all__ = ['API_CONFIG', 'REGIONS', 'DEFAULT_REGION', 'load_config', 'save_config']
