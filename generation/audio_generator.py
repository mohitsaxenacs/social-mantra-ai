import os
import logging
import json
import requests
import time
from datetime import datetime
import random
from gtts import gTTS
from pydub import AudioSegment
from pydub.generators import Sine

logger = logging.getLogger(__name__)

class AudioGenerator:
    def __init__(self):
        """Initialize the audio generator for voice and music"""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.data_dir = os.path.join('data', 'audio')
        self.export_dir = os.path.join('export')
        
        # Create necessary directories
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Voice settings (default to English)
        self.language = 'en'
        self.voice_type = 'en-US'
        
        # Available voices for English
        self.available_voices = {
            'male': ['en-US-Standard-B', 'en-US-Standard-D', 'en-US-Standard-I', 'en-US-Standard-J'],
            'female': ['en-US-Standard-A', 'en-US-Standard-C', 'en-US-Standard-E', 'en-US-Standard-F']
        }
    
    def generate_script(self, content_idea):
        """Generate a voiceover script based on content idea"""
        logger.info(f"Generating voiceover script for: {content_idea['title']}")
        
        # Use OpenAI API if available, otherwise generate a basic script
        if self.openai_api_key:
            return self._generate_script_with_openai(content_idea)
        else:
            return self._generate_basic_script(content_idea)
    
    def _generate_script_with_openai(self, content_idea):
        """Generate an engaging voiceover script using OpenAI API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Create prompt for script generation
            prompt = f"""Write an engaging 30-60 second voiceover script for a short-form video with the following details:

Title: {content_idea['title']}
Concept: {content_idea['concept']}
Target Audience: {content_idea['target_audience']}
Hook: {content_idea['hook']}
Key Points: {', '.join(content_idea['key_points'])}

The script should:
1. Start with a powerful hook to grab attention in the first 3 seconds
2. Cover all the key points concisely
3. Include a strong call-to-action at the end
4. Be natural, conversational, and engaging (written for speaking, not reading)
5. Be properly timed for a short-form video (30-60 seconds when read at a normal pace)
6. Be COMPLETELY ORIGINAL content that won't trigger copyright issues

