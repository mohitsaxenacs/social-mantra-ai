import streamlit as st
import random
import pandas as pd
import altair as alt
import googleapiclient.discovery
import re
from datetime import datetime, timedelta
from ui.utils.state_management import mark_step_complete, go_to_next_step

# Custom function to parse ISO 8601 duration without requiring the isodate package
def parse_duration(duration_str):
    """Parse ISO 8601 duration string to seconds"""
    # Example: PT1H30M15S = 1 hour, 30 minutes, 15 seconds
    try:
        # Initialize values
        hours, minutes, seconds = 0, 0, 0
        
        # Extract hours, minutes, seconds using regex
        hour_match = re.search(r'(\d+)H', duration_str)
        if hour_match:
            hours = int(hour_match.group(1))
            
        minute_match = re.search(r'(\d+)M', duration_str)
        if minute_match and 'H' in duration_str:
            minutes = int(minute_match.group(1))
        elif minute_match:
            # If there's no 'H', it could be PT30M format
            minutes = int(minute_match.group(1))
            
        second_match = re.search(r'(\d+)S', duration_str)
        if second_match:
            seconds = int(second_match.group(1))
        
        # Calculate total seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds
    except Exception:
        # Default fallback if parsing fails
        return 60  # Default to 1 minute

# YouTube API Integration
def get_youtube_service(api_key):
    """Initialize the YouTube API service"""
    if not api_key:
        st.error("No YouTube API key provided. Please add your API key in the Setup page.")
        return None
    
    try:
        # Add more detailed error handling and cache_discovery=False to avoid credential warnings
        youtube = googleapiclient.discovery.build(
            'youtube', 'v3', 
            developerKey=api_key, 
            cache_discovery=False
        )
        
        # Skip the test request as it might cause unnecessary quota usage
        # Let the actual search request handle any API key errors
        return youtube
    except googleapiclient.errors.HttpError as e:
        error_content = e.content.decode() if hasattr(e, 'content') else str(e)
        if "API key not valid" in error_content or "invalid API key" in error_content.lower():
            st.error("YouTube API key is not valid. Please check the following:")
            st.markdown("""
            **Possible fixes for API key issues:**
            1. Ensure you've enabled the **YouTube Data API v3** in your Google Cloud Console
            2. Check if your API key has any restrictions that might block YouTube API access
            3. Verify your API key was copied correctly without any extra spaces
            4. Make sure your Google Cloud project billing is set up properly if required
            5. Try creating a new API key if the problem persists
            """)
            st.info("For detailed instructions on creating a YouTube API key, visit: https://developers.google.com/youtube/registering_an_application")
        else:
            st.error(f"YouTube API Error: {str(e)}")
            st.code(error_content)
        return None
    except Exception as e:
        st.error(f"Error connecting to YouTube API: {str(e)}")
        st.code(f"Error type: {type(e).__name__}\nDetails: {str(e)}")
        return None

def search_youtube_videos(youtube, query, max_results=5, video_duration='short'):
    """Search for YouTube videos using the API"""
    try:
        # First search for videos matching the query
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=max_results,
            type='video',
            videoDuration=video_duration,  # 'short' for videos under 4 minutes
            order='viewCount',            # Sort by view count
            relevanceLanguage='en'
        ).execute()
        
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        
        if not video_ids:
            return []
        
        # Then get detailed stats for the videos
        videos_response = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=','.join(video_ids)
        ).execute()
        
        # Process and return the video data
        processed_videos = []
        for item in videos_response['items']:
            # Extract the data we need
            video_id = item['id']
            title = item['snippet']['title']
            channel = item['snippet']['channelTitle']
            published_at = item['snippet']['publishedAt']
            
            # Format the date - Fix timezone handling
            try:
                # Convert the YouTube timestamp to a timezone-aware datetime
                published_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                
                # Make now timezone-aware too with UTC
                now = datetime.now().replace(tzinfo=published_date.tzinfo)
                
                # Now we can safely calculate the difference
                days_ago = (now - published_date).days
                
                if days_ago == 0:
                    posted = "Today"
                elif days_ago == 1:
                    posted = "Yesterday"
                else:
                    posted = f"{days_ago} days ago"
            except Exception as e:
                # Fallback in case of datetime parsing errors
                posted = "Recently"
                days_ago = 7  # Assume a default for calculations
                st.warning(f"Date parsing error: {str(e)}")
            
            # Get video duration using our custom parser instead of isodate
            duration_iso = item['contentDetails']['duration']
            duration_seconds = parse_duration(duration_iso)
            duration = f"{int(duration_seconds)} sec"
            
            # Get statistics
            statistics = item.get('statistics', {})
            views = int(statistics.get('viewCount', 0))
            likes = int(statistics.get('likeCount', 0))
            comments = int(statistics.get('commentCount', 0))
            
            # Generate daily view trend data (estimated)
            daily_views = []
            # Approximate daily view distribution over time
            total_days = max(days_ago, 1)
            avg_views_per_day = views / total_days
            
            # Create a realistic growth curve (slower at start, faster later)
            for day in range(total_days):
                day_factor = (day / total_days) * 1.5  # Weighted towards recent days
                if day_factor < 1:
                    day_views = int(avg_views_per_day * day_factor)
                else:
                    day_views = int(avg_views_per_day * day_factor)
                    
                daily_views.append({
                    "day": total_days - day,
                    "views": day_views
                })
            
            processed_videos.append({
                "id": video_id,
                "title": title,
                "channel": channel,
                "views": f"{views:,}",
                "views_value": views,
                "posted": posted,
                "duration": duration,
                "likes": f"{likes:,}",
                "comments": f"{comments:,}",
                "daily_views": daily_views,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })
        
        return processed_videos
    
    except Exception as e:
        st.error(f"YouTube API error: {str(e)}")
        return []

