# Social Mantra AI

## Project Overview

The Social Mantra AI tool is a comprehensive solution for creating, managing, and publishing viral short-form videos across multiple social media platforms. It automates the entire content creation pipeline from research and ideation to uploading and analytics, all accessible through an intuitive Streamlit web interface.

### Supported Platforms

- YouTube Shorts
- Facebook Reels
- Instagram Reels

## Key Features

### 1. Content Research & Ideation

- **Niche-based Research**: Analyzes trending videos, top channels, and relevant topics in your specified niche
- **Trending Topic Analysis**: Identifies current trends and viral content formats
- **Idea Generation**: Creates engaging short-form video concepts with hooks and key points

### 2. Content Optimization

- **Platform-specific Metadata**: Generates optimized titles, descriptions, and tags/hashtags for each platform
- **Originality Verification**: Checks content for plagiarism indicators to ensure originality

### 3. Audio Generation

- **Script Generation**: Creates engaging scripts for voiceovers based on content ideas
- **Voiceover Creation**: Generates human-like voiceovers using either:
  - Google Text-to-Speech (gTTS) - Basic option
  - ElevenLabs API - Premium option with more natural voices
- **Background Music**: Adds mood-appropriate background music
- **Audio Mixing**: Combines voiceover and background music with appropriate levels

### 4. Video & Image Generation

- **AI-Powered Video Generation**: Creates professional-quality videos using state-of-the-art AI models
  - Free options: Stable Video Diffusion, RunwayML (limited)
  - Premium options: Runway Gen-2, Pika Labs, Midjourney Video
- **Placeholder Videos**: Generates simple text-based videos with generated audio
- **Custom Video Support**: Supports custom-created videos placed in the appropriate folder

### 5. Content Upload

- **Multi-platform Publishing**: Uploads videos to YouTube, Facebook, and Instagram simultaneously
- **Privacy Control**: Uploads as private for review before publishing
- **Metadata Application**: Automatically applies optimized metadata during upload
- **Scheduling**: Sets future publication dates and times for approved content
- **Staggered Release**: Option to release videos 30 minutes apart across platforms

### 6. Performance Analytics

- **Engagement Tracking**: Monitors views, likes, comments, and shares
- **Platform Comparison**: Compares performance across different platforms
- **Content Adjustment**: Recommends adjustments based on performance data

### 7. User-Friendly React Interface

- **Guided Setup**: Step-by-step configuration with helpful tooltips
- **API Key Management**: Secure handling of all required API keys with instructions
- **Platform Selection**: Multi-checkbox interface to select target platforms
- **Model Selection**: Options to choose between free and premium AI models for each component
- **Visual Workflow**: Visual representation of the content creation pipeline
- **Real-time Progress**: Live updates on each step of the process

## System Architecture

### Directory Structure

```
social-mantra-ai/
├── analytics/              # Analytics and performance tracking
├── assets/                 # Static assets like music
├── config/                 # Configuration files
├── data/                   # Data storage
├── export/                 # Generated content and metadata
├── generation/             # Content and audio generation
├── research/               # Trend and platform research
├── uploads/                # Platform-specific uploaders
├── frontend/               # React frontend components
│   ├── src/                # React source code
│   │   ├── components/     # UI components
│   │   ├── pages/          # Application pages
│   └── public/             # Static assets
├── backend/                # FastAPI backend
│   ├── main.py             # Main application entry point
│   ├── routes/             # API routes
│   └── models/             # Database models
├── .env                    # Environment variables (API keys, etc.)
├── .env.example            # Template for environment variables
├── requirements.txt        # Python dependencies
└── README.md               # Basic project information
```

### Module Overview

#### Research Module

- `youtube_research.py`: Analyzes YouTube trends and popular content
- `trends.py`: Tracks trending topics across platforms and general web

#### Generation Module

- `content_generator.py`: Creates content ideas and concepts
- `metadata_generator.py`: Optimizes platform-specific metadata
- `audio_generator.py`: Produces voiceovers, background music, and audio mixing
- `video_generator.py`: Handles AI video generation and processing

#### Uploads Module

- `content_uploader.py`: Manages the upload process across platforms
- `youtube_uploader.py`: Handles YouTube-specific upload functionality
- `facebook_uploader.py`: Handles Facebook-specific upload functionality
- `instagram_uploader.py`: Handles Instagram-specific upload functionality

#### Analytics Module

- `performance_analyzer.py`: Tracks content performance and suggests improvements

#### UI Module

- `frontend/`: Modern React application
- `backend/`: FastAPI backend

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- API accounts for:
  - YouTube (Google Developer Console)
  - Facebook (Facebook Developer)
  - Instagram (Creator account)
  - OpenAI (optional, for advanced content generation)
  - ElevenLabs (optional, for premium voice generation)
  - Runway ML, Pika Labs, or other video generation services (optional)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/social-mantra-ai.git
   cd social-mantra-ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the development servers:

   ```bash
   # Start the backend API server
   cd backend
   uvicorn main:app --reload
   
   # In another terminal, start the React frontend
   cd frontend
   npm start
   ```

4. Follow the guided setup in the React interface to configure your API keys and preferences.

## React UI Guide

The React UI provides an intuitive interface for configuring and running the social media automation tool. The interface is divided into several sections:

#### 1. Setup & Configuration

- **API Key Configuration**: Enter all required API keys with help tooltips explaining where to find them
- **Platform Selection**: Choose which platforms you want to target (YouTube, Facebook, Instagram)
- **Content Niche**: Specify your content niche for targeted research and generation

