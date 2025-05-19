import os
import json
import logging
import random
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class MetadataGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.data_dir = os.path.join('data', 'metadata')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def for_youtube(self, idea):
        """Generate optimized metadata for YouTube Shorts"""
        logger.info(f"Generating YouTube metadata for idea: {idea['title']}")
        
        if self.api_key:
            return self._generate_with_openai('youtube', idea)
        else:
            return self._generate_sample_metadata('youtube', idea)
    
    def for_facebook(self, idea):
        """Generate optimized metadata for Facebook Reels"""
        logger.info(f"Generating Facebook metadata for idea: {idea['title']}")
        
        if self.api_key:
            return self._generate_with_openai('facebook', idea)
        else:
            return self._generate_sample_metadata('facebook', idea)
    
    def for_instagram(self, idea):
        """Generate optimized metadata for Instagram Reels"""
        logger.info(f"Generating Instagram metadata for idea: {idea['title']}")
        
        if self.api_key:
            return self._generate_with_openai('instagram', idea)
        else:
            return self._generate_sample_metadata('instagram', idea)
    
    def _generate_with_openai(self, platform, idea):
        """Generate platform-specific metadata using OpenAI API"""
        try:
            # Create prompt based on platform and idea
            prompt = self._create_platform_prompt(platform, idea)
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': 'You are a social media metadata optimization expert.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 1000
            }
            
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                
                # Parse the response - expecting a JSON object
                try:
                    # Try to parse as JSON directly
                    if result.strip().startswith('{') and result.strip().endswith('}'): 
                        metadata = json.loads(result)
                    else:
                        # If not valid JSON, try to extract JSON-like content
                        import re
                        json_pattern = r'\{.*\}'
                        json_match = re.search(json_pattern, result, re.DOTALL)
                        
                        if json_match:
                            metadata = json.loads(json_match.group(0))
                        else:
                            # Fallback to sample metadata
                            logger.warning("Failed to parse OpenAI response as JSON")
                            return self._generate_sample_metadata(platform, idea)
                            
                    # Save metadata to file
                    self._save_data(f"{platform}_metadata.json", {
                        'idea': idea['title'],
                        'date': datetime.now().isoformat(),
                        'metadata': metadata
                    })
                    
                    return metadata
                    
                except json.JSONDecodeError:
                    logger.error("Failed to parse OpenAI response as JSON")
                    return self._generate_sample_metadata(platform, idea)
            else:
                logger.error(f"OpenAI API error: {response.text}")
                return self._generate_sample_metadata(platform, idea)
                
        except Exception as e:
            logger.error(f"Error generating metadata with OpenAI: {str(e)}")
            return self._generate_sample_metadata(platform, idea)
    
    def _create_platform_prompt(self, platform, idea):
        """Create platform-specific prompt for metadata generation"""
        base_prompt = f"""Generate optimized metadata for the following short-form video idea to be posted on {platform.title()}:

Video Title: {idea['title']}
Concept: {idea['concept']}
Target Audience: {idea['target_audience']}
Hook: {idea['hook']}
Key Points: {', '.join(idea['key_points'])}

"""
        
        if platform.lower() == 'youtube':
            base_prompt += """For YouTube Shorts, please provide the following metadata optimized for maximum visibility and engagement:

1. An attention-grabbing title (max 70 characters)
2. A detailed description that front-loads important information (max 300 characters)
3. A list of 10-15 relevant tags/keywords
4. The most appropriate video category

Format the response as a JSON object with these fields: title, description, tags (as an array), category."""
        
        elif platform.lower() == 'facebook':
            base_prompt += """For Facebook Reels, please provide the following metadata optimized for maximum visibility and engagement:

1. An attention-grabbing title (max 50 characters)
2. A concise description that includes a call to action (max 200 characters)
3. A list of 5-10 relevant hashtags
4. A compelling call to action

Format the response as a JSON object with these fields: title, description, hashtags (as an array), call_to_action."""
        
        elif platform.lower() == 'instagram':
            base_prompt += """For Instagram Reels, please provide the following metadata optimized for maximum visibility and engagement:

1. A compelling caption that hooks viewers (max 250 characters)
2. A list of 15-20 relevant hashtags that mix popular and niche tags
3. A list of 1-3 relevant accounts to mention

Format the response as a JSON object with these fields: caption, hashtags (as an array), mentions (as an array)."""
        
        return base_prompt
    
    def _generate_sample_metadata(self, platform, idea):
        """Generate sample metadata when API is not available"""
        logger.info(f"Using sample metadata for {platform}")
        
        title = idea['title']
        concept = idea['concept']
        key_points = idea['key_points']
        
        if platform.lower() == 'youtube':
            # Generate YouTube metadata
            # Make title more clickable if needed
            if not any(x in title.lower() for x in ['how', 'why', 'what', '?', 'this', 'these', 'revealed']):
                title = f"How {title}"
                
            # Ensure title is not too long
            if len(title) > 70:
                title = title[:67] + '...'
            
            # Create description with key points and call to action
            description = f"{concept}\n\nIn this video:\n"
            for point in key_points[:3]:
                description += f"- {point}\n"
            description += "\nLike & Subscribe for more content like this! #shorts"
            
            # Create tags
            base_tags = [
                'shorts', 'ytshorts', 'viral', 'trending'
            ]
            
            # Add content-specific tags
            for word in title.lower().replace('?', '').replace('!', '').split():
                if len(word) > 3 and word not in ['this', 'that', 'with', 'what', 'when', 'will', 'your', 'from']:
                    base_tags.append(word)
            
            # Add extra tags based on key points
            for point in key_points:
                words = point.split()
                if words:
                    base_tags.append(words[0].lower())
            
            # Deduplicate and limit tags
            tags = []
            for tag in base_tags:
                if tag not in tags:
                    tags.append(tag)
            
            # Determine category (simplified version)
            categories = {
                'cook': 'Food',
                'recipe': 'Food',
                'food': 'Food',
                'tech': 'Science & Technology',
                'fitness': 'Sports',
                'workout': 'Sports',
                'game': 'Gaming',
                'beauty': 'People & Blogs',
                'fashion': 'People & Blogs',
                'money': 'Education',
                'finance': 'Education',
                'learn': 'Education',
                'tutorial': 'Education',
                'funny': 'Comedy',
                'comedy': 'Comedy',
                'music': 'Music'
            }
            
            category = 'Entertainment'  # Default category
            for key, value in categories.items():
                if key in title.lower() or key in concept.lower():
                    category = value
                    break
            
            return {
                'title': title,
                'description': description[:300],  # Limit to 300 chars
                'tags': tags[:15],  # Limit to 15 tags
                'category': category
            }
            
        elif platform.lower() == 'facebook':
            # Generate Facebook metadata
            # Ensure title is not too long
            if len(title) > 50:
                title = title[:47] + '...'
            
            # Create concise description with call to action
            description = f"{concept[:120]}... "
            
            # Add call to action
            call_to_actions = [
                "Follow for more!",
                "Double tap if you agree!",
                "Save this for later!",
                "Tag someone who needs to see this!",
                "Try this and let me know what you think!",
                "Drop a 🔥 if you'd try this!"
            ]
            
            call_to_action = random.choice(call_to_actions)
            description += call_to_action
            
            # Create hashtags
            hashtags = ['reels', 'viral']
            
            # Add specific hashtags based on content
            for word in title.lower().replace('?', '').replace('!', '').split():
                if len(word) > 3 and word not in ['this', 'that', 'with', 'what', 'when', 'will', 'your', 'from']:
                    hashtags.append(word)
            
            # Add one key point as hashtag
            if key_points:
                main_point = key_points[0].split()[0].lower()
                if main_point not in hashtags and len(main_point) > 3:
                    hashtags.append(main_point)
            
            # Format hashtags and limit
            formatted_hashtags = []
            for tag in hashtags:
                if tag not in formatted_hashtags:
                    formatted_hashtags.append(tag)
            
            return {
                'title': title,
                'description': description[:200],  # Limit to 200 chars
                'hashtags': formatted_hashtags[:10],  # Limit to 10 hashtags
                'call_to_action': call_to_action
            }
            
        elif platform.lower() == 'instagram':
            # Generate Instagram metadata
            # Create compelling caption
            first_line = title if len(title) < 50 else title[:47] + '...'
            
            caption_templates = [
                f"{first_line} 👀\n\n{concept[:100]}...",
                f"✨ {first_line} ✨\n\n{concept[:100]}...",
                f"I had to share this! {first_line}\n\n{concept[:100]}...",
                f"You asked, I answered: {first_line}\n\n{concept[:100]}...",
                f"Don't scroll past this! {first_line}\n\n{concept[:100]}..."
            ]
            
            caption = random.choice(caption_templates)
            
            # Add engagement prompt
            engagement_prompts = [
                "\n\nSave this for later! 💾",
                "\n\nDouble tap if you agree 💯",
                "\n\nTag someone who needs to see this 👇",
                "\n\nDrop your questions below 💬",
                "\n\nAgree or disagree? Let me know 👇"
            ]
            
            caption += random.choice(engagement_prompts)
            
            # Create hashtags - mix of popular and niche
            popular_hashtags = [
                'reels', 'instareels', 'viral', 'trending', 'fyp', 'foryoupage', 'instagram'
            ]
            
            niche_hashtags = []
            # Add content-specific hashtags
            for word in title.lower().replace('?', '').replace('!', '').split():
                if len(word) > 3 and word not in ['this', 'that', 'with', 'what', 'when', 'will', 'your', 'from']:
                    niche_hashtags.append(word)
            
            # Add key points as hashtags
            for point in key_points:
                words = point.split()
                if words:
                    word = words[0].lower()
                    if word not in niche_hashtags and len(word) > 3:
                        niche_hashtags.append(word)
            
            # Combine and format hashtags
            all_hashtags = popular_hashtags + niche_hashtags
            formatted_hashtags = []
            for tag in all_hashtags:
                if tag not in formatted_hashtags:
                    formatted_hashtags.append(tag)
            
            # Generate mentions (simplified)
            mentions = ['explore', 'viral']
            
            return {
                'caption': caption[:250],  # Limit to 250 chars
                'hashtags': formatted_hashtags[:20],  # Limit to 20 hashtags
                'mentions': mentions
            }
            
        else:
            # Generic fallback metadata
            return {
                'title': title,
                'description': concept[:200],
                'tags': [word.lower() for word in title.split() if len(word) > 3][:10]
            }
    
    def _save_data(self, filename, data):
        """Save data to a JSON file"""
        try:
            filepath = os.path.join(self.data_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"Metadata saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving metadata: {str(e)}")
