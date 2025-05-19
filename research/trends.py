import os
import json
import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class TrendResearch:
    def __init__(self):
        self.data_dir = os.path.join('data', 'trends')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def get_trending_topics(self, niche, limit=20):
        """Get trending topics related to a specific niche"""
        logger.info(f"Researching trending topics for niche: {niche}")
        
        # Try multiple methods to gather trend data
        trends = []
        
        # Method 1: OpenAI API (if key available)
        openai_trends = self._get_openai_trends(niche)
        if openai_trends:
            trends.extend(openai_trends)
        
        # Method 2: Web scraping (simulated)
        web_trends = self._get_web_trends(niche)
        if web_trends:
            trends.extend(web_trends)
        
        # Deduplicate and limit results
        unique_trends = []
        for trend in trends:
            if trend not in unique_trends:
                unique_trends.append(trend)
                if len(unique_trends) >= limit:
                    break
        
        # Save results
        self._save_data('trending_topics.json', {
            'niche': niche,
            'date': datetime.now().isoformat(),
            'topics': unique_trends
        })
        
        return unique_trends
    
    def _get_openai_trends(self, niche):
        """Get trending topics using OpenAI API"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OpenAI API key not found in environment variables")
            return []
        
        try:
            # For demonstration, using a simple API request
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': 'You are a trend research expert.'},
                    {'role': 'user', 'content': f'What are the top 15 trending topics in {niche} right now? Format as a list of topics only, one per line.'}
                ],
                'temperature': 0.7,
                'max_tokens': 500
            }
            
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            
            if response.status_code == 200:
                trends_text = response.json()['choices'][0]['message']['content']
                trends = [line.strip() for line in trends_text.split('\n') if line.strip()]
                return trends
            else:
                logger.error(f"OpenAI API error: {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting trends from OpenAI: {str(e)}")
            return []
    
    def _get_web_trends(self, niche):
        """Simulate getting trends from web sources"""
        try:
            # This is a simulation - in a real app, you would implement web scraping or use trend APIs
            # For demonstration, using sample data based on the niche
            
            # Check if cached data exists
            cached_filepath = os.path.join(self.data_dir, 'trending_topics.json')
            if os.path.exists(cached_filepath):
                with open(cached_filepath, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    
                if cached_data.get('niche') == niche:
                    logger.info(f"Using cached trend data for niche: {niche}")
                    return cached_data.get('topics', [])
            
            # Sample trends by niche (for demo purposes)
            sample_trends = {
                'cooking': [
                    'One-pot recipes', 'Air fryer hacks', 'Plant-based proteins', 
                    '15-minute meals', 'Food plating techniques', 'Meal prep ideas',
                    'Fusion cuisine', 'Sustainable cooking', 'Budget-friendly recipes',
                    'International street food', 'Dessert innovations', 'Spice blends',
                    'Breakfast upgrades', 'Fermentation techniques', 'Kitchen gadget reviews'
                ],
                'fitness': [
                    'HIIT workouts', 'Mobility training', 'Mind-muscle connection', 
                    'Home gym setups', 'Recovery techniques', 'Functional fitness',
                    'Bodyweight exercises', 'Nutrition timing', 'Workout motivation', 
                    'Progressive overload', 'Outdoor fitness challenges', 'Posture correction',
                    'Morning routines', 'Fitness tracking', 'Sport-specific training'
                ],
                'tech': [
                    'AI productivity tools', 'Smart home integration', 'Tech minimalism', 
                    'Augmented reality apps', 'Digital privacy', 'Tech sustainability',
                    'Coding challenges', 'Budget gadgets', 'Smartphone camera tips', 
                    'Remote work tech', 'Gaming optimizations', 'Tech career advice',
                    'DIY electronics', 'App customization', 'Future tech predictions'
                ],
                'beauty': [
                    'Skincare routines', 'Natural ingredients', 'Makeup techniques', 
                    'Hair transformations', 'Product reviews', 'Beauty on a budget',
                    'Seasonal trends', "Men's grooming", 'Clean beauty', 
                    'Multi-use products', 'Quick morning routines', 'Wellness integration',
                    'Cultural beauty practices', 'Beauty tool hacks', 'Ingredient deep dives'
                ],
                'gaming': [
                    'Speed running techniques', 'Hidden game features', 'Game development insights', 
                    'Budget gaming setups', 'Retro game appreciation', 'Mod showcases',
                    'Game glitches', 'Competitive strategies', 'Game narrative analysis', 
                    'Indie game reviews', 'Gaming community stories', 'Upcoming releases',
                    'Cross-platform play', 'Gaming challenge runs', 'Hardware optimization'
                ]
            }
            
            # Return trends for the specified niche, or generic trends if niche not found
            return sample_trends.get(niche.lower(), [
                'Content creation tips', 'Social media growth strategies', 
                'Storytelling techniques', 'Audience engagement', 'Trending challenges',
                'Platform-specific features', 'Collaboration ideas', 'Analytics interpretation',
                'Monetization strategies', 'Authentic personal branding', 'Visual style development',
                'Community building', 'Content repurposing', 'Algorithm updates', 'Trending sounds'
            ])
                
        except Exception as e:
            logger.error(f"Error getting web trends: {str(e)}")
            return []
    
    def _save_data(self, filename, data):
        """Save data to a JSON file"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"Trend data saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving trend data: {str(e)}")