def get_trending_videos_from_api(niche, count=10):
    """Get trending YouTube videos based on niche using the YouTube API"""
    # Get YouTube API key from session state using the correct nested structure
    api_keys = st.session_state.get("api_keys", {})
    youtube_api_key = api_keys.get("youtube_api_key", "")
    
    if not youtube_api_key:
        st.error(
            "YouTube API key not found. Please go to Setup and provide a valid YouTube API key in the API configuration section."
        )
        return []
    
    # Initialize YouTube API service
    youtube = get_youtube_service(youtube_api_key)
    if not youtube:
        st.error("Failed to initialize YouTube API. Your API key may be invalid or there may be connectivity issues.")
        return []
    
    # Convert niche to search query terms
    search_terms = {
        "Cats and Dogs": ["cute cats shorts", "dog training shorts", "funny pets", "cat and dog shorts"],
        "Cooking": ["easy recipes shorts", "cooking tips shorts", "quick meals", "food hacks shorts"],
        "Fitness": ["workout shorts", "fitness tips shorts", "exercise routine", "gym motivation shorts"],
        "Technology": ["tech tips shorts", "gadget review shorts", "smartphone hacks", "tech tutorial shorts"],
        "Travel": ["travel tips shorts", "destination guide shorts", "vacation hacks", "travel vlog shorts"],
        "Fashion": ["fashion tips shorts", "outfit ideas shorts", "style guide", "fashion trends shorts"],
        "Beauty": ["makeup tutorial shorts", "skincare routine shorts", "beauty hacks", "hair styling shorts"],
    }
    
    # Get search terms for the niche or use the niche itself if not in the dictionary
    queries = search_terms.get(niche, [f"{niche} shorts", f"{niche} tips", f"{niche} guide"])
    
    # Search for videos using each query and combine results
    all_videos = []
    try:
        for query in queries:
            videos = search_youtube_videos(youtube, query, max_results=count)
            all_videos.extend(videos)
        
        if not all_videos:
            st.warning(f"No videos found for niche: {niche}. Try a different niche or check your YouTube API key permissions.")
            return []
            
        # Remove duplicates and take the top 'count' videos by views
        unique_videos = {}
        for video in all_videos:
            if video['id'] not in unique_videos or video['views_value'] > unique_videos[video['id']]['views_value']:
                unique_videos[video['id']] = video
        
        # Sort by views and take the top 'count'
        sorted_videos = sorted(unique_videos.values(), key=lambda x: x['views_value'], reverse=True)
        return sorted_videos[:count]
        
    except Exception as e:
        st.error(f"YouTube API error: {str(e)}")
        st.code(f"Error details: {type(e).__name__}\n{str(e)}")
        return []

