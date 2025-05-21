# Social Mantra AI - Full Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Installation Guide](#installation-guide)
4. [Application Workflow](#application-workflow)
5. [Core Components](#core-components)
6. [Web Interface (Streamlit)](#web-interface-streamlit)
7. [API Integrations](#api-integrations)
8. [Technical Details](#technical-details)
9. [Troubleshooting](#troubleshooting)
10. [Future Development](#future-development)

## System Overview

The Social Mantra AI tool is a comprehensive solution designed to automate the creation, optimization, and distribution of short-form videos across multiple social media platforms (YouTube Shorts, Facebook Reels, and Instagram Reels). The system handles the entire content pipeline from research and ideation to publishing and performance analytics.

The application integrates with various AI services for content generation, voice synthesis, and video creation, while providing a user-friendly interface through Streamlit for managing the entire workflow.

### Key Capabilities

- **Niche-based Content Research**: Analyzes trending videos, top channels, and popular topics in user-specified niches
- **Content Generation**: Creates viral-optimized short-form video concepts with engaging hooks and key points
- **Platform-specific Metadata**: Automatically generates optimized titles, descriptions, tags, and hashtags for each platform
- **Audio Creation**: Generates voiceovers using AI and combines them with appropriate background music
- **Video Generation**: Creates videos using AI models or builds placeholder videos with audio
- **Multi-platform Publishing**: Uploads content to YouTube, Facebook, and Instagram simultaneously
- **Scheduling**: Sets publication dates and times for content, with options for staggered release
- **Performance Analytics**: Tracks content performance across platforms and suggests optimization strategies

## Architecture

The application follows a modular architecture organized into distinct functional components:

```
social-media-shorts-video-automation/
│
├── analytics/              # Performance tracking and analysis
│   ├── __init__.py
│   └── performance_analyzer.py
│
├── assets/                 # Static assets like music
│   └── music/
│
├── config/                 # Configuration files
│
├── data/                   # Data storage
│   └── audio/
│
├── export/                 # Generated content and metadata
│
├── generation/             # Content and audio generation
│   ├── __init__.py
│   ├── audio_generator.py
│   ├── content_generator.py
│   ├── metadata_generator.py
│   └── video_generator.py
│
├── research/               # Trend and platform research
│   ├── __init__.py
│   ├── trends.py
│   └── youtube_research.py
│
├── uploads/                # Platform-specific uploaders
│   ├── __init__.py
│   ├── content_uploader.py
│   ├── facebook_uploader.py
│   ├── instagram_uploader.py
│   └── youtube_uploader.py
│
├── ui/                     # Streamlit UI components
│   ├── __init__.py
│   ├── components/         # Reusable UI components
│   │   ├── __init__.py
│   │   ├── api_input.py
│   │   ├── model_selector.py
│   │   └── platform_selector.py
│   │
│   ├── pages/              # Application pages
│   │   ├── __init__.py
│   │   ├── analytics.py
│   │   ├── generation.py
│   │   ├── research.py
│   │   ├── setup.py
│   │   └── upload.py
│   │
│   └── utils/              # UI utilities
│       ├── __init__.py
│       └── state_management.py
│
├── .env                    # Environment variables (API keys)
├── .env.example            # Example environment file
├── app.py                  # Streamlit application entry
├── main.py                 # Command-line application entry
├── requirements.txt        # Python dependencies
└── README.md              # Basic project information
```

### Core Modules

1. **Research**: Analyzes trending content and topics across platforms
2. **Generation**: Creates content ideas, metadata, audio, and videos
3. **Uploads**: Handles content distribution to social media platforms
4. **Analytics**: Tracks performance and provides optimization suggestions
5. **UI**: Provides a user-friendly interface for the application

## Installation Guide

### Prerequisites

- Python 3.8 or higher
- Required API accounts:
  - YouTube (Google API Console)
  - Facebook Developer Account
  - Instagram Creator Account
  - OpenAI (optional)
  - ElevenLabs (optional)
  - Video generation service (RunwayML, Pika Labs, etc. - optional)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/social-media-shorts-video-automation.git
   cd social-media-shorts-video-automation
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file to add your API keys and credentials.

5. **Launch the application**:
   - For the Streamlit UI:
     ```bash
     streamlit run app.py
     ```
   - For the command-line interface:
     ```bash
     python main.py
     ```

## Application Workflow

The application follows a five-step workflow from setup to analytics:

### 1. Setup & Configuration

- Configure API keys for various services
- Select target social media platforms
- Choose AI models for different generation tasks
- Specify content niche

### 2. Content Research

- Analyze trending content in specified niche
- Identify top-performing videos and channels
- Discover trending topics and hashtags

### 3. Content Generation

- Generate viral content ideas with hooks and key points
- Create platform-specific metadata (titles, descriptions, tags)
- Generate audio content (voiceovers and background music)
- Create videos using selected AI models or placeholder videos

### 4. Upload & Schedule

- Review generated content before uploading
- Upload content to selected platforms (as private for review)
- Schedule content for future publication
- Set staggered release times across platforms

### 5. Performance Analytics

- Track content performance across platforms
- Compare metrics between platforms
- Receive recommendations for optimization
- Start new content workflow based on insights

## Core Components

### Research Module

#### YouTubeResearch Class

Responsible for researching trending content and channels on YouTube within a specified niche.

**Key Methods**:
- `get_trending_videos(niche)`: Retrieves trending videos in the specified niche
- `get_top_channels(niche)`: Identifies top-performing channels in the niche
- `_build_youtube_client()`: Initializes the YouTube API client

#### TrendResearch Class

Analyzes trending topics across platforms and general web sources.

**Key Methods**:
- `get_trending_topics(niche)`: Retrieves trending topics related to the niche
- `_analyze_hashtags(niche)`: Analyzes popular hashtags in the niche

### Generation Module

#### ContentGenerator Class

Generates viral content ideas based on research data.

**Key Methods**:
- `generate_ideas(niche, trending_videos, top_channels, trending_topics, count=10)`: Creates content ideas with hooks and key points
- `_generate_hooks(niche)`: Creates attention-grabbing hooks for content

#### MetadataGenerator Class

Creates optimized metadata for each platform.

**Key Methods**:
- `for_youtube(idea)`: Generates YouTube-specific metadata
- `for_facebook(idea)`: Generates Facebook-specific metadata
- `for_instagram(idea)`: Generates Instagram-specific metadata

#### AudioGenerator Class

Handles audio generation, including voiceovers and background music.

**Key Methods**:
- `generate_script(idea)`: Creates a script for voiceover
- `generate_voiceover(content_id, script, voice_gender='random')`: Creates a voiceover using selected AI service
- `generate_background_music(content_id, duration=30, mood='upbeat')`: Generates or selects background music
- `mix_audio(content_id, voiceover_path, music_path)`: Combines voiceover and background music
- `verify_originality(script)`: Checks content for originality/plagiarism indicators

### Uploads Module

#### ContentUploader Class

Manages content uploads across multiple platforms.

**Key Methods**:
- `upload_content(content_ideas, private=True)`: Uploads content to selected platforms
- `schedule_content(content_ids, schedule_date=None, stagger=False)`: Schedules content for future publication

#### Platform-specific Uploaders

Handles platform-specific uploading requirements:

- **YouTubeUploader**: Uploads to YouTube Shorts
- **FacebookUploader**: Uploads to Facebook Reels
- **InstagramUploader**: Uploads to Instagram Reels

Each uploader implements:
- `upload(video_path, metadata_path, private=True)`: Uploads content with specified privacy setting
- `schedule(video_id, publish_time)`: Schedules a video for future publication

### Analytics Module

#### PerformanceAnalyzer Class

Analyzes content performance and suggests improvements.

**Key Methods**:
- `analyze()`: Retrieves and processes performance data across platforms
- `suggest_adjustments(performance_data, niche)`: Suggests content optimizations based on performance

## Web Interface (Streamlit)

The application provides a user-friendly web interface built with Streamlit.

### Main App Structure

The `app.py` file serves as the entry point for the Streamlit application:
- Initializes the application and session state
- Provides navigation through the workflow steps
- Renders the appropriate page based on the current step

### UI Pages

#### Setup Page

Displays the setup and configuration interface:
- API key management with help tooltips
- Platform selection via checkboxes
- AI model selection with recommendations
- Content niche input

#### Research Page

Shows content research results:
- Trending topics in the selected niche
- Top-performing videos and channels

#### Generation Page

Manages content generation tasks:
- Content idea generation and selection
- Metadata creation and preview
- Audio generation (voiceovers and music)
- Video generation and preview

#### Upload Page

Handles content upload and scheduling:
- Content review before uploading
- Platform selection for each piece of content
- Privacy settings (private/public)
- Publication scheduling

#### Analytics Page

Displays performance metrics and insights:
- Overview of content performance
- Platform-specific metrics
- Performance comparison between platforms
- Recommendations for optimization

### UI Components

#### API Input Component

A reusable component for securely handling API key inputs with help tooltips.

#### Platform Selector Component

Multi-checkbox interface for selecting target social media platforms.

#### Model Selector Component

Tabbed interface for selecting AI models for different generation tasks (voice, video, image).

### State Management

The application uses Streamlit's session state for managing user data and workflow progression.

**Key State Variables**:
- `current_step`: Tracks the current workflow step
- `api_keys`: Stores API keys and credentials
- `selected_platforms`: Tracks selected social media platforms
- `content_niche`: Stores the specified content niche
- `models`: Tracks selected AI models
- `content_ideas`: Stores generated content ideas
- Various completion flags to track workflow progress

## API Integrations

The application integrates with various external APIs for different functionality:

### YouTube API

**Used for**:
- Researching trending videos and channels
- Uploading videos as YouTube Shorts
- Setting privacy settings and scheduling
- Retrieving performance metrics

**Required Credentials**:
- YouTube API Key
- Client Secrets JSON file (for OAuth2 authentication)

### Facebook Graph API

**Used for**:
- Uploading videos as Facebook Reels
- Managing privacy settings and scheduling
- Retrieving engagement metrics

**Required Credentials**:
- App ID
- App Secret
- Access Token
- Page ID

### Instagram API (via Instagrapi)

**Used for**:
- Uploading videos as Instagram Reels
- Managing captions and hashtags
- Retrieving performance data

**Required Credentials**:
- Instagram username
- Instagram password

### OpenAI API (Optional)

**Used for**:
- Enhanced content generation
- Script writing
- Metadata optimization

**Required Credentials**:
- OpenAI API Key

### ElevenLabs API (Optional)

**Used for**:
- High-quality voiceover generation

**Required Credentials**:
- ElevenLabs API Key

### Video Generation APIs (Optional)

**Used for**:
- AI-powered video generation

**Options**:
- RunwayML API
- Pika Labs API

## Technical Details

### Environment Variables

The application uses the following environment variables (stored in `.env`):

```
# YouTube API credentials
YOUTUBE_API_KEY=your_youtube_api_key
YOUTUBE_CLIENT_SECRETS=path/to/your/client_secrets.json

# Facebook API credentials
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id

# Instagram credentials
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# OpenAI API (optional)
OPENAI_API_KEY=your_openai_api_key

# ElevenLabs API (optional)
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# Video generation APIs (optional)
RUNWAY_API_KEY=your_runway_api_key
PIKA_API_KEY=your_pika_api_key
```

### Dependencies

Key dependencies include:

- **API Clients**:
  - `google-api-python-client`: YouTube API client
  - `facebook-sdk`: Facebook Graph API client
  - `instagrapi`: Instagram API client
  - `openai`: OpenAI API client

- **Content Generation**:
  - `gTTS`: Google Text-to-Speech
  - `pydub`: Audio processing
  - `movie.py`: Video processing
  - `elevenlabs`: Premium voice generation

- **Data Processing**:
  - `pandas`: Data manipulation
  - `numpy`: Numerical processing

- **UI**:
  - `streamlit`: Web interface
  - `matplotlib` and `seaborn`: Data visualization

### Data Flow

1. **User Input**: Configuration data (API keys, platforms, niche)
2. **Research**: Platform APIs → Research module → Content data
3. **Generation**: Content data → Generation module → Content assets (ideas, metadata, audio, video)
4. **Upload**: Content assets → Uploads module → Social media platforms
5. **Analytics**: Social media platforms → Analytics module → Performance insights

### Security Considerations

- API keys and credentials are stored in `.env` file (not committed to version control)
- OAuth2 authentication is used for YouTube where applicable
- Instagram credentials are used directly (consider using cookies-based auth for production)
- Streamlit session state securely manages sensitive data during the session

## Troubleshooting

### Common Issues

#### API Authentication Errors

**Symptoms**: 
- "Invalid credentials" errors
- "Authorization required" messages
- API requests failing

**Solutions**:
1. Verify API keys in `.env` file
2. Check that API services are enabled in respective dashboards
3. Ensure OAuth credentials have correct scopes
4. Verify API quotas haven't been exceeded

#### Upload Failures

**Symptoms**:
- Failed uploads
- Timeout errors
- Platform-specific error messages

**Solutions**:
1. Check internet connection
2. Verify video format meets platform requirements
3. Ensure video duration is appropriate (15-60 seconds)
4. Check file sizes against platform limits
5. Verify API permissions for uploading

#### Audio Generation Issues

**Symptoms**:
- Missing audio files
- Poor quality audio
- Audio mixing failures

**Solutions**:
1. Check API keys for voice services
2. Verify required directories exist
3. Check input script for unsupported characters
4. Ensure audio file formats are compatible

### Logging

The application logs detailed information to `app.log`, which can be useful for debugging:

- Error messages and stack traces
- API request details
- Generation and upload status
- Performance metrics

## Future Development

### Planned Enhancements

1. **Additional Platforms**:
   - TikTok integration
   - Twitter/X video support
   - Pinterest Idea Pins

2. **Advanced Video Generation**:
   - More sophisticated AI video models
   - Template-based video creation
   - Video editing capabilities

3. **Enhanced Analytics**:
   - Predictive performance modeling
   - A/B testing for content variations
   - Competitive analysis

4. **Workflow Improvements**:
   - Batch processing for multiple niches
   - Advanced scheduling options
   - Custom content templates

5. **Infrastructure**:
   - Cloud deployment options
   - Multi-user support
   - API endpoints for headless operation

### Contributing

Contributions to the project are welcome! Here's how to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please follow coding standards and include tests for new functionality.

### Support and Community

For questions, bug reports, or feature requests:

- Open an issue on GitHub
- Join our community Discord
- Check the project wiki for additional documentation

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the creators of the various APIs and libraries used in this project
- Special thanks to the Streamlit team for their excellent framework
- Appreciation to all contributors and users who provide feedback
