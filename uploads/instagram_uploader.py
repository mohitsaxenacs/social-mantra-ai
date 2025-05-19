import os
import logging
import json
import time
from datetime import datetime
import requests
from instagrapi import Client

logger = logging.getLogger(__name__)

class InstagramUploader:
    def __init__(self):
        """Initialize Instagram uploader with API credentials"""
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        self.credentials_file = os.path.join('config', 'instagram_credentials.json')
        self.client = None
        
        # Check if required credentials are available
        self.api_ready = all([self.username, self.password])
        if not self.api_ready:
            logger.warning("Instagram credentials incomplete. Some features may be unavailable.")
        
        # Ensure credential directory exists
        os.makedirs(os.path.dirname(self.credentials_file), exist_ok=True)
    
    def _get_authenticated_client(self):
        """Get an authenticated Instagram client"""
        if not self.api_ready:
            logger.error("Instagram credentials not configured")
            return None
        
        try:
            # Create client instance
            client = Client()
            
            # Load session if available
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    cached_settings = json.load(f)
                    client.set_settings(cached_settings)
                    logger.info("Loaded Instagram session from cache")
                    
                # Test if session is still valid
                try:
                    client.get_timeline_feed()
                    logger.info("Instagram session is valid")
                    return client
                except Exception as e:
                    logger.warning(f"Cached Instagram session expired: {str(e)}")
                    # Continue to login
            
            # Login with username and password
            logged_in = client.login(self.username, self.password)
            
            if logged_in:
                # Save session for future use
                with open(self.credentials_file, 'w') as f:
                    json.dump(client.get_settings(), f)
                logger.info("Instagram login successful")
                return client
            else:
                logger.error("Instagram login failed")
                return None
        
        except Exception as e:
            logger.error(f"Error authenticating with Instagram: {str(e)}")
            return None
    
    def _parse_metadata(self, metadata_path):
        """Parse Instagram metadata from file"""
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        
        metadata = {
            'caption': '',
            'hashtags': [],
            'mentions': []
        }
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                if not line or line.startswith('INSTAGRAM REELS METADATA'):
                    continue
                
                if line.startswith('Caption:'):
                    metadata['caption'] = line[8:].strip()
                elif line.startswith('Hashtags:'):
                    hashtags_text = line[9:].strip()
                    metadata['hashtags'] = [tag.strip() for tag in hashtags_text.split() if tag.strip().startswith('#') or tag.strip()]
                elif line.startswith('Mentions:'):
                    mentions_text = line[9:].strip()
                    metadata['mentions'] = [mention.strip() for mention in mentions_text.split(',') if mention.strip()]
        
        return metadata
    
    def upload(self, video_path, metadata_path, private=True):
        """Upload a video to Instagram Reels with private or public visibility"""
        if not os.path.exists(video_path):
            error_msg = f"Video file not found: {video_path}"
            logger.error(error_msg)
            return {'error': error_msg}
        
        # Initialize Instagram client if needed
        if not self.client:
            self.client = self._get_authenticated_client()
            
        if not self.client:
            error_msg = "Instagram client not available, make sure credentials are configured"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'unauthenticated'}
        
        # Parse metadata
        try:
            metadata = self._parse_metadata(metadata_path)
        except Exception as e:
            error_msg = f"Failed to parse metadata: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg}
        
        # Prepare caption with hashtags and mentions
        caption = metadata['caption']
        
        # Add hashtags if any
        if metadata['hashtags']:
            # Add proper # if missing
            hashtags = [tag if tag.startswith('#') else f"#{tag}" for tag in metadata['hashtags']]
            hashtag_text = ' '.join(hashtags)
            caption = f"{caption}\n\n{hashtag_text}"
        
        # Add mentions if any
        if metadata['mentions']:
            # Add proper @ if missing
            mentions = [mention if mention.startswith('@') else f"@{mention}" for mention in metadata['mentions']]
            mentions_text = ' '.join(mentions)
            caption = f"{caption}\n\n{mentions_text}"
        
        try:
            # Upload to Instagram Reels
            logger.info(f"Starting Instagram Reels upload: {os.path.basename(video_path)}")
            
            # Set visibility
            if private:
                # In instagrapi, we upload as a private post first, then later can set to public
                result = self.client.clip_upload(
                    video_path,
                    caption=caption,
                    # For private posts, we use 'only_me' as the audience
                    extra_data={'audience': 'only_me'}
                )
            else:
                # Upload as public
                result = self.client.clip_upload(
                    video_path,
                    caption=caption
                )
            
            # Format the result for consistent response
            media_id = result.id
            media_code = result.code
            
            upload_result = {
                'video_id': media_id,
                'media_code': media_code,
                'url': f"https://www.instagram.com/reel/{media_code}/",
                'status': 'private' if private else 'public',
                'uploaded_at': datetime.now().isoformat()
            }
            
            logger.info(f"Successfully uploaded video to Instagram: {upload_result['url']}")
            return upload_result
            
        except Exception as e:
            error_msg = f"Instagram upload error: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'error'}
    
    def schedule(self, video_id, schedule_time):
        """Schedule a private video to be published at a specific time"""
        if not self.client:
            self.client = self._get_authenticated_client()
            
        if not self.client:
            error_msg = "Instagram client not available, make sure credentials are configured"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'unauthenticated'}
        
        try:
            # Note: Instagram doesn't have a direct API for scheduling posts
            # We're using a workaround by changing privacy settings at the scheduled time
            # In a production app, you would use a job scheduler like Celery
            # For this demo, we'll simulate scheduling by returning success
            
            # Format time for display
            formatted_time = schedule_time.isoformat()
            
            # In a real implementation, you would save this to a scheduling database
            # and have a background worker check for posts to publish
            
            # Return simulated success result
            result = {
                'video_id': video_id,
                'scheduled_for': formatted_time,
                'status': 'scheduled',
                'note': 'Instagram scheduling is simulated; in production use a job scheduler'
            }
            
            logger.info(f"Scheduled Instagram post {video_id} for {formatted_time}")
            return result
            
        except Exception as e:
            error_msg = f"Instagram scheduling error: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'error'}