#### 2. Model Selection

- **Voice Generation Models**:
  - Free: Google Text-to-Speech (gTTS)
  - Premium: ElevenLabs (Recommended for quality and naturalness)

- **Video Generation Models**:
  - Free: Stable Video Diffusion, RunwayML (limited usage)
  - Premium: Runway Gen-2, Pika Labs, Midjourney Video (Recommend: Runway Gen-2 for best quality-to-cost ratio)

#### 3. Content Generation Workflow

- **Research**: Analyze trending content in your niche
- **Generate Ideas**: Create viral content concepts
- **Create Metadata**: Optimize for each platform
- **Generate Audio**: Create voiceovers and background music
- **Generate Videos**: Create engaging short-form videos
- **Upload Content**: Publish to selected platforms
- **Schedule**: Set publication times

### Basic Usage with React UI

1. Start the development servers:
   ```bash
   # Start the backend API server
   cd backend
   uvicorn main:app --reload
   
   # In another terminal, start the React frontend
   cd frontend
   npm start
   ```

2. The application will open in your default web browser

3. Follow the guided workflow in the UI:
   - Configure API keys and settings
   - Select your content niche
   - Choose target platforms
   - Run the content generation pipeline
   - Review and approve generated content
   - Upload and schedule content

### Advanced Options

The React UI provides advanced options for power users:

- **Custom Script Editing**: Manually edit generated scripts before voiceover creation
- **Custom Prompt Engineering**: Fine-tune the prompts used for content generation
- **Advanced Scheduling**: Set complex publishing schedules across platforms
- **Batch Processing**: Generate multiple batches of content at once

### Workflow Steps

#### 1. Research & Idea Generation

The application begins by researching your specified niche across platforms to identify trending content and topics. It then generates 10 content ideas with hooks and key points designed for virality on short-form video platforms.

#### 2. Metadata Generation

For each content idea, the system creates optimized metadata tailored to each platform:
- **YouTube**: Title, description, tags, category
- **Facebook**: Title, description, hashtags, call-to-action
- **Instagram**: Caption, hashtags, mentions

#### 3. Audio Generation

The system generates a script for each content idea and creates:
- A voiceover using either gTTS or ElevenLabs
- Background music that matches the content mood
- A mixed audio file combining voiceover and background music

#### 4. Video Creation

Users can either:
- Create their own videos and place them in the content_idea_X folder
- Use the system's placeholder video generator which creates a simple video using the title, hook, and generated audio

#### 5. Content Upload

The system uploads videos with all metadata to the selected platforms. By default, uploads are set to private for review before publication.

#### 6. Content Scheduling

After reviewing the uploaded private videos, users can schedule them for public release at specific dates and times. The system supports staggered release to optimize engagement across platforms.

#### 7. Performance Analysis

The system can analyze the performance of published content and suggest adjustments for future content to improve engagement and virality.

## API Integrations

### YouTube API

Used for:
- Researching trending videos and topics
- Uploading videos as YouTube Shorts
- Setting privacy settings (private/public)
- Scheduling future publications
- Retrieving performance metrics

### Facebook Graph API

Used for:
- Uploading videos as Facebook Reels
- Setting privacy settings
- Scheduling posts
- Retrieving engagement metrics

### Instagram API (via Instagrapi)

Used for:
- Uploading videos as Instagram Reels
- Setting visibility options
- Retrieving engagement metrics

### OpenAI API (Optional)

Used for:
- Enhanced content generation
- Script writing
- Metadata optimization

### ElevenLabs API (Optional)

Used for:
- High-quality voiceover generation with natural-sounding voices
- Multiple voice options and styles

## Troubleshooting

### Common Issues

1. **API Authentication Errors**
   - Ensure all API keys and credentials in the `.env` file are correct
   - Check that API access is enabled in respective developer consoles
   - Verify your API quotas haven't been exceeded

2. **Upload Failures**
   - Check your internet connection
   - Verify video format matches platform requirements
   - Ensure video duration is appropriate for short-form content
   - Check platform-specific error messages in the log

3. **Audio Generation Issues**
   - If using ElevenLabs, verify API key and quota
   - For gTTS issues, check internet connection
   - Ensure required directories exist

### Logs

The application logs detailed information to `app.log`. Check this file for debugging information when issues occur.

## Security Considerations

- API keys and credentials are stored in the `.env` file, which should never be committed to version control
- The application uses OAuth2 for YouTube authentication for enhanced security
- Credentials are loaded from environment variables rather than hardcoded

## Future Enhancements

- Web UI for easier interaction
- More advanced video editing capabilities
- Additional social media platforms (TikTok, Twitter)
- AI-powered content optimization
- Enhanced analytics dashboard
- Batch processing of multiple niches

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, bug reports, or feature requests, please open an issue on the GitHub repository or contact the development team.

---

## Appendix: Platform-Specific Notes

### YouTube Shorts

- Videos must be vertical (9:16 aspect ratio)
- Maximum duration: 60 seconds
- Use #Shorts in the description for better discovery

### Facebook Reels

- Videos must be vertical (9:16 aspect ratio)
- Duration: 15-30 seconds optimal (max 60 seconds)
- Hashtags improve discoverability

### Instagram Reels

- Videos must be vertical (9:16 aspect ratio)
- Duration: 15-30 seconds optimal (max 60 seconds)
- Use relevant hashtags (max 30) for improved reach
