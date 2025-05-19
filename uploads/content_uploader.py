import os
import json
import logging
from datetime import datetime, timedelta
import time

# Import platform-specific uploaders
from uploads.youtube_uploader import YouTubeUploader
from uploads.facebook_uploader import FacebookUploader
from uploads.instagram_uploader import InstagramUploader

logger = logging.getLogger(__name__)

class ContentUploader:
    def __init__(self):
        self.youtube_uploader = YouTubeUploader()
        self.facebook_uploader = FacebookUploader()
        self.instagram_uploader = InstagramUploader()
        
        self.data_dir = os.path.join('data', 'uploads')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def upload_content(self, content_ideas, private=True):
        """Upload generated content to each platform with private visibility"""
        logger.info(f"Starting content upload process for {len(content_ideas)} ideas (Private: {private})")
        
        upload_results = []
        
        for i, idea in enumerate(content_ideas):
            logger.info(f"Processing upload for content idea #{i+1}: {idea['title']}")
            
            # Get content assets folder path
            content_dir = os.path.join('export', f'content_idea_{i+1}')
            
            # Initialize result entry
            result = {
                'content_id': i+1,
                'title': idea['title'],
                'uploaded_at': datetime.now().isoformat(),
                'private': private,
                'platforms': {}
            }
            
            # Check for required files
            if not self._verify_content_files(content_dir):
                logger.error(f"Content idea #{i+1} is missing required files for upload")
                result['error'] = "Missing required files for upload"
                upload_results.append(result)
                continue
            
            # Upload to each platform
            try:
                # YouTube upload
                youtube_result = self.youtube_uploader.upload(
                    video_path=os.path.join(content_dir, 'video.mp4'),
                    metadata_path=os.path.join(content_dir, 'youtube_metadata.txt'),
                    private=private
                )
                result['platforms']['youtube'] = youtube_result
                
                # Brief pause between uploads
                time.sleep(2)
                
                # Facebook upload
                facebook_result = self.facebook_uploader.upload(
                    video_path=os.path.join(content_dir, 'video.mp4'),
                    metadata_path=os.path.join(content_dir, 'facebook_metadata.txt'),
                    private=private
                )
                result['platforms']['facebook'] = facebook_result
                
                # Brief pause between uploads
                time.sleep(2)
                
                # Instagram upload
                instagram_result = self.instagram_uploader.upload(
                    video_path=os.path.join(content_dir, 'video.mp4'),
                    metadata_path=os.path.join(content_dir, 'instagram_metadata.txt'),
                    private=private
                )
                result['platforms']['instagram'] = instagram_result
                
                # Add to results
                upload_results.append(result)
                logger.info(f"Successfully uploaded content idea #{i+1} to all platforms")
                
            except Exception as e:
                logger.error(f"Error uploading content idea #{i+1}: {str(e)}")
                result['error'] = str(e)
                upload_results.append(result)
        
        # Save upload results
        self._save_upload_results(upload_results)
        
        return upload_results
    
    def schedule_content(self, content_ids, schedule_date=None, stagger=True):
        """Schedule previously uploaded private content for public release"""
        logger.info(f"Scheduling content IDs: {content_ids}")
        
        # Load upload records
        upload_records = self._load_upload_results()
        
        # Filter for requested content IDs
        to_schedule = [record for record in upload_records if record.get('content_id') in content_ids]
        
        if not to_schedule:
            logger.error(f"No matching upload records found for content IDs: {content_ids}")
            return {'error': 'No matching upload records found'}
        
        # Default schedule date to tomorrow if not provided
        if not schedule_date:
            schedule_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        schedule_time = datetime.strptime(f"{schedule_date} 09:00", '%Y-%m-%d %H:%M')
        schedule_results = []
        
        for i, record in enumerate(to_schedule):
            result = {
                'content_id': record['content_id'],
                'title': record['title'],
                'scheduled_for': schedule_time.isoformat(),
                'platforms': {}
            }
            
            try:
                # Calculate staggered time if needed (30 min intervals)
                current_schedule = schedule_time
                if stagger and i > 0:
                    current_schedule += timedelta(minutes=30 * i)
                
                # Schedule on each platform
                if 'youtube' in record['platforms']:
                    youtube_id = record['platforms']['youtube'].get('video_id')
                    if youtube_id:
                        youtube_result = self.youtube_uploader.schedule(
                            video_id=youtube_id,
                            schedule_time=current_schedule
                        )
                        result['platforms']['youtube'] = youtube_result
                
                if 'facebook' in record['platforms']:
                    facebook_id = record['platforms']['facebook'].get('video_id')
                    if facebook_id:
                        facebook_result = self.facebook_uploader.schedule(
                            video_id=facebook_id,
                            schedule_time=current_schedule
                        )
                        result['platforms']['facebook'] = facebook_result
                
                if 'instagram' in record['platforms']:
                    instagram_id = record['platforms']['instagram'].get('video_id')
                    if instagram_id:
                        instagram_result = self.instagram_uploader.schedule(
                            video_id=instagram_id,
                            schedule_time=current_schedule
                        )
                        result['platforms']['instagram'] = instagram_result
                
                schedule_results.append(result)
                logger.info(f"Successfully scheduled content ID {record['content_id']} for {current_schedule.isoformat()}")
                
            except Exception as e:
                logger.error(f"Error scheduling content ID {record['content_id']}: {str(e)}")
                result['error'] = str(e)
                schedule_results.append(result)
        
        # Save scheduling results
        self._save_schedule_results(schedule_results)
        
        return schedule_results
    
    def _verify_content_files(self, content_dir):
        """Verify that all required files exist for upload"""
        required_files = [
            'video.mp4',  # We'll assume video.mp4 is the video file
            'youtube_metadata.txt',
            'facebook_metadata.txt',
            'instagram_metadata.txt'
        ]
        
        return all(os.path.exists(os.path.join(content_dir, file)) for file in required_files)
    
    def _save_upload_results(self, results):
        """Save upload results to a JSON file"""
        try:
            # Load existing results if any
            filepath = os.path.join(self.data_dir, 'upload_records.json')
            existing_results = []
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing_results = json.load(f)
            
            # Append new results
            combined_results = existing_results + results
            
            # Save combined results
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(combined_results, f, ensure_ascii=False, indent=4)
                
            logger.info(f"Saved upload results to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving upload results: {str(e)}")
    
    def _save_schedule_results(self, results):
        """Save scheduling results to a JSON file"""
        try:
            # Load existing results if any
            filepath = os.path.join(self.data_dir, 'schedule_records.json')
            existing_results = []
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing_results = json.load(f)
            
            # Append new results
            combined_results = existing_results + results
            
            # Save combined results
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(combined_results, f, ensure_ascii=False, indent=4)
                
            logger.info(f"Saved scheduling results to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving scheduling results: {str(e)}")
    
    def _load_upload_results(self):
        """Load existing upload results"""
        try:
            filepath = os.path.join(self.data_dir, 'upload_records.json')
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return []
                
        except Exception as e:
            logger.error(f"Error loading upload results: {str(e)}")
            return []
