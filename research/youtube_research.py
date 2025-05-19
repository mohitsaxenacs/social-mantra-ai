import os
import json
import logging
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

class YouTubeResearch:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube = self._build_youtube_client()
        self.data_dir = os.path.join('data', 'youtube')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _build_youtube_client(self):
        if not self.api_key:
            logger.warning("YouTube API key not found in environment variables")
            return None
            
        try:
            return build('youtube', 'v3', developerKey=self.api_key)
        except Exception as e:
            logger.error(f"Error building YouTube client: {str(e)}")
            return None
    
    def get_trending_videos(self, niche, max_results=50):
        """Fetch trending videos related to a specific niche"""
        if not self.youtube:
            logger.error("YouTube client not initialized. Cannot fetch trending videos.")
            return self._load_sample_data('trending_videos.json')
        
        try:
            # Search for trending videos in the niche
            search_response = self.youtube.search().list(
                q=niche,
                part='id,snippet',
                maxResults=max_results,
                type='video',
                videoDefinition='high',
                relevanceLanguage='en',
                order='viewCount'
            ).execute()
            
            # Get video IDs from search results
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            # Get detailed stats for each video
            if video_ids:
                videos_response = self.youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(video_ids)
                ).execute()
                
                # Process video data
                videos = []
                for item in videos_response.get('items', []):
                    video = {
                        'id': item['id'],
                        'title': item['snippet']['title'],
                        'channel_id': item['snippet']['channelId'],
                        'channel_title': item['snippet']['channelTitle'],
                        'description': item['snippet']['description'],
                        'published_at': item['snippet']['publishedAt'],
                        'thumbnail': item['snippet']['thumbnails']['high']['url'],
                        'view_count': int(item['statistics'].get('viewCount', 0)),
                        'like_count': int(item['statistics'].get('likeCount', 0)),
                        'comment_count': int(item['statistics'].get('commentCount', 0)),
                        'tags': item['snippet'].get('tags', []),
                        'duration': item['contentDetails']['duration'],
                        'engagement_ratio': self._calculate_engagement_ratio(item['statistics'])
                    }
                    videos.append(video)
                
                # Sort by engagement ratio
                videos.sort(key=lambda x: x['engagement_ratio'], reverse=True)
                
                # Save results
                self._save_data('trending_videos.json', {
                    'niche': niche,
                    'date': datetime.now().isoformat(),
                    'videos': videos
                })
                
                return videos
            return []
                
        except HttpError as e:
            logger.error(f"YouTube API error: {str(e)}")
            return self._load_sample_data('trending_videos.json')
        except Exception as e:
            logger.error(f"Error fetching trending videos: {str(e)}")
            return self._load_sample_data('trending_videos.json')
    
    def get_top_channels(self, niche, max_results=20):
        """Find top channels in a specific niche"""
        if not self.youtube:
            logger.error("YouTube client not initialized. Cannot fetch top channels.")
            return self._load_sample_data('top_channels.json')
        
        try:
            # Search for top channels in the niche
            search_response = self.youtube.search().list(
                q=niche,
                part='id,snippet',
                maxResults=max_results,
                type='channel',
                relevanceLanguage='en'
            ).execute()
            
            # Get channel IDs from search results
            channel_ids = [item['id']['channelId'] for item in search_response.get('items', [])]
            
            # Get detailed stats for each channel
            if channel_ids:
                channels_response = self.youtube.channels().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(channel_ids)
                ).execute()
                
                # Process channel data
                channels = []
                for item in channels_response.get('items', []):
                    channel = {
                        'id': item['id'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'thumbnail': item['snippet']['thumbnails']['high']['url'],
                        'subscriber_count': int(item['statistics'].get('subscriberCount', 0)),
                        'video_count': int(item['statistics'].get('videoCount', 0)),
                        'view_count': int(item['statistics'].get('viewCount', 0)),
                        'uploads_playlist': item['contentDetails']['relatedPlaylists']['uploads']
                    }
                    channels.append(channel)
                
                # Sort by subscriber count
                channels.sort(key=lambda x: x['subscriber_count'], reverse=True)
                
                # For top 5 channels, get their most popular videos
                for i, channel in enumerate(channels[:5]):
                    channel['popular_videos'] = self._get_popular_videos(channel['id'])
                
                # Save results
                self._save_data('top_channels.json', {
                    'niche': niche,
                    'date': datetime.now().isoformat(),
                    'channels': channels
                })
                
                return channels
            return []
                
        except HttpError as e:
            logger.error(f"YouTube API error: {str(e)}")
            return self._load_sample_data('top_channels.json')
        except Exception as e:
            logger.error(f"Error fetching top channels: {str(e)}")
            return self._load_sample_data('top_channels.json')
    
    def _get_popular_videos(self, channel_id, max_results=5):
        """Get most popular videos from a channel"""
        try:
            # Search for popular videos from the channel
            search_response = self.youtube.search().list(
                channelId=channel_id,
                part='id,snippet',
                maxResults=max_results,
                type='video',
                order='viewCount'
            ).execute()
            
            # Get video IDs from search results
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            # Get detailed stats for each video
            if video_ids:
                videos_response = self.youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(video_ids)
                ).execute()
                
                # Process video data
                videos = []
                for item in videos_response.get('items', []):
                    video = {
                        'id': item['id'],
                        'title': item['snippet']['title'],
                        'view_count': int(item['statistics'].get('viewCount', 0)),
                        'like_count': int(item['statistics'].get('likeCount', 0)),
                        'thumbnail': item['snippet']['thumbnails']['high']['url']
                    }
                    videos.append(video)
                
                return videos
            return []
                
        except Exception as e:
            logger.error(f"Error fetching popular videos: {str(e)}")
            return []
    
    def _calculate_engagement_ratio(self, statistics):
        """Calculate engagement ratio (likes + comments) / views"""
        views = int(statistics.get('viewCount', 0))
        likes = int(statistics.get('likeCount', 0))
        comments = int(statistics.get('commentCount', 0))
        
        if views == 0:
            return 0
            
        return (likes + comments) / views
    
    def _save_data(self, filename, data):
        """Save data to a JSON file"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"Data saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
    
    def _load_sample_data(self, filename):
        """Load sample data if API fails"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Loaded sample data from {filepath}")
                return data.get('videos', []) if 'videos' in data else data.get('channels', [])
            else:
                logger.warning(f"No sample data found at {filepath}")
                return []
        except Exception as e:
            logger.error(f"Error loading sample data: {str(e)}")
            return []
