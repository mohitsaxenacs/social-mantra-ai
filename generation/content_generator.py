import os
import json
import logging
import random
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.data_dir = os.path.join('data', 'content')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def generate_ideas(self, niche, trending_videos, top_channels, trending_topics, count=10):
        """Generate content ideas based on research data"""
        logger.info(f"Generating {count} content ideas for niche: {niche}")
        
        # Create prompt based on research data
        prompt = self._create_generation_prompt(niche, trending_videos, top_channels, trending_topics, count)
        
        # Generate ideas using OpenAI API (if available) or fallback to sample data
        if self.api_key:
            ideas = self._generate_with_openai(prompt, count)
        else:
            ideas = self._generate_sample_ideas(niche, trending_topics, count)
        
        # Save ideas to file
        self._save_data('content_ideas.json', {
            'niche': niche,
            'date': datetime.now().isoformat(),
            'ideas': ideas
        })
        
        return ideas
    
    def _create_generation_prompt(self, niche, trending_videos, top_channels, trending_topics, count):
        """Create a detailed prompt for content generation"""
        # Extract relevant information from research data
        top_video_titles = [video['title'] for video in trending_videos[:10]] if trending_videos else []
        top_channel_names = [channel['title'] for channel in top_channels[:5]] if top_channels else []
        
        # Build the prompt
        prompt = f"""Generate {count} viral short-form video ideas for {niche} content to post on YouTube Shorts, Instagram Reels, and Facebook Reels.

The ideas should be inspired by these trending topics in {niche}:
{', '.join(trending_topics[:10]) if trending_topics else 'general trending topics'}

These are currently popular video titles in this niche:
{', '.join(top_video_titles) if top_video_titles else 'no specific titles available'}

Top channels in this niche include:
{', '.join(top_channel_names) if top_channel_names else 'no specific channels available'}

For each idea, provide:
1. An attention-grabbing title
2. A brief concept description (30-50 words)
3. Target audience
4. A strong hook for the first 3 seconds
5. 3-5 key points to cover

The ideas should be original, highly engaging, and optimized for short-form vertical video format.
Focus on content that creates curiosity, provides value, shows personality, and encourages sharing.
Each video concept should be 15-60 seconds long.

Format the response as a list of JSON objects with these exact fields: title, concept, target_audience, hook, key_points (as an array).
"""
        return prompt
    
    def _generate_with_openai(self, prompt, count):
        """Generate content ideas using OpenAI API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': 'You are a viral content strategist for short-form videos.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.8,
                'max_tokens': 2000
            }
            
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                
                # Parse the response - expecting a JSON array or JSON-like format
                try:
                    # Try to parse as JSON directly
                    if result.strip().startswith('[') and result.strip().endswith(']'):
                        ideas = json.loads(result)
                    else:
                        # If not valid JSON, try to extract JSON-like content
                        import re
                        json_pattern = r'\[\s*{.*}\s*\]'
                        json_match = re.search(json_pattern, result, re.DOTALL)
                        
                        if json_match:
                            ideas = json.loads(json_match.group(0))
                        else:
                            # Fallback to sample ideas
                            logger.warning("Failed to parse OpenAI response as JSON")
                            return self._generate_sample_ideas(None, None, count)
                            
                    return ideas[:count]  # Limit to requested count
                    
                except json.JSONDecodeError:
                    logger.error("Failed to parse OpenAI response as JSON")
                    return self._generate_sample_ideas(None, None, count)
            else:
                logger.error(f"OpenAI API error: {response.text}")
                return self._generate_sample_ideas(None, None, count)
                
        except Exception as e:
            logger.error(f"Error generating content with OpenAI: {str(e)}")
            return self._generate_sample_ideas(None, None, count)
    
    def _generate_sample_ideas(self, niche, trending_topics, count):
        """Generate sample content ideas when API is not available"""
        logger.info("Using sample content ideas")
        
        # Load any cached ideas if available
        cached_filepath = os.path.join(self.data_dir, 'content_ideas.json')
        if os.path.exists(cached_filepath):
            try:
                with open(cached_filepath, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    
                if cached_data.get('niche') == niche and len(cached_data.get('ideas', [])) >= count:
                    logger.info(f"Using cached content ideas for niche: {niche}")
                    return cached_data.get('ideas', [])[:count]
            except Exception:
                pass
        
        # Sample ideas for different niches
        sample_ideas = {
            'cooking': [
                {
                    'title': '3 Pasta Hacks Chefs Don't Want You To Know',
                    'concept': 'Quick demonstration of professional pasta cooking techniques that elevate home cooking with minimal effort.',
                    'target_audience': 'Home cooks looking to improve basic skills',
                    'hook': 'The secret to restaurant-quality pasta isn't what you think...',
                    'key_points': ['Salt water properly', 'Reserve pasta water', 'Finish cooking in sauce']
                },
                {
                    'title': 'This 5-Minute Air Fryer Dessert Will Change Your Life',
                    'concept': 'Super quick air fryer dessert recipe that requires minimal ingredients but delivers maximum flavor.',
                    'target_audience': 'Busy people with a sweet tooth',
                    'hook': 'What if I told you the perfect dessert takes just 5 minutes?',
                    'key_points': ['Simple ingredients', 'Air fryer technique', 'Versatile variations', 'No baking skills required']
                },
                {
                    'title': 'The One-Pan Breakfast That Makes Your Morning Easier',
                    'concept': 'Demonstrating an efficient one-pan breakfast method that saves time and dishes while being nutritionally complete.',
                    'target_audience': 'Busy professionals and parents',
                    'hook': 'The secret to a perfect breakfast with zero morning stress...',
                    'key_points': ['Prep ahead option', 'Balanced macros', 'Minimal cleanup', 'Customization ideas']
                }
            ],
            'fitness': [
                {
                    'title': '30-Second Stretch That Fixes Posture Immediately',
                    'concept': 'Quick demonstration of one highly effective stretch that counters desk posture and phone neck.',
                    'target_audience': 'Office workers and tech users',
                    'hook': 'Your neck pain might disappear after this 30-second fix...',
                    'key_points': ['Proper technique', 'Why it works', 'How often to do it', 'Common mistakes']
                },
                {
                    'title': 'The Only 3 Exercises You Need for Defined Arms',
                    'concept': 'Showcasing three compound exercises that efficiently target all arm muscles for definition and strength.',
                    'target_audience': 'Fitness enthusiasts looking for efficiency',
                    'hook': 'Forget the 30-minute arm workout, these 3 moves are all you need...',
                    'key_points': ['Proper form', 'Weight progression', 'Frequency recommendation', 'Common mistakes to avoid']
                },
                {
                    'title': 'Try This Morning Routine for All-Day Energy (No Coffee)',
                    'concept': 'Quick morning movement routine that activates the body and boosts energy naturally without caffeine.',
                    'target_audience': 'Health-conscious individuals seeking natural energy',
                    'hook': 'What if you could feel more energized than coffee in just 2 minutes?',
                    'key_points': ['Morning light exposure', 'Quick movement sequence', 'Hydration tip', 'Breathing technique']
                }
            ],
            'tech': [
                {
                    'title': 'iPhone Hidden Feature You're Not Using (But Should)',
                    'concept': 'Revealing an underutilized iPhone feature that significantly improves productivity or security.',
                    'target_audience': 'iPhone users of all levels',
                    'hook': 'This hidden iPhone setting saves me 30 minutes every day...',
                    'key_points': ['Where to find it', 'How to set up', 'Use case examples', 'Why it matters']
                },
                {
                    'title': 'This AI Tool Does Your Homework Better Than ChatGPT',
                    'concept': 'Introducing a specialized AI tool that outperforms ChatGPT for specific educational tasks.',
                    'target_audience': 'Students and lifelong learners',
                    'hook': 'The AI tool students are using that teachers haven't caught onto yet...',
                    'key_points': ['Tool demonstration', 'Comparison to ChatGPT', 'Best use cases', 'Tips for best results']
                },
                {
                    'title': '10-Second Hack to Make Your WiFi Twice as Fast',
                    'concept': 'Simple router positioning or setting adjustment that drastically improves WiFi performance in most homes.',
                    'target_audience': 'Anyone frustrated with home internet speeds',
                    'hook': 'Your WiFi is slow because of this one simple mistake...',
                    'key_points': ['Common router mistake', 'Simple fix demonstration', 'Before/after speed test', 'Additional optimization tips']
                }
            ]
        }
        
        # Generic ideas for any niche
        generic_ideas = [
            {
                'title': 'I Tested Viral TikTok Hacks So You Don't Have To',
                'concept': 'Testing popular viral hacks related to the niche to determine which ones actually work.',
                'target_audience': 'Curious skeptics who enjoy debunking content',
                'hook': 'This viral hack with millions of views actually made things worse...',
                'key_points': ['Hack overview', 'Testing process', 'Results', 'Better alternatives']
            },
            {
                'title': '5 Things Beginners Always Get Wrong About [NICHE]',
                'concept': 'Identifying common misconceptions or mistakes that newcomers make in the niche with simple corrections.',
                'target_audience': 'Beginners and intermediate enthusiasts',
                'hook': 'The #1 mistake is so common, I see it every single day...',
                'key_points': ['Common misconceptions', 'Simple fixes', 'Expert demonstration', 'Resource recommendations']
            },
            {
                'title': 'The 80/20 Rule of [NICHE]: Focus on This for Results',
                'concept': 'Applying the Pareto principle to show which 20% of efforts produce 80% of results in the niche.',
                'target_audience': 'Efficiency-focused individuals in the niche',
                'hook': 'Stop wasting time on things that don't matter in [NICHE]...',
                'key_points': ['High-impact activities', 'What to minimize', 'Expert examples', 'Implementation strategy']
            },
            {
                'title': 'What [Top Influencer] Does Behind The Scenes That Nobody Sees',
                'concept': 'Revealing the less glamorous but critical aspects of success in the niche that top creators don't show.',
                'target_audience': 'Aspiring creators and niche enthusiasts',
                'hook': 'The real reason [influencer] succeeded isn't what they show on camera...',
                'key_points': ['Reality vs. perception', 'Critical behind-scenes work', 'Common misconceptions', 'Actionable takeaways']
            },
            {
                'title': 'Why Most People Fail at [NICHE] (And How to Succeed)',
                'concept': 'Analyzing common patterns of failure in the niche and providing a framework for success.',
                'target_audience': 'Motivated individuals who have struggled to make progress',
                'hook': '95% of people quit [NICHE] because of this one mistake...',
                'key_points': ['Common failure pattern', 'Mindset shift needed', 'Systematic approach', 'Success examples']
            },
            {
                'title': 'The 30-Day [NICHE] Challenge That Actually Works',
                'concept': 'Outlining a structured 30-day progressive challenge that delivers meaningful results in the niche.',
                'target_audience': 'Action-takers looking for a structured approach',
                'hook': 'This 30-day challenge transformed my [relevant outcome]...',
                'key_points': ['Challenge structure', 'Daily commitment', 'Expected obstacles', 'Results timeline']
            },
            {
                'title': 'I Spent $1000 Testing [NICHE Products/Services] - Here's What's Worth It',
                'concept': 'Sharing results from extensive testing of products or services in the niche to identify the best value.',
                'target_audience': 'Consumers researching purchases in the niche',
                'hook': 'Save your money - this popular [product] completely failed our test...',
                'key_points': ['Testing methodology', 'Surprising winners', 'Overhyped failures', 'Best value options']
            }
        ]
        
        # Select ideas based on niche or use generic ideas
        selected_ideas = []
        niche_specific_ideas = sample_ideas.get(niche.lower(), []) if niche else []
        
        # Add niche-specific ideas first
        selected_ideas.extend(niche_specific_ideas)
        
        # Add generic ideas with niche inserted into title/content
        for idea in generic_ideas:
            if len(selected_ideas) >= count:
                break
                
            # Clone the idea and customize it for the niche if available
            customized_idea = idea.copy()
            if niche:
                customized_idea['title'] = customized_idea['title'].replace('[NICHE]', niche.title())
                customized_idea['concept'] = customized_idea['concept'].replace('[NICHE]', niche.lower())
                customized_idea['hook'] = customized_idea['hook'].replace('[NICHE]', niche.lower())
                
            selected_ideas.append(customized_idea)
        
        # If we still need more ideas, create variations
        while len(selected_ideas) < count:
            # Take a random idea and create a variation
            base_idea = random.choice(selected_ideas)
            variation = base_idea.copy()
            
            # Modify the title and content slightly
            if 'Top' in variation['title']:
                variation['title'] = variation['title'].replace('Top', 'Best')
            elif '5' in variation['title']:
                variation['title'] = variation['title'].replace('5', '7')
            elif 'This' in variation['title']:
                variation['title'] = variation['title'].replace('This', 'Try This')
            else:
                variation['title'] = 'Why ' + variation['title']
                
            # Add to selected ideas
            selected_ideas.append(variation)
        
        return selected_ideas[:count]
    
    def _save_data(self, filename, data):
        """Save data to a JSON file"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"Content ideas saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving content ideas: {str(e)}")