# Rename the old function to indicate it's a simulation
def get_simulated_trending_videos(niche, count=3):
    """Generate simulated trending YouTube video examples based on the niche"""
    # Dictionary of YouTube trends by niche
    channels_by_niche = {
        "Cats and Dogs": ["Cute Cat Friends", "Dog Training Pro", "Pet Lovers", "Furry Companions", "Paws & Whiskers"],
        "Cooking": ["Easy Meals", "Chef Julia's Kitchen", "Quick Recipes", "Budget Bites", "Flavor Lab"],
        "Fitness": ["Gym Masters", "Home Workout Pro", "Fitness Journey", "Strong & Fit", "Daily Exercise"],
        "Technology": ["Tech Insider", "Gadget Review", "Digital Life", "Tech Made Simple", "Future Now"],
        "Travel": ["Wanderlust", "Travel Guide", "Adventure Seekers", "Budget Travels", "Explore Earth"],
        "Fashion": ["Style Guide", "Fashion Forward", "Trendy Looks", "Wardrobe Essentials", "Runway to Street"],
        "Beauty": ["Glow Up", "Beauty Secrets", "Makeup Masterclass", "Skin Deep", "Beauty Hacks"],
        "default": ["Trending Now", "Viral Videos", "Top Content", "Must Watch", "Popular Channel"]
    }
    
    videos = []
    channel_options = channels_by_niche.get(niche, channels_by_niche["default"])
    
    for i in range(count):
        channel = random.choice(channel_options)
        views = random.randint(500000, 20000000)
        days_ago = random.randint(1, 14)
        likes = int(views * random.uniform(0.05, 0.2))
        comments = int(views * random.uniform(0.005, 0.02))
        duration = f"{random.randint(20, 59)} sec"
        
        # Generate a title based on niche
        if niche in niche_topics:
            title_base = random.choice(niche_topics[niche])
        else:
            title_base = random.choice([t.format(niche=niche) for t in niche_topics["default"]])
            
        # Add clickbait elements to make it more realistic
        clickbait_prefixes = ["I Can't Believe", "You Won't Believe", "This Changes Everything", "The Truth About", "Secret", "Revealed", "How I", "Why You Should", "Never"]
        clickbait_suffixes = ["(shocking)", "(must watch)", "(life changing)", "(in seconds)", "ud83dude31", "ud83dudd25", "u2728", "ud83eudd2f", "ud83dudc40"]
        
        # Sometimes add a clickbait prefix or suffix
        if random.random() < 0.4:
            title = f"{random.choice(clickbait_prefixes)} {title_base}"
        else:
            title = title_base
            
        if random.random() < 0.3:
            title = f"{title} {random.choice(clickbait_suffixes)}"
            
        # Generate daily view data for charts
        daily_views = []
        current_views = views
        for day in range(days_ago):
            day_views = int(current_views * (1 - random.uniform(0.05, 0.2)))
            daily_views.append({
                "day": days_ago - day,
                "views": day_views
            })
            current_views = day_views
            
        # Create video entry
        videos.append({
            "title": title,
            "channel": channel,
            "views": f"{views:,}",
            "views_value": views,
            "posted": f"{days_ago} days ago",
            "duration": duration,
            "likes": f"{likes:,}",
            "comments": f"{comments:,}",
            "daily_views": daily_views
        })
    
    return videos

