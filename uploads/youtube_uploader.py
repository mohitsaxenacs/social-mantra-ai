import os
import logging
import http.client
import httplib2
import random
import time
import json
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)

class YouTubeUploader:
    def __init__(self):
        """Initialize YouTube uploader with API credentials"""
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.client_secrets_file = os.getenv('YOUTUBE_CLIENT_SECRETS')
        self.credentials_file = os.path.join('config', 'youtube_credentials.json')
        self.youtube = None
        
        # Ensure credential directory exists
        os.makedirs(os.path.dirname(self.credentials_file), exist_ok=True)
        
        # Scopes required for uploading and updating videos
        self.scopes = [
            'https://www.googleapis.com/auth/youtube.upload',
            'https://www.googleapis.com/auth/youtube'
        ]
    
    def _get_authenticated_service(self):
        """Get an authenticated YouTube API service"""
        credentials = None
        
        # Check if credentials file exists
        if os.path.exists(self.credentials_file):
            credentials = Credentials.from_authorized_user_info(
                json.load(open(self.credentials_file)),
                self.scopes
            )
        
        # If credentials don't exist or are invalid, run the auth flow
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())
                except:
                    logger.warning("Failed to refresh credentials, re-authenticating")
                    if os.path.exists(self.credentials_file):
                        os.remove(self.credentials_file)
                    credentials = None
            
            if not credentials:
                if not self.client_secrets_file or not os.path.exists(self.client_secrets_file):
                    logger.error("YouTube client secrets file not found")
                    return None
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, 
                    self.scopes
                )
                credentials = flow.run_local_server(port=0)
                
                # Save credentials for future use
                with open(self.credentials_file, 'w') as token:
                    token.write(credentials.to_json())
        
        # Build the service
        try:
            return build('youtube', 'v3', credentials=credentials)
        except Exception as e:
            logger.error(f"Error building YouTube service: {str(e)}")
            return None
    
    def _parse_metadata(self, metadata_path):
        """Parse YouTube metadata from file"""
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        
        metadata = {
            'title': '',
            'description': '',
            'tags': [],
            'category': 'Entertainment'
        }
        
        current_section = None
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                if not line or line.startswith('YOUTUBE SHORTS METADATA'):
                    continue
                
                if line.startswith('Title:'):
                    metadata['title'] = line[6:].strip()
                elif line.startswith('Description:'):
                    metadata['description'] = line[12:].strip()
                elif line.startswith('Tags:'):
                    metadata['tags'] = [tag.strip() for tag in line[5:].split(',')]
                elif line.startswith('Category:'):
                    metadata['category'] = line[9:].strip()
        
        return metadata
    
    def upload(self, video_path, metadata_path, private=True):
        """Upload a video to YouTube with private or public visibility"""
        if not os.path.exists(video_path):
            error_msg = f"Video file not found: {video_path}"
            logger.error(error_msg)
            return {'error': error_msg}
        
        # Parse metadata
        try:
            metadata = self._parse_metadata(metadata_path)
        except Exception as e:
            error_msg = f"Failed to parse metadata: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg}
        
        # Initialize YouTube API service
        if not self.youtube:
            self.youtube = self._get_authenticated_service()
            
        if not self.youtube:
            error_msg = "YouTube API service not available, make sure credentials are configured"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'unauthenticated'}
        
        # Determine the video category ID
        # Common categories: 22 (People & Blogs), 23 (Comedy), 24 (Entertainment), etc.
        category_mapping = {
            'People & Blogs': '22',
            'Comedy': '23',
            'Entertainment': '24',
            'Music': '10',
            'Gaming': '20',
            'Sports': '17',
            'Science & Technology': '28',
            'Education': '27',
            'Food': '26',  # Actually 'Howto & Style'
        }
        
        category_id = category_mapping.get(metadata['category'], '24')  # Default to Entertainment
        
        # Set video privacy status
        privacy_status = 'private' if private else 'public'
        
        # Create video insert request
        body = {
            'snippet': {
                'title': metadata['title'],
                'description': metadata['description'],
                'tags': metadata['tags'],
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        try:
            # Create media upload object
            media = MediaFileUpload(
                video_path, 
                mimetype='video/mp4', 
                chunksize=1024*1024, 
                resumable=True
            )
            
            # Create the API request
            insert_request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            # Upload the video
            logger.info(f"Starting YouTube upload for video: {metadata['title']}")
            response = self._resumable_upload(insert_request)
            
            if response:
                result = {
                    'video_id': response['id'],
                    'title': response['snippet']['title'],
                    'url': f"https://youtu.be/{response['id']}",
                    'status': response['status']['privacyStatus'],
                    'uploaded_at': datetime.now().isoformat()
                }
                logger.info(f"Successfully uploaded video to YouTube: {result['url']}")
                return result
            else:
                return {'error': 'Upload failed or was interrupted', 'status': 'failed'}
                
        except HttpError as e:
            error_msg = f"YouTube API HTTP error: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'api_error'}
            
        except Exception as e:
            error_msg = f"YouTube upload error: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'error'}
    
    def _resumable_upload(self, insert_request):
        """Upload a video in resumable chunks with progress and error handling"""
        response = None
        error = None
        retry = 0
        max_retries = 10
        
        while response is None:
            try:
                status, response = insert_request.next_chunk()
                if status:
                    percent = int(status.progress() * 100)
                    logger.info(f"YouTube upload progress: {percent}%")
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    if retry >= max_retries:
                        logger.error(f"YouTube upload failed after {max_retries} retries")
                        return None
                    retry += 1
                    sleep_seconds = random.randint(1, 2 ** retry)
                    logger.warning(f"YouTube API server error, retrying in {sleep_seconds} seconds...")
                    time.sleep(sleep_seconds)
                else:
                    logger.error(f"YouTube upload error: {str(e)}")
                    return None
            except (httplib2.HttpLib2Error, http.client.HTTPException) as e:
                if retry >= max_retries:
                    logger.error(f"YouTube upload connection error after {max_retries} retries")
                    return None
                retry += 1
                sleep_seconds = random.randint(1, 2 ** retry)
                logger.warning(f"YouTube upload connection error, retrying in {sleep_seconds} seconds: {str(e)}")
                time.sleep(sleep_seconds)
        
        return response
    
    def schedule(self, video_id, schedule_time):
        """Schedule a private video to be published at a specific time"""
        if not self.youtube:
            self.youtube = self._get_authenticated_service()
            
        if not self.youtube:
            error_msg = "YouTube API service not available, make sure credentials are configured"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'unauthenticated'}
        
        try:
            # Format publish time in ISO 8601 format
            publish_time = schedule_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
            # Update video status to scheduled
            response = self.youtube.videos().update(
                part='status',
                body={
                    'id': video_id,
                    'status': {
                        'privacyStatus': 'private',  # Will become public at publish time
                        'publishAt': publish_time,
                        'selfDeclaredMadeForKids': False
                    }
                }
            ).execute()
            
            result = {
                'video_id': response['id'],
                'scheduled_for': publish_time,
                'status': 'scheduled'
            }
            
            logger.info(f"Successfully scheduled YouTube video {video_id} for {publish_time}")
            return result
            
        except HttpError as e:
            error_msg = f"YouTube API HTTP error while scheduling: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'api_error'}
            
        except Exception as e:
            error_msg = f"YouTube scheduling error: {str(e)}"
            logger.error(error_msg)
            return {'error': error_msg, 'status': 'error'}