Format the response as plain text script ready for voiceover recording.
"""
            
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': 'You are an expert short-form video scriptwriter.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 500
            }
            
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            
            if response.status_code == 200:
                script = response.json()['choices'][0]['message']['content'].strip()
                
                # Save the script
                script_file = os.path.join(self.data_dir, f"{content_idea['title'].replace(' ', '_')}_script.txt")
                with open(script_file, 'w', encoding='utf-8') as f:
                    f.write(script)
                
                return script
            else:
                logger.error(f"OpenAI API error: {response.text}")
                return self._generate_basic_script(content_idea)
                
        except Exception as e:
            logger.error(f"Error generating script with OpenAI: {str(e)}")
            return self._generate_basic_script(content_idea)
    
    def _generate_basic_script(self, content_idea):
        """Generate a basic script from content idea structure"""
        # Create a simple script based on content structure
        script = f"Hey there! Today we're talking about {content_idea['title']}.\n\n"
        
        # Add hook
        script += f"{content_idea['hook']}\n\n"
        
        # Add key points
        for i, point in enumerate(content_idea['key_points'][:3], 1):
            script += f"Point {i}: {point}\n"
        
        # Add closing call to action
        script += f"\nThat's it for today's quick tip on {content_idea['title']}. "
        script += "If you found this helpful, like and follow for more content like this!"
        
        # Save the script
        script_file = os.path.join(self.data_dir, f"{content_idea['title'].replace(' ', '_')}_script.txt")
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script)
        
        return script
    
    def generate_voiceover(self, content_id, script, voice_gender='random'):
        """Generate a voiceover audio file from script"""
        logger.info(f"Generating voiceover for content #{content_id}")
        
        # Create directory if it doesn't exist
        content_dir = os.path.join(self.export_dir, f'content_idea_{content_id}')
        os.makedirs(content_dir, exist_ok=True)
        
        # Output file path
        voice_path = os.path.join(content_dir, 'voiceover.mp3')
        
        # If ElevenLabs API key is available, use that for higher quality
        if self.elevenlabs_api_key:
            try:
                success = self._generate_with_elevenlabs(script, voice_path, voice_gender)
                if success:
                    return voice_path
            except Exception as e:
                logger.error(f"Error with ElevenLabs TTS: {str(e)}")
                # Fall back to gTTS
        
        # Use Google Text-to-Speech as fallback
        try:
            # Select voice gender
            if voice_gender == 'random':
                voice_gender = random.choice(['male', 'female'])
            
            # Create TTS object
            tts = gTTS(text=script, lang=self.language, slow=False)
            
            # Save to file
            tts.save(voice_path)
            logger.info(f"Generated voiceover saved to {voice_path}")
            
            return voice_path
            
        except Exception as e:
            logger.error(f"Error generating voiceover: {str(e)}")
            return None
    
    def _generate_with_elevenlabs(self, script, output_path, voice_gender):
        """Generate high-quality voiceover using ElevenLabs API"""
        try:
            # Choose voice based on gender preference
            voice_id = "pNInz6obpgDQGcFmaJgB"  # Default male voice
            if voice_gender == 'female':
                voice_id = "EXAVITQu4vr4xnSDxMaL"  # Female voice
            
            # API endpoint
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            # Request headers
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            # Request body
            data = {
                "text": script,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            # Make the request
            response = requests.post(url, json=data, headers=headers)
            
            # Check if request was successful
            if response.status_code == 200:
                # Save the audio file
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                logger.info(f"ElevenLabs voiceover generated and saved to {output_path}")
                return True
            else:
                logger.error(f"ElevenLabs API error: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error with ElevenLabs TTS: {str(e)}")
            return False
    
    def generate_background_music(self, content_id, duration=30, mood='upbeat'):
        """Generate or select background music for video"""
        logger.info(f"Generating background music for content #{content_id}")
        
        # Create directory if it doesn't exist
        content_dir = os.path.join(self.export_dir, f'content_idea_{content_id}')
        os.makedirs(content_dir, exist_ok=True)
        
        # Output file path
        music_path = os.path.join(content_dir, 'background_music.mp3')
        
        # In a real application, you might use a music API or have a library of licensed tracks
        # For this demo, we'll create a simple tone or select from sample files
        
        try:
            # Check if we have sample music files available
            sample_dir = os.path.join('assets', 'music')
            if os.path.exists(sample_dir) and len(os.listdir(sample_dir)) > 0:
                # Select a random music file based on mood
                mood_files = [f for f in os.listdir(sample_dir) if mood in f.lower() and f.endswith('.mp3')]
                
                if not mood_files:
                    # If no matching mood, select any music file
                    mood_files = [f for f in os.listdir(sample_dir) if f.endswith('.mp3')]
                
                if mood_files:
                    selected_file = random.choice(mood_files)
                    music_file = os.path.join(sample_dir, selected_file)
                    
                    # Load the file and adjust duration
                    music = AudioSegment.from_mp3(music_file)
                    
                    # Trim or loop to match desired duration
                    target_duration = duration * 1000  # Convert to milliseconds
                    if len(music) > target_duration:
                        # Trim
                        music = music[:target_duration]
                    else:
                        # Loop
                        loops_needed = int(target_duration / len(music)) + 1
                        music = music * loops_needed
                        music = music[:target_duration]
                    
                    # Save the file
                    music.export(music_path, format="mp3")
                    logger.info(f"Background music saved to {music_path}")
                    
                    return music_path
            
            # If no sample files available, generate a simple tone
            # Generate a simple sine wave as background music (for demo purposes)
            frequency = 440  # A4 note
            if mood == 'upbeat':
                frequency = 523  # C5 note
            elif mood == 'calm':
                frequency = 392  # G4 note
            elif mood == 'dramatic':
                frequency = 349  # F4 note
            
            # Generate tone
            sine_wave = Sine(frequency)
            audio = sine_wave.to_audio_segment(duration=duration*1000)  # Duration in milliseconds
            
            # Fade in and out
            fade_duration = min(1000, duration*1000/4)  # 1 second or 1/4 of duration, whichever is shorter
            audio = audio.fade_in(fade_duration).fade_out(fade_duration)
            
            # Reduce volume
            audio = audio - 20  # Reduce by 20dB
            
            # Save the file
            audio.export(music_path, format="mp3")
            logger.info(f"Generated background tone saved to {music_path}")
            
            return music_path
            
        except Exception as e:
            logger.error(f"Error generating background music: {str(e)}")
            return None
    
    def mix_audio(self, content_id, voiceover_path=None, music_path=None):
        """Mix voiceover and background music"""
        logger.info(f"Mixing audio for content #{content_id}")
        
        if not voiceover_path or not os.path.exists(voiceover_path):
            logger.error(f"Voiceover file not found: {voiceover_path}")
            return None
            
        # Create directory if it doesn't exist
        content_dir = os.path.join(self.export_dir, f'content_idea_{content_id}')
        os.makedirs(content_dir, exist_ok=True)
        
        # Output file path
        final_audio_path = os.path.join(content_dir, 'final_audio.mp3')
        
        try:
            # Load voiceover
            voiceover = AudioSegment.from_mp3(voiceover_path)
            
            # If music path is provided and exists
            if music_path and os.path.exists(music_path):
                # Load background music
                music = AudioSegment.from_mp3(music_path)
                
                # Ensure music is same length as voiceover
                if len(music) < len(voiceover):
                    # Loop music if it's shorter than voiceover
                    loops_needed = int(len(voiceover) / len(music)) + 1
                    music = music * loops_needed
                
                # Trim music to match voiceover length
                music = music[:len(voiceover)]
                
                # Lower music volume to make voiceover clear
                music = music - 15  # Reduce by 15dB
                
                # Mix voiceover and music
                mixed_audio = voiceover.overlay(music)
            else:
                # If no music, just use voiceover
                mixed_audio = voiceover
            
            # Export the final mixed audio
            mixed_audio.export(final_audio_path, format="mp3")
            logger.info(f"Mixed audio saved to {final_audio_path}")
            
            return final_audio_path
            
        except Exception as e:
            logger.error(f"Error mixing audio: {str(e)}")
            return None
    
    def verify_originality(self, script):
        """Verify that the script is original content"""
        # In a real implementation, this might use a plagiarism detection API
        # For this demo, we'll use a simple check and assume OpenAI-generated content is original
        
        # Check for common indicators of non-original content
        plagiarism_indicators = [
            "as seen on",
            "according to",
            "quoted from",
            "in the words of",
            "as stated in",
            "as reported by"
        ]
        
        script_lower = script.lower()
        suspicious_phrases = [phrase for phrase in plagiarism_indicators if phrase in script_lower]
        
        if suspicious_phrases:
            logger.warning(f"Script may contain non-original content: {', '.join(suspicious_phrases)}")
            originality_score = 0.6  # Moderate risk of non-originality
        else:
            originality_score = 0.95  # High likelihood of originality
        
        return {
            'is_original': originality_score > 0.8,
            'originality_score': originality_score,
            'suspicious_phrases': suspicious_phrases
        }
