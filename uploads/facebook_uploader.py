import os
import logging
import json
import time
from datetime import datetime
import requests

logger = logging.getLogger(__name__)

class FacebookUploader:
    def __init__(self):
        """Initialize Facebook uploader with API credentials"""
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')  # Page ID for posting
        
        # Base URLs for API calls
        self.graph_url = 'https://graph.facebook.com/v18.0/'
        
        # Check if required credentials are available
        self.api_ready = all([self.app_id, self.app_secret, self.access_token, self.page_id])
        if not self.api_ready:
            logger.warning("Facebook API credentials incomplete. Some features may be unavailable.")
    
    def _parse_metadata(self, metadata_path):
        """Parse Facebook metadata from file"""
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        
        metadata = {
            'title': '',
            'description': '',
            'hashtags': [],
            'call_to_action': ''
        }
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                if not line or line.startswith('FACEBOOK REELS METADATA'):
                    continue
                
                if line.startswith('Title:'):
                    metadata['title'] = line[6:].strip()
                elif line.startswith('Description:'):
                    metadata['description'] = line[12:].strip()
                elif line.startswith('Hashtags:'):
                    hashtags_text = line[9:].strip()
                    metadata['hashtags'] = [tag.strip() for tag in hashtags_text.split() if tag.strip().startswith('#') or tag.strip()]
                elif line.startswith('Call to Action:'):
                    metadata['call_to_action'] = line[15:].strip()
        
        return metadata
    
    def upload(self, video_path, metadata_path, private=True):
        """Upload a video to Facebook Reels with private or public visibility"""
        if not os.path.exists(video_path):
            error_msg = f"Video file not found: {video_path}"
            logger.error(error_msg)
            return {'error': error_msg}
        
        if not self.api_ready:
            error_msg = "Facebook API credentials not configured"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'unauthenticated'}
        
        # Parse metadata
        try:
            metadata = self._parse_metadata(metadata_path)
        except Exception as e:
            error_msg = f"Failed to parse metadata: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg}
        
        # Prepare caption with hashtags
        description = metadata['description']
        if metadata['hashtags']:
            # Add proper # if missing
            hashtags = [tag if tag.startswith('#') else f"#{tag}" for tag in metadata['hashtags']]
            hashtag_text = ' '.join(hashtags)
            description = f"{description}\n\n{hashtag_text}"
        
        # Add call to action if available
        if metadata['call_to_action']:
            description = f"{description}\n\n{metadata['call_to_action']}"
        
        # Set privacy status
        privacy = {'value': 'ONLY_ME'} if private else {'value': 'EVERYONE'}
        
        try:
            # Step 1: Get upload URL via container endpoint
            upload_phase_url = f"{self.graph_url}{self.page_id}/video_reels"
            upload_params = {
                'access_token': self.access_token,
                'upload_phase': 'start',
                'title': metadata['title'],
                'description': description
            }
            
            # Add privacy setting
            if private:
                upload_params['privacy'] = json.dumps(privacy)
            
            upload_response = requests.post(upload_phase_url, data=upload_params)
            
            if upload_response.status_code != 200:
                error_msg = f"Facebook API error: {upload_response.text}"
                logger.error(error_msg)
                return {'error': error_msg, 'status': 'api_error'}
            
            upload_data = upload_response.json()
            video_id = upload_data.get('video_id')
            upload_url = upload_data.get('upload_url')
            
            if not video_id or not upload_url:
                error_msg = "Failed to get Facebook upload URL"
                logger.error(error_msg)
                return {'error': error_msg, 'status': 'api_error'}
            
            # Step 2: Upload the video to the provided URL
            with open(video_path, 'rb') as video_file:
                video_data = video_file.read()
            
            upload_response = requests.post(
                upload_url, 
                files={'video_file': ('video.mp4', video_data, 'video/mp4')},
                headers={'Authorization': f'Bearer {self.access_token}'}
            )
            
            if upload_response.status_code not in [200, 201]:
                error_msg = f"Facebook video upload error: {upload_response.text}"
                logger.error(error_msg)
                return {'error': error_msg, 'status': 'upload_error'}
            
            # Step 3: Finalize the upload
            finalize_params = {
                'access_token': self.access_token,
                'upload_phase': 'finish',
                'video_id': video_id
            }
            
            finalize_response = requests.post(upload_phase_url, data=finalize_params)
            
            if finalize_response.status_code != 200:
                error_msg = f"Facebook video finalization error: {finalize_response.text}"
                logger.error(error_msg)
                return {'error': error_msg, 'status': 'finalization_error'}
            
            finalize_data = finalize_response.json()
            
            # Return success result
            result = {
                'video_id': video_id,
                'title': metadata['title'],
                'url': f"https://www.facebook.com/watch/?v={video_id}",  # This is a generic URL pattern
                'status': 'private' if private else 'public',
                'uploaded_at': datetime.now().isoformat()
            }
            
            logger.info(f"Successfully uploaded video to Facebook: {result['url']}")
            return result
            
        except requests.RequestException as e:
            error_msg = f"Facebook API request error: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'request_error'}
            
        except Exception as e:
            error_msg = f"Facebook upload error: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'error'}
    
    def schedule(self, video_id, schedule_time):
        """Schedule a private video to be published at a specific time"""
        if not self.api_ready:
            error_msg = "Facebook API credentials not configured"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'unauthenticated'}
        
        try:
            # Format publish time in Unix timestamp
            publish_timestamp = int(schedule_time.timestamp())
            
            # Update video status to scheduled
            schedule_url = f"{self.graph_url}{video_id}"
            schedule_params = {
                'access_token': self.access_token,
                'privacy': json.dumps({
                    'value': 'EVERYONE',
                    'publish_time': publish_timestamp
                })
            }
            
            schedule_response = requests.post(schedule_url, data=schedule_params)
            
            if schedule_response.status_code != 200:
                error_msg = f"Facebook scheduling error: {schedule_response.text}"
                logger.error(error_msg)
                return {'error': error_msg, 'status': 'api_error'}
            
            schedule_data = schedule_response.json()
            
            # Return success result
            result = {
                'video_id': video_id,
                'scheduled_for': schedule_time.isoformat(),
                'status': 'scheduled'
            }
            
            logger.info(f"Successfully scheduled Facebook video {video_id} for {schedule_time.isoformat()}")
            return result
            
        except requests.RequestException as e:
            error_msg = f"Facebook API request error during scheduling: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'request_error'}
            
        except Exception as e:
            error_msg = f"Facebook scheduling error: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'error'}