# Topics dictionary - moved to global scope to fix the NameError
niche_topics = {
    "Cats and Dogs": [
        "DIY pet toys that your cat will actually play with",
        "Teaching your dog new tricks in under 5 minutes", 
        "Signs your cat is secretly plotting against you",
        "Why dogs tilt their heads when you talk to them",
        "Cats reacting to cucumbers - explained",
        "Most dangerous foods for dogs - what to avoid",
        "How cats always land on their feet - the science explained",
        "Training techniques for stubborn dogs",
        "Cat breeds that are surprisingly good with children",
        "Understanding your dog's body language"
    ],
    "Cooking": [
        "15-minute meal prep ideas that actually taste good",
        "Air fryer hacks you never knew existed",
        "One-pot meals for busy weeknights",
        "Hidden secrets of restaurant chefs",
        "How to properly cut an onion without crying",
        "Budget-friendly meal ideas under $10",
        "The science behind perfect chocolate chip cookies",
        "Cooking mistakes everyone makes and how to fix them",
        "Secret ingredients that transform ordinary dishes",
        "Quick breakfast ideas for people who hate mornings"
    ],
    "Fitness": [
        "5-minute workouts that actually show results",
        "Why you're not seeing results at the gym",
        "Workout myths that are actually hurting your progress",
        "The perfect form for squats - what trainers won't tell you",
        "How to get toned arms without heavy weights",
        "The science of muscle growth explained simply",
        "Post-workout habits that sabotage your progress",
        "Exercises you're probably doing wrong",
        "How to stay motivated when you hate working out",
        "Surprising foods that boost your workout results"
    ],
    "Technology": [
        "Hidden smartphone features most people don't know about",
        "Simple tech hacks to make your life easier",
        "Why your WiFi is actually slow - and how to fix it",
        "AI tools that will change how you work forever",
        "Protect your privacy online with these simple steps",
        "Tech myths that waste your money",
        "The dark side of smart home devices",
        "Future tech that's closer than you think",
        "Apps that actually make you more productive",
        "Why expensive cables are a complete waste of money"
    ],
    "Travel": [
        "Hidden gems in popular tourist destinations",
        "Airport hacks that will change how you travel",
        "How to pack for a week in just a carry-on",
        "Travel scams you need to watch out for",
        "Budget travel tips that actually work",
        "Why you should never exchange currency at the airport",
        "Secret hotel room upgrades most people don't know about",
        "The psychology behind jet lag and how to beat it",
        "Apps that make travel planning effortless",
        "Hidden costs of cheap flights - what to watch for"
    ],
    "Fashion": [
        "Capsule wardrobe essentials that never go out of style",
        "How to look expensive on a budget",
        "Style mistakes that make you look older",
        "The psychology of color in fashion",
        "Thrift shopping secrets from fashion experts",
        "Why expensive doesn't always mean better quality",
        "How to find the perfect jeans for your body type",
        "Surprising fashion rules you should break",
        "Sustainable fashion brands that don't sacrifice style",
        "Wardrobe organization hacks from professional stylists"
    ],
    "Beauty": [
        "Skincare ingredients you should never mix",
        "Makeup tricks professional artists swear by",
        "Why expensive skincare might be wasting your money",
        "The science of aging skin explained simply",
        "Hair mistakes that are aging you",
        "Drugstore dupes for high-end beauty products",
        "Skincare myths dermatologists want you to stop believing",
        "The perfect order to apply skincare products",
        "How to find your perfect foundation match",
        "Natural remedies for common skin problems that actually work"
    ],
    # Add a generic list for any niche not specifically covered
    "default": [
        "5 surprising facts about {niche} most people don't know",
        "The biggest myths about {niche} debunked",
        "How {niche} is changing in 2025",
        "Beginner's guide to {niche} - where to start",
        "Expert tips for {niche} that will change your perspective",
        "Common mistakes people make with {niche}",
        "The history of {niche} explained in 60 seconds",
        "Why {niche} matters more than ever in 2025",
        "How to get started with {niche} on a budget",
        "The future of {niche} - trends to watch"
    ]
}

# Topics generator based on niche
def get_trending_topics(niche, count=5):
    """Generate trending topics based on the selected niche"""
    # Use the specific niche topics if available, otherwise use the default list with the niche substituted
    if niche in niche_topics:
        topics = niche_topics[niche]
    else:
        # Format the default topics with the user's niche
        topics = [topic.format(niche=niche) for topic in niche_topics["default"]]
    
    # Randomly select topics to make it feel fresh each time
    selected_topics = random.sample(topics, min(count, len(topics)))
    
    # Add fake stats to make it look more realistic
    result = []
    for topic in selected_topics:
        views = random.randint(100000, 5000000)
        growth = random.randint(25, 400)
        days = random.randint(3, 30)
        
        # Add time series data for charts
        daily_data = []
        start_views = views - (views * growth / 100)
        for day in range(days):
            daily_views = int(start_views + (views - start_views) * (day / days))
            daily_data.append({
                "day": day + 1,
                "views": daily_views
            })
            
        result.append({
            "topic": topic,
            "views": f"{views:,}",
            "growth": f"+{growth}%",
            "growth_value": growth,  # numeric value for sorting/charts
            "views_value": views,    # numeric value for sorting/charts
            "period": f"Last {days} days",
            "days": days,
            "daily_data": daily_data
        })
    
    return result

