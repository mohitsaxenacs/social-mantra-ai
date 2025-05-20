from pydantic import BaseSettings
from typing import Dict, Any, Optional
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Social Media Shorts Automation"
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]
    DEFAULT_REGION: str = "US"
    
    # YouTube API Regional mapping
    REGIONS: Dict[str, str] = {
        "United States": "US",
        "United Kingdom": "GB",
        "Canada": "CA",
        "Australia": "AU",
        "India": "IN",
        "Brazil": "BR",
        "France": "FR",
        "Germany": "DE",
        "Japan": "JP",
        "South Korea": "KR",
        "Mexico": "MX",
        "Spain": "ES",
        "Italy": "IT",
        "Russia": "RU",
        "Netherlands": "NL"
    }

settings = Settings()
