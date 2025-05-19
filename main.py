#!/usr/bin/env python3

import os
import sys
import logging
from dotenv import load_dotenv

# Import modules
from research.youtube_research import YouTubeResearch
from research.trends import TrendResearch
from generation.content_generator import ContentGenerator
from generation.metadata_generator import MetadataGenerator
from generation.audio_generator import AudioGenerator
from analytics.performance_analyzer import PerformanceAnalyzer
from uploads.content_uploader import ContentUploader

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class SocialMediaAutomation:
    def __init__(self):
        self.youtube_research = YouTubeResearch()
        self.trend_research = TrendResearch()
        self.content_generator = ContentGenerator()
        self.metadata_generator = MetadataGenerator()
        self.audio_generator = AudioGenerator()
        self.performance_analyzer = PerformanceAnalyzer()
        self.content_uploader = ContentUploader()
        
        # Create necessary directories
        os.makedirs('data', exist_ok=True)
        os.makedirs('export', exist_ok=True)
        os.makedirs('config', exist_ok=True)
        os.makedirs('assets/music', exist_ok=True)
        
        logger.info("Social Media Automation Tool initialized successfully")
    
    def run(self):
        print("\n========== SOCIAL MEDIA SHORTS AUTOMATION ==========\n")
        print("This tool will help you generate viral short-form videos")
        print("for YouTube Shorts, Facebook Reels, and Instagram Reels\n")
        
        # Get niche from user
        niche = input("Enter your content niche (e.g., cooking, fitness, tech): ")
        
        # Research phase
        print("\nResearching top performing content in your niche...")
        trending_videos = self.youtube_research.get_trending_videos(niche)
        top_channels = self.youtube_research.get_top_channels(niche)
        trending_topics = self.trend_research.get_trending_topics(niche)
        
        # Content generation phase
        print("\nGenerating content ideas based on research...")
        content_ideas = self.content_generator.generate_ideas(
            niche, 
            trending_videos, 
            top_channels,
            trending_topics,
            count=10
        )
        
        # Verify originality of content ideas
        for idea in content_ideas:
            # Basic originality check for concepts
            self._verify_originality(idea)
        
        # Metadata generation phase
        print("\nOptimizing metadata for each platform...")
        for i, idea in enumerate(content_ideas):
            print(f"\nContent Idea #{i+1}: {idea['title']}")
            
            # Generate metadata for each platform
            youtube_metadata = self.metadata_generator.for_youtube(idea)
            facebook_metadata = self.metadata_generator.for_facebook(idea)
            instagram_metadata = self.metadata_generator.for_instagram(idea)
            
            # Display and export metadata
            self._display_metadata(i+1, idea, youtube_metadata, facebook_metadata, instagram_metadata)
            self._export_metadata(i+1, idea, youtube_metadata, facebook_metadata, instagram_metadata)
            
            # Generate voiceover script (English)
            script = self.audio_generator.generate_script(idea)
            
            # Verify script originality
            originality_result = self.audio_generator.verify_originality(script)
            if not originality_result['is_original']:
                print(f"  ⚠️ Warning: Script may contain non-original content. Score: {originality_result['originality_score']}")
                if originality_result['suspicious_phrases']:
                    print(f"     Suspicious phrases: {', '.join(originality_result['suspicious_phrases'])}")
                # Generate a new script if necessary
                regenerate = input("  Would you like to regenerate a more original script? (y/n): ").lower() == 'y'
                if regenerate:
                    script = self.audio_generator.generate_script(idea)
            
            # Generate audio files if user wants to
            self._generate_audio_for_content(i+1, idea, script)
        
        # Audio generation phase (for all content at once)
        if input("\nWould you like to generate audio for all content ideas? (y/n): ").lower() == 'y':
            voice_gender = input("Preferred voice gender (male/female/random): ").lower()
            if voice_gender not in ['male', 'female', 'random']:
                voice_gender = 'random'
            
            mood = input("Background music mood (upbeat/calm/dramatic): ").lower()
            if mood not in ['upbeat', 'calm', 'dramatic']:
                mood = 'upbeat'
                
            print("\nGenerating audio files...")
            for i, idea in enumerate(content_ideas):
                content_id = i + 1
                # Check if script already exists
                script_file = os.path.join('data', 'audio', f"{idea['title'].replace(' ', '_')}_script.txt")
                
                if os.path.exists(script_file):
                    with open(script_file, 'r', encoding='utf-8') as f:
                        script = f.read()
                else:
                    # Generate script if it doesn't exist
                    script = self.audio_generator.generate_script(idea)
                
                # Generate audio
                self._generate_audio_for_content(content_id, idea, script, voice_gender, mood)
                print(f"  ✓ Generated audio for Content Idea #{content_id}: {idea['title']}")
        
        # Upload phase
        if input("\nWould you like to upload the generated content to social media platforms? (y/n): ").lower() == 'y':
            # Check if video files actually exist (for first-time usage they won't)
            content_ids = self._check_content_for_upload(content_ideas)
            
            if not content_ids:
                print("\nNo content is ready for upload. Please ensure videos are created first.")
                print("Place video files named 'video.mp4' in each content_idea_X folder.")
                
                # Ask if user wants to create placeholder videos with the audio
                if input("\nWould you like to create placeholder videos with the generated audio? (y/n): ").lower() == 'y':
                    self._create_placeholder_videos(content_ideas)
                    # Re-check content for upload
                    content_ids = self._check_content_for_upload(content_ideas)
            
            if content_ids:
                # Ask which content to upload
                print("\nThe following content is ready for upload:")
                for content_id in content_ids:
                    print(f"  {content_id}. {content_ideas[content_id-1]['title']}")
                
                upload_ids_input = input("\nEnter the content IDs to upload (comma-separated, or 'all'): ")
                
                if upload_ids_input.lower() == 'all':
                    upload_ids = content_ids
                else:
                    try:
                        upload_ids = [int(id.strip()) for id in upload_ids_input.split(',')]
                        # Filter to only valid IDs
                        upload_ids = [id for id in upload_ids if id in content_ids]
                    except ValueError:
                        print("Invalid input. No content will be uploaded.")
                        upload_ids = []
                
                if upload_ids:
                    # Confirm upload privacy
                    private = input("\nUpload as private for review first? (y/n): ").lower() == 'y'
                    private_status = "private" if private else "public"
                    
                    print(f"\nUploading {len(upload_ids)} videos as {private_status}...")
                    upload_results = self.content_uploader.upload_content(
                        [content_ideas[id-1] for id in upload_ids], 
                        private=private
                    )
                    
                    # Show upload results
                    self._display_upload_results(upload_results)
                    
                    # Ask about scheduling if uploaded as private
                    if private and upload_results:
                        if input("\nWould you like to schedule these private videos for public release? (y/n): ").lower() == 'y':
                            self._schedule_content([result.get('content_id') for result in upload_results if 'error' not in result])
        
        # Analytics and adjustment phase
        if input("\nWould you like to analyze performance of your existing content? (y/n): ").lower() == 'y':
            self._analyze_performance(niche)
    
    def _display_metadata(self, idx, idea, youtube, facebook, instagram):
        print(f"\n----- CONTENT IDEA #{idx}: {idea['title']} -----")
        
        print("\nYouTube Shorts Metadata:")
        print(f"Title: {youtube['title']}")
        print(f"Description: {youtube['description'][:100]}...")
        print(f"Tags: {', '.join(youtube['tags'][:5])}...")
        
        print("\nFacebook Reels Metadata:")
        print(f"Title: {facebook['title']}")
        print(f"Description: {facebook['description'][:100]}...")
        print(f"Hashtags: {' '.join(facebook['hashtags'][:5])}...")
        
        print("\nInstagram Reels Metadata:")
        print(f"Caption: {instagram['caption'][:100]}...")
        print(f"Hashtags: {' '.join(instagram['hashtags'][:5])}...")
    
    def _export_metadata(self, idx, idea, youtube, facebook, instagram):
        export_dir = os.path.join('export', f'content_idea_{idx}')
        os.makedirs(export_dir, exist_ok=True)
        
        # Export idea and metadata to files
        with open(os.path.join(export_dir, 'content_idea.txt'), 'w') as f:
            f.write(f"CONTENT IDEA #{idx}\n\n")
            f.write(f"Title: {idea['title']}\n")
            f.write(f"Concept: {idea['concept']}\n")
            f.write(f"Target Audience: {idea['target_audience']}\n")
            f.write(f"Hook: {idea['hook']}\n")
            f.write(f"Key Points: {', '.join(idea['key_points'])}\n")
            if 'originality_score' in idea:
                f.write(f"\nOriginality Score: {idea['originality_score']}\n")
        
        with open(os.path.join(export_dir, 'youtube_metadata.txt'), 'w') as f:
            f.write("YOUTUBE SHORTS METADATA\n\n")
            f.write(f"Title: {youtube['title']}\n")
            f.write(f"Description: {youtube['description']}\n")
            f.write(f"Tags: {', '.join(youtube['tags'])}\n")
            f.write(f"Category: {youtube['category']}\n")
        
        with open(os.path.join(export_dir, 'facebook_metadata.txt'), 'w') as f:
            f.write("FACEBOOK REELS METADATA\n\n")
            f.write(f"Title: {facebook['title']}\n")
            f.write(f"Description: {facebook['description']}\n")
            f.write(f"Hashtags: {' '.join(facebook['hashtags'])}\n")
            f.write(f"Call to Action: {facebook['call_to_action']}\n")
        
        with open(os.path.join(export_dir, 'instagram_metadata.txt'), 'w') as f:
            f.write("INSTAGRAM REELS METADATA\n\n")
            f.write(f"Caption: {instagram['caption']}\n")
            f.write(f"Hashtags: {' '.join(instagram['hashtags'])}\n")
            f.write(f"Mentions: {', '.join(instagram['mentions'])}\n")
    
    def _verify_originality(self, idea):
        """Check content idea for originality markers"""
        # Simple check for originality: look for plagiarism indicators
        plagiarism_indicators = [
            "as seen on",
            "according to",
            "quoted from",
            "in the words of",
            "as stated in"
        ]
        
        # Check concept and hook for suspicious phrases
        text_to_check = (idea['concept'] + " " + idea['hook']).lower()
        suspicious_phrases = [phrase for phrase in plagiarism_indicators if phrase in text_to_check]
        
        if suspicious_phrases:
            idea['originality_score'] = 0.6
            idea['suspicious_phrases'] = suspicious_phrases
            print(f"  ⚠️ Warning: Content idea may not be fully original. Score: {idea['originality_score']}")
        else:
            idea['originality_score'] = 0.95
        
        return idea['originality_score'] > 0.8
    
    def _generate_audio_for_content(self, content_id, idea, script, voice_gender='random', mood='upbeat'):
        """Generate audio files (voiceover + background) for a content idea"""
        # Generate voiceover
        voiceover_path = self.audio_generator.generate_voiceover(content_id, script, voice_gender)
        
        if not voiceover_path:
            logger.error(f"Failed to generate voiceover for content #{content_id}")
            return False
        
        # Generate background music
        music_path = self.audio_generator.generate_background_music(content_id, duration=30, mood=mood)
        
        # Mix audio
        if voiceover_path and music_path:
            final_audio = self.audio_generator.mix_audio(content_id, voiceover_path, music_path)
            if final_audio:
                return True
        
        return False
    
    def _create_placeholder_videos(self, content_ideas):
        """Create simple placeholder videos using the generated audio"""
        try:
            # Check for required libraries
            from moviepy.editor import AudioFileClip, TextClip, ColorClip, CompositeVideoClip
            import numpy as np
            
            print("\nCreating placeholder videos with audio...")
            
            for i, idea in enumerate(content_ideas):
                content_id = i + 1
                content_dir = os.path.join('export', f'content_idea_{content_id}')
                final_audio_path = os.path.join(content_dir, 'final_audio.mp3')
                video_path = os.path.join(content_dir, 'video.mp4')
                
                # Skip if video already exists or audio doesn't exist
                if os.path.exists(video_path) or not os.path.exists(final_audio_path):
                    continue
                
                try:
                    # Load audio
                    audio = AudioFileClip(final_audio_path)
                    duration = audio.duration
                    
                    # Create a background
                    size = (1080, 1920)  # Vertical video for shorts/reels
                    background = ColorClip(size, color=(25, 25, 25), duration=duration)
                    
                    # Create title text
                    txt_clip = TextClip(idea['title'], fontsize=70, color='white', font='Arial-Bold', 
                                      align='center', size=(900, None))
                    txt_clip = txt_clip.set_position(('center', 500)).set_duration(duration)
                    
                    # Create subtitle text (hook)
                    subtitle = TextClip(idea['hook'], fontsize=40, color='white', font='Arial', 
                                      align='center', size=(800, None), method='caption')
                    subtitle = subtitle.set_position(('center', 700)).set_duration(duration)
                    
                    # Compose video
                    video = CompositeVideoClip([background, txt_clip, subtitle])
                    video = video.set_audio(audio)
                    
                    # Write to file
                    video.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')
                    print(f"  ✓ Created placeholder video for Content Idea #{content_id}: {idea['title']}")
                    
                except Exception as e:
                    logger.error(f"Error creating placeholder video for content #{content_id}: {str(e)}")
                    print(f"  ✗ Failed to create video for Content Idea #{content_id}: {str(e)}")
                    
        except ImportError:
            print("\nCould not create placeholder videos. Please install moviepy: pip install moviepy")
            return False
        
        return True
    
    def _check_content_for_upload(self, content_ideas):
        """Check which content has video files ready for upload"""
        content_ids = []
        
        for i, _ in enumerate(content_ideas, 1):
            content_dir = os.path.join('export', f'content_idea_{i}')
            video_path = os.path.join(content_dir, 'video.mp4')
            
            if os.path.exists(video_path):
                content_ids.append(i)
        
        return content_ids
    
    def _display_upload_results(self, results):
        """Display the results of content uploads"""
        print("\nUpload Results:")
        
        for result in results:
            content_id = result.get('content_id')
            title = result.get('title')
            
            if 'error' in result:
                print(f"  Content #{content_id}: {title} - FAILED - {result['error']}")
                continue
            
            print(f"  Content #{content_id}: {title}")
            
            for platform, platform_result in result.get('platforms', {}).items():
                if 'error' in platform_result:
                    print(f"    {platform.title()}: FAILED - {platform_result['error']}")
                else:
                    print(f"    {platform.title()}: SUCCESS - {platform_result.get('url', 'No URL available')}")
    
    def _schedule_content(self, content_ids):
        """Schedule content for future publication"""
        if not content_ids:
            print("No content available for scheduling.")
            return
        
        print("\nSchedule content for publication:")
        print("\nEnter the date for publication (YYYY-MM-DD), or press Enter for tomorrow:")
        date_input = input("> ")
        
        # Use default date if none provided
        schedule_date = date_input if date_input else None
        
        # Ask if they want staggered release
        stagger = input("\nStagger release times? (30 min between each post) (y/n): ").lower() == 'y'
        
        print("\nScheduling content...")
        schedule_results = self.content_uploader.schedule_content(
            content_ids, 
            schedule_date=schedule_date,
            stagger=stagger
        )
        
        # Display scheduling results
        print("\nScheduling Results:")
        
        if isinstance(schedule_results, dict) and 'error' in schedule_results:
            print(f"  ERROR: {schedule_results['error']}")
            return
        
        for result in schedule_results:
            content_id = result.get('content_id')
            scheduled_for = result.get('scheduled_for')
            
            if 'error' in result:
                print(f"  Content #{content_id}: FAILED - {result['error']}")
                continue
            
            print(f"  Content #{content_id}: Scheduled for {scheduled_for}")
            
            for platform, platform_result in result.get('platforms', {}).items():
                if 'error' in platform_result:
                    print(f"    {platform.title()}: FAILED - {platform_result['error']}")
                else:
                    platform_time = platform_result.get('scheduled_for', scheduled_for)
                    print(f"    {platform.title()}: Scheduled for {platform_time}")
    
    def _analyze_performance(self, niche):
        print("\nAnalyzing your content performance across platforms...")
        performance_data = self.performance_analyzer.analyze()
        
        print("\nBased on your performance data, here are the adjustments for future content:")
        adjustments = self.performance_analyzer.suggest_adjustments(performance_data, niche)
        
        for platform, suggestions in adjustments.items():
            print(f"\n{platform} Adjustments:")
            for suggestion in suggestions[:3]:
                print(f"- {suggestion}")


if __name__ == "__main__":
    try:
        app = SocialMediaAutomation()
        app.run()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        print(f"\nAn error occurred: {str(e)}")
        print("Check the log file for details")