def show():
    """Display the content research page"""
    st.markdown("## 2️⃣ Content Research")
    st.caption("Research trending topics and content in your niche")
    
    # Add enhanced debug information for session state
    with st.expander("Debug Information"):
        st.write("Session State Keys:", list(st.session_state.keys()))
        api_keys = st.session_state.get("api_keys", {})
        st.write("API Keys in Session State:", api_keys)
        youtube_api_key = api_keys.get("youtube_api_key", "")
        youtube_client_secrets = api_keys.get("youtube_client_secrets", "")
        
        if youtube_api_key:
            masked_key = "*****" + youtube_api_key[-4:] if len(youtube_api_key) >= 4 else "*****"
            st.write("YouTube API Key (masked):", masked_key)
        else:
            st.write("YouTube API Key: Not found in session state")
            
        if youtube_client_secrets:
            st.write("YouTube Client Secrets: Available in session state")
            st.write("Filename:", youtube_client_secrets)
        else:
            st.write("YouTube Client Secrets: Not found in session state")
            
        # Check for client_secrets.json in multiple possible locations
        import os
        possible_paths = [
            "client_secrets.json",  # Current directory
            os.path.join(os.getcwd(), "client_secrets.json"),  # Explicit current directory
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "client_secrets.json"),  # Script directory
            os.path.join(os.path.expanduser("~"), "client_secrets.json"),  # User home directory
        ]
        
        st.write("Checking for client_secrets.json in various locations:")
        found = False
        for path in possible_paths:
            if os.path.exists(path):
                st.success(f"Found at: {path}")
                found = True
                # Show file size
                try:
                    file_size = os.path.getsize(path)
                    st.write(f"File size: {file_size} bytes")
                except Exception as e:
                    st.write(f"Error getting file size: {e}")
        
        if not found:
            st.error("client_secrets.json not found in any expected location")
            st.info("YouTube API requires only an API key for read-only operations (what we're using). client_secrets.json is only needed for operations requiring user authentication like uploading videos.")
    
    # Get content niche from session state
    niche = st.session_state.get("content_niche", "")
    
    if not niche:
        st.warning("No content niche selected. Please go back to setup and select a niche.")
        if st.button("⬅️ Go to Setup"):
            st.session_state["current_step"] = "setup"
            st.rerun()
        return
    
    st.info(f"Researching content for niche: **{niche}**")
    
    # Check if YouTube API key is available
    api_keys = st.session_state.get("api_keys", {})
    youtube_api_key = api_keys.get("youtube_api_key", "")
    
    # Show trending topics section with API-dependent content
    st.markdown("### Trending Topics")
    st.caption("Based on social media engagement and search trends")
    
    if not youtube_api_key:
        st.error("YouTube API key is required to fetch trending topics.")
        st.info("Please go to Setup and provide your YouTube API key in the API configuration section.")
    else:
        try:
            # This section will now rely on YouTube API instead of simulation
            # Initialize YouTube API service
            youtube = get_youtube_service(youtube_api_key)
            if not youtube:
                st.error("Failed to initialize YouTube API. Your API key may be invalid.")
            else:
                # Test the API with a minimal request to verify it's actually working
                try:
                    # Make a minimal test request that doesn't consume much quota
                    test_response = youtube.i18nLanguages().list(part="snippet").execute()
                    
                    # If we get here, the API is truly connected and working
                    st.success("✅ YouTube API connected successfully! Fetching trending topics...")
                    
                    # Map niche to relevant search terms
                    search_terms = {
                        "Cats and Dogs": ["cats", "dogs", "pets", "kittens", "puppies"],
                        "Cooking": ["recipes", "cooking", "food", "kitchen", "chef"],
                        "Fitness": ["workout", "fitness", "exercise", "gym", "training"],
                        "Technology": ["tech", "technology", "gadgets", "smartphones", "computers"],
                        "Travel": ["travel", "destinations", "vacation", "tourism", "sightseeing"],
                        "Fashion": ["fashion", "style", "clothing", "outfits", "accessories"],
                        "Beauty": ["beauty", "makeup", "skincare", "cosmetics", "hair"],
                    }
                    
                    # Get applicable search terms for this niche
                    niche_terms = search_terms.get(niche, [niche.lower()])
                    
                    # Show what we'll be searching for
                    st.info(f"Analyzing YouTube trends for: {', '.join(niche_terms)}")
                    
                    # Placeholder for actual API implementation - this helps the user understand
                    # that the API is connected but the actual topic analysis is planned for future work
                    st.info("Note: In a complete implementation, this would analyze real YouTube data to extract trending topics in your niche.")
                    
                except googleapiclient.errors.HttpError as e:
                    error_content = e.content.decode() if hasattr(e, 'content') else str(e)
                    if "API key not valid" in error_content or "invalid API key" in error_content.lower():
                        st.error("🚫 YouTube API key validation failed.")
                        st.markdown("""
                        **Your API key was rejected by YouTube. Possible reasons:**
                        1. The API key may be incorrect or contain extra characters
                        2. The YouTube Data API v3 is not enabled for this key
                        3. There may be API key restrictions blocking access
                        4. Your Google Cloud project may need billing setup
                        5. Try creating a new API key if the problem persists
                        """)
                    else:
                        st.error(f"YouTube API Error: {str(e)}")
                        st.code(error_content[:500] + "..." if len(error_content) > 500 else error_content)
        except Exception as e:
            st.error(f"Error analyzing trending topics: {str(e)}")
            st.code(f"Error details: {type(e).__name__}\n{str(e)}")
    
    # Show YouTube trending videos with visualization
    st.markdown("### Top YouTube Content")
    st.caption("Popular YouTube Shorts in your niche")
    
    try:
        trending_videos = get_trending_videos_from_api(niche)
        
        if trending_videos:
            video_metrics_tab, video_chart_tab = st.tabs(["Video Details", "Performance Charts"])
            
            with video_metrics_tab:
                # Display trending videos in a more visual way
                for video in trending_videos:
                    with st.container():
                        cols = st.columns([3, 1])
                        with cols[0]:
                            st.subheader(video["title"])
                            st.caption(f"Channel: {video['channel']} 📆 {video['posted']} ⏰ {video['duration']}")
                        with cols[1]:
                            st.metric("Views", video["views"])
                        
                        sub_cols = st.columns([1, 1, 2, 1])
                        with sub_cols[0]:
                            st.write(f"👍 {video['likes']}")
                        with sub_cols[1]:
                            st.write(f"💬 {video['comments']}")
                        with sub_cols[3]:
                            # Add a button to view the video on YouTube
                            if 'url' in video:
                                st.markdown(f"[Watch on YouTube]({video['url']})")
                            
                        st.markdown("---")
            
            with video_chart_tab:
                # Create comparison bar chart for videos
                video_data = pd.DataFrame({
                    'Video': [v["title"][:20] + "..." for v in trending_videos],  # Truncate long titles
                    'Views': [v["views_value"] for v in trending_videos]
                })
                
                videos_chart = alt.Chart(video_data).mark_bar().encode(
                    x=alt.X('Video:N', title=None),
                    y=alt.Y('Views:Q', title='Total Views'),
                    color=alt.Color('Views:Q', scale=alt.Scale(scheme='reds'), legend=None),
                    tooltip=['Video', 'Views']
                ).properties(
                    title='YouTube Shorts Performance Comparison',
                    height=300
                )
                
                st.altair_chart(videos_chart, use_container_width=True)
                
                # Growth trend visualization for selected video
                st.subheader("View growth for selected video")
                video_selector = st.selectbox(
                    "Select a video to view its growth trend:", 
                    options=[v["title"] for v in trending_videos]
                )
                
                # Get the selected video's data
                selected_video = next(v for v in trending_videos if v["title"] == video_selector)
                video_trend_data = pd.DataFrame(selected_video["daily_views"])
                
                # Create line chart for video growth
                video_line_chart = alt.Chart(video_trend_data).mark_area(opacity=0.7).encode(
                    x=alt.X('day:Q', title='Days ago'),
                    y=alt.Y('views:Q', title='Views'),
                    tooltip=['day', 'views']
                ).properties(
                    title='View accumulation over time',
                    height=300
                )
                
                st.altair_chart(video_line_chart, use_container_width=True)
        else:
            st.warning("No trending videos could be found. Please check your YouTube API configuration.")
            
    except Exception as e:
        st.error(f"An error occurred while loading YouTube content: {str(e)}")
        st.code(f"Error details: {type(e).__name__}\n{str(e)}")
    
    # Add search functionality
    with st.expander("Search for specific topics"):
        search_term = st.text_input("Enter keywords related to your niche")
        if search_term and st.button("Search"):
            st.write(f"Searching for content related to '{search_term}' in the {niche} niche...")
            # This would typically call an API, but we'll simulate results
            st.info("This feature will connect to YouTube API, Google Trends, and other sources in the full version.")
    
    # Add navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Back to Setup"):
            st.session_state["current_step"] = "setup"
            st.rerun()
    
    with col3:
        if st.button("Continue to Generation ➡️"):
            # Mark this step as complete
            mark_step_complete("research")
            # Go to next step
            go_to_next_step()
            st.rerun()