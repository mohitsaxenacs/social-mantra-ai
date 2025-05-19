import os
import json
import logging
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)

class PerformanceAnalyzer:
    def __init__(self):
        self.data_dir = os.path.join('data', 'analytics')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Create visualization directory
        self.viz_dir = os.path.join('export', 'analytics')
        os.makedirs(self.viz_dir, exist_ok=True)
    
    def analyze(self):
        """Analyze performance data across platforms"""
        logger.info("Analyzing content performance across platforms")
        
        # In a real implementation, this would fetch data from platform APIs
        # For now, we'll simulate with sample data or load from local storage
        
        # Check if performance data exists
        performance_file = os.path.join(self.data_dir, 'performance_data.json')
        
        if os.path.exists(performance_file):
            # Load existing data
            with open(performance_file, 'r', encoding='utf-8') as f:
                performance_data = json.load(f)
                logger.info("Loaded existing performance data")
        else:
            # Generate sample performance data
            performance_data = self._generate_sample_performance_data()
            
            # Save sample data
            with open(performance_file, 'w', encoding='utf-8') as f:
                json.dump(performance_data, f, ensure_ascii=False, indent=4)
            logger.info("Generated and saved sample performance data")
        
        # Process and visualize the data
        self._create_performance_visualizations(performance_data)
        
        return performance_data
    
    def suggest_adjustments(self, performance_data, niche):
        """Suggest content adjustments based on performance data"""
        logger.info(f"Suggesting content adjustments for niche: {niche}")
        
        # Extract insights from performance data
        platform_insights = {}
        
        for platform, videos in performance_data.items():
            # Sort videos by engagement rate for this platform
            sorted_videos = sorted(videos, key=lambda x: x['engagement_rate'], reverse=True)
            
            # Get top 3 performing videos for insights
            top_videos = sorted_videos[:3]
            
            # Extract common patterns in top videos
            titles = [video['title'] for video in top_videos]
            content_types = [video['content_type'] for video in top_videos]
            durations = [video['duration'] for video in top_videos]
            
            # Find most common content type
            if content_types:
                from collections import Counter
                most_common_type = Counter(content_types).most_common(1)[0][0]
            else:
                most_common_type = "varied"
            
            # Calculate average duration of top performing content
            avg_duration = sum(durations) / len(durations) if durations else 30
            
            # Title pattern analysis (simplified)
            has_number = any(any(c.isdigit() for c in title) for title in titles)
            has_question = any('?' in title for title in titles)
            
            # Generate platform-specific insights
            insights = {
                'top_content_type': most_common_type,
                'optimal_duration': round(avg_duration),
                'title_patterns': {
                    'uses_numbers': has_number,
                    'uses_questions': has_question
                },
                'top_videos': top_videos
            }
            
            platform_insights[platform] = insights
        
        # Generate adjustment suggestions
        adjustments = {}
        
        for platform, insights in platform_insights.items():
            platform_adjustments = []
            
            # Content type suggestion
            platform_adjustments.append(
                f"Focus on {insights['top_content_type']} content which is performing best on {platform}"
            )
            
            # Duration suggestion
            platform_adjustments.append(
                f"Aim for {insights['optimal_duration']} second videos which get optimal engagement"
            )
            
            # Title pattern suggestions
            if insights['title_patterns']['uses_numbers']:
                platform_adjustments.append(
                    f"Include numbers in your {platform} titles (e.g., '5 Ways to...', '3 Tips for...')"
                )
            
            if insights['title_patterns']['uses_questions']:
                platform_adjustments.append(
                    f"Use questions in your {platform} titles to increase curiosity"
                )
            
            # Platform-specific suggestions
            if platform == 'YouTube':
                platform_adjustments.append(
                    "Add stronger calls to action for subscribing in your YouTube videos"
                )
            elif platform == 'Instagram':
                platform_adjustments.append(
                    "Use more trending sounds and effects in your Instagram Reels"
                )
            elif platform == 'Facebook':
                platform_adjustments.append(
                    "Include more text overlays in your Facebook Reels for better retention"
                )
            
            adjustments[platform] = platform_adjustments
        
        # Add cross-platform suggestions
        cross_platform = [
            f"Repurpose successful {platform} content for other platforms with platform-specific optimizations"
            for platform in platform_insights.keys()
        ]
        
        adjustments["Cross-Platform"] = cross_platform
        
        # Save adjustment suggestions
        suggestion_file = os.path.join(self.data_dir, 'content_adjustments.json')
        with open(suggestion_file, 'w', encoding='utf-8') as f:
            json.dump(adjustments, f, ensure_ascii=False, indent=4)
        logger.info("Saved content adjustment suggestions")
        
        return adjustments
    
    def _generate_sample_performance_data(self):
        """Generate sample performance data for demonstration"""
        # Content types and titles for sample data
        content_types = ['tutorial', 'reaction', 'tips', 'challenge', 'humor', 'educational']
        
        title_templates = [
            "How to {action} Your {subject} in 30 Seconds",
            "5 {adjective} {subject} Tips You Need to Know",
            "I Tried This {adjective} {subject} Hack and It Actually Worked",
            "Why Your {subject} {problem} (And How to Fix It)",
            "The {adjective} Way to {action} Your {subject}",
            "This {subject} Trick Will Save You Hours",
            "What No One Tells You About {subject}",
            "3 Reasons Your {subject} Is Not {desired_outcome}"
        ]
        
        actions = ['improve', 'optimize', 'transform', 'upgrade', 'fix']
        subjects = ['content', 'workflow', 'strategy', 'results', 'videos', 'social media']
        adjectives = ['amazing', 'simple', 'surprising', 'game-changing', 'effective']
        problems = ['isn't working', 'is failing', 'needs improvement']
        desired_outcomes = ['growing', 'viral', 'engaging', 'converting']
        
        # Generate sample data for each platform
        platforms = ['YouTube', 'Instagram', 'Facebook']
        performance_data = {platform: [] for platform in platforms}
        
        for platform in platforms:
            # Generate 20 sample videos for each platform
            for i in range(20):
                # Create random title
                template = random.choice(title_templates)
                title = template
                
                if '{action}' in title:
                    title = title.replace('{action}', random.choice(actions))
                if '{subject}' in title:
                    title = title.replace('{subject}', random.choice(subjects))
                if '{adjective}' in title:
                    title = title.replace('{adjective}', random.choice(adjectives))
                if '{problem}' in title:
                    title = title.replace('{problem}', random.choice(problems))
                if '{desired_outcome}' in title:
                    title = title.replace('{desired_outcome}', random.choice(desired_outcomes))
                
                # Generate random metrics based on platform
                views = random.randint(500, 50000)
                likes = int(views * random.uniform(0.05, 0.3))
                comments = int(views * random.uniform(0.01, 0.08))
                shares = int(views * random.uniform(0.01, 0.1))
                
                # Slight platform variations
                if platform == 'YouTube':
                    views = int(views * random.uniform(0.8, 1.5))
                elif platform == 'Instagram':
                    likes = int(likes * random.uniform(1.2, 1.8))
                elif platform == 'Facebook':
                    shares = int(shares * random.uniform(1.5, 2.5))
                
                # Calculate engagement rate
                engagement_rate = (likes + comments + shares) / views if views > 0 else 0
                
                # Add video data
                video_data = {
                    'title': title,
                    'content_type': random.choice(content_types),
                    'publish_date': f"2024-{random.randint(1,5)}-{random.randint(1,28)}",
                    'duration': random.randint(15, 60),
                    'views': views,
                    'likes': likes,
                    'comments': comments,
                    'shares': shares,
                    'engagement_rate': engagement_rate,
                    'thumbnail_click_rate': random.uniform(0.05, 0.25),
                    'retention_rate': random.uniform(0.3, 0.9),
                    'platform': platform
                }
                
                performance_data[platform].append(video_data)
        
        return performance_data
    
    def _create_performance_visualizations(self, performance_data):
        """Create visualizations from performance data"""
        try:
            # Convert data to pandas DataFrame
            all_videos = []
            for platform, videos in performance_data.items():
                all_videos.extend(videos)
            
            if not all_videos:
                logger.warning("No performance data available for visualization")
                return
                
            df = pd.DataFrame(all_videos)
            
            # Set plot style
            sns.set(style="whitegrid")
            plt.figure(figsize=(12, 8))
            
            # 1. Engagement Rate by Platform
            plt.subplot(2, 2, 1)
            sns.barplot(x='platform', y='engagement_rate', data=df)
            plt.title('Average Engagement Rate by Platform')
            plt.xlabel('Platform')
            plt.ylabel('Engagement Rate')
            
            # 2. Average Views by Content Type
            plt.subplot(2, 2, 2)
            content_views = df.groupby(['content_type', 'platform'])['views'].mean().reset_index()
            sns.barplot(x='content_type', y='views', hue='platform', data=content_views)
            plt.title('Average Views by Content Type')
            plt.xlabel('Content Type')
            plt.ylabel('Average Views')
            plt.xticks(rotation=45)
            
            # 3. Retention Rate vs. Duration
            plt.subplot(2, 2, 3)
            sns.scatterplot(x='duration', y='retention_rate', hue='platform', data=df)
            plt.title('Retention Rate vs. Video Duration')
            plt.xlabel('Duration (seconds)')
            plt.ylabel('Retention Rate')
            
            # 4. Engagement Metrics Comparison
            plt.subplot(2, 2, 4)
            metrics = ['likes', 'comments', 'shares']
            platform_metrics = []
            
            for platform in df['platform'].unique():
                platform_df = df[df['platform'] == platform]
                for metric in metrics:
                    platform_metrics.append({
                        'platform': platform,
                        'metric': metric,
                        'value': platform_df[metric].mean()
                    })
            
            metrics_df = pd.DataFrame(platform_metrics)
            sns.barplot(x='platform', y='value', hue='metric', data=metrics_df)
            plt.title('Average Engagement Metrics by Platform')
            plt.xlabel('Platform')
            plt.ylabel('Average Count')
            
            # Adjust layout and save figure
            plt.tight_layout()
            plot_path = os.path.join(self.viz_dir, 'performance_analysis.png')
            plt.savefig(plot_path)
            logger.info(f"Created performance visualization at {plot_path}")
            
            # Create additional plots for individual platforms
            for platform in df['platform'].unique():
                platform_df = df[df['platform'] == platform]
                
                plt.figure(figsize=(10, 6))
                
                # Top Performing Content by Views
                top_views = platform_df.sort_values('views', ascending=False).head(5)
                plt.subplot(1, 2, 1)
                sns.barplot(y='title', x='views', data=top_views)
                plt.title(f'Top 5 {platform} Videos by Views')
                plt.xlabel('Views')
                plt.ylabel('')
                plt.tight_layout()
                
                # Top Performing Content by Engagement
                top_engagement = platform_df.sort_values('engagement_rate', ascending=False).head(5)
                plt.subplot(1, 2, 2)
                sns.barplot(y='title', x='engagement_rate', data=top_engagement)
                plt.title(f'Top 5 {platform} Videos by Engagement')
                plt.xlabel('Engagement Rate')
                plt.ylabel('')
                plt.tight_layout()
                
                # Save platform-specific figure
                platform_plot_path = os.path.join(self.viz_dir, f'{platform.lower()}_analysis.png')
                plt.savefig(platform_plot_path)
                logger.info(f"Created {platform} visualization at {platform_plot_path}")
                
        except Exception as e:
            logger.error(f"Error creating visualizations: {str(e)}")
