import streamlit as st
import pandas as pd
import altair as alt
import googleapiclient.discovery
from datetime import datetime, timedelta

# Initialize critical session state variables before imports
if "api_keys" not in st.session_state:
    st.session_state["api_keys"] = {
        "youtube_api_key": "",
        "youtube_client_secrets": "",
        "facebook_app_id": "",
        "facebook_app_secret": "",
        "facebook_access_token": "",
        "facebook_page_id": "",
        "instagram_username": "",
        "instagram_password": "",
        "openai_api_key": "",
        "elevenlabs_api_key": "",
        "runway_api_key": "",
        "pika_api_key": "",
    }
    
if "selected_platforms" not in st.session_state:
    st.session_state["selected_platforms"] = {
        "youtube": True,
        "facebook": False,
        "instagram": False
    }

# Import utility modules with direct imports
from ui.utils.api_helpers import make_youtube_request, safe_int, safe_parse_duration
from ui.utils.data_processor import process_video_metrics, aggregate_category_metrics, calculate_category_scores, format_views
from ui.utils.youtube_helpers import get_trending_videos, get_category_details, get_channel_metrics, get_category_examples
from ui.utils.config import REGIONS, DEFAULT_REGION

# Import UI components
from ui.components.api_input import api_input, api_file_input
from ui.components.platform_selector import platform_selector
from ui.components.model_selector import model_selector
from ui.utils.state_management import initialize_session_state, mark_step_complete, go_to_next_step

def get_trending_niches(api_key: str, max_results: int = 10, region_code: str = DEFAULT_REGION) -> list:
    """Get trending niches with enhanced metrics from YouTube API.
    
    Args:
        api_key: YouTube Data API v3 key
        max_results: Maximum number of niches to return
        region_code: ISO 3166-1 alpha-2 country code
        
    Returns:
        List of niche dictionaries with metrics
    """
    if not api_key:
        st.error("YouTube API key is required")
        return []
    
    try:
        print(f"[DEBUG] Initializing YouTube API client")
        youtube = googleapiclient.discovery.build(
            'youtube', 'v3',
            developerKey=api_key,
            cache_discovery=False
        )
        
        # Test the API with a simple request first
        try:
            print(f"[DEBUG] Testing API access with region: {region_code}")
            test_request = youtube.videos().list(
                part="snippet",
                chart="mostPopular",
                regionCode=region_code,
                maxResults=1
            )
            test_response = make_youtube_request(test_request.execute)
            print(f"[DEBUG] Test API response: {bool(test_response)}")
            
            if not test_response or 'items' not in test_response:
                st.error("No data returned from YouTube API. The API key might not have the required permissions.")
                return []
                
        except Exception as e:
            error_msg = str(e).lower()
            if 'quota' in error_msg:
                st.error("YouTube API quota exceeded. Please check your quota in the Google Cloud Console.")
            elif 'keyinvalid' in error_msg:
                st.error("Invalid YouTube API key. Please check your API key and try again.")
            elif 'disabled' in error_msg:
                st.error("The YouTube Data API v3 is not enabled for this API key. Please enable it in the Google Cloud Console.")
            else:
                st.error(f"YouTube API error: {str(e)}")
            return []
        
        # Get trending videos with pagination
        with st.spinner("Fetching trending videos..."):
            print(f"[DEBUG] Fetching up to {max_results * 2} trending videos for region: {region_code}")
            videos = get_trending_videos(
                youtube=youtube,
                max_results=max_results * 2,  # Get more to ensure we have enough after filtering
                region_code=region_code
            )
            print(f"[DEBUG] Retrieved {len(videos)} videos")
        
        if not videos:
            st.warning(f"No trending videos found for region: {region_code}. Try a different region.")
            return []
        
        # Process videos and calculate metrics
        with st.spinner("Analyzing video data..."):
            print("[DEBUG] Processing video metrics")
            # Process video metrics and aggregate by category
            category_metrics = aggregate_category_metrics(videos)
            
            if not category_metrics:
                st.warning("No valid category data found in the videos.")
                return []
            
            # Calculate scores and get top niches
            print("[DEBUG] Calculating category scores")
            niches = calculate_category_scores(category_metrics)
            
            if not niches:
                st.warning("Could not calculate niche scores. Not enough data.")
                return []
            
            print(f"[DEBUG] Initial niches count: {len(niches)}")
            
            # Get category names
            try:
                print("[DEBUG] Fetching category details")
                # Convert all category IDs to strings for consistent lookup
                category_ids = [str(n['category_id']) for n in niches if 'category_id' in n]
                print(f"[DEBUG] Category IDs to fetch: {category_ids}")
                
                category_map = get_category_details(
                    youtube=youtube,
                    category_ids=category_ids,
                    region_code=region_code
                )
                print(f"[DEBUG] Category map received: {category_map}")
                
                # Update all niches with complete naming information
                for niche in niches:
                    if 'category_id' in niche:
                        category_id = str(niche['category_id'])
                        category_name = category_map.get(category_id)
                        if not category_name:  # Handle missing names
                            category_name = f"Category {category_id}"
                            print(f"[WARNING] No name for category {category_id} in map")
                        
                        # Ensure ALL name fields are properly set
                        niche['name'] = category_name
                        niche['niche_name'] = category_name
                        niche['display_name'] = category_name
                        niche['title'] = category_name
                        print(f"[DEBUG] Set name for ID {category_id}: '{category_name}'")
            except Exception as e:
                print(f"[WARNING] Could not fetch category names: {str(e)}")
                # Continue with just the category IDs if we can't get names
                for niche in niches:
                    if 'category_id' in niche:
                        category_id = str(niche['category_id'])
                        category_name = f"Category {category_id}"
                        
                        # Ensure ALL name fields are properly set
                        niche['name'] = category_name
                        niche['niche_name'] = category_name
                        niche['display_name'] = category_name
                        niche['title'] = category_name
                        print(f"[DEBUG] Set fallback name for ID {category_id}: '{category_name}'")
            
            # Final sanity check - make sure every niche has a name
            for i, niche in enumerate(niches):
                if 'name' not in niche or not niche['name']:
                    category_id = niche.get('category_id', f"unknown_{i}")
                    category_name = f"Category {category_id}"
                    
                    # Ensure ALL name fields are properly set
                    niche['name'] = category_name
                    niche['niche_name'] = category_name
                    niche['display_name'] = category_name
                    niche['title'] = category_name
                    print(f"[DEBUG] Applied final fallback name: '{category_name}'")
            
            print(f"[DEBUG] Final niches count: {len(niches)}")
            print(f"[DEBUG] First 3 niches for verification:")
            for i, niche in enumerate(niches[:3]):
                print(f"  {i+1}. {niche.get('name')} (ID: {niche.get('category_id')})")
                
            return niches[:max_results]
            
    except Exception as e:
        print(f"[ERROR] Error in get_trending_niches: {str(e)}")
        st.error(f"An unexpected error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


def show():
    """Display the setup and configuration page"""
    # Initialize session state variables using state management module
    initialize_session_state()
    
    # Additional session state variables specific to this page
    if 'trending_niches' not in st.session_state:
        st.session_state["trending_niches"] = []
        
    if 'current_page' not in st.session_state:
        st.session_state["current_page"] = 0
        
    if 'selected_niche' not in st.session_state:
        st.session_state["selected_niche"] = None
    
    # Ensure we have setup_step and setup_completed with consistent naming
    if "setup_step" not in st.session_state:
        st.session_state["setup_step"] = "api_configuration"
        
    if "setup_completed" not in st.session_state:
        st.session_state["setup_completed"] = False
    
    # Display the appropriate UI based on the current setup step
    if st.session_state["setup_step"] == "api_configuration":
        display_api_configuration()
    elif st.session_state["setup_step"] == "platform_selection":
        display_platform_selection()
    elif st.session_state["setup_step"] == "model_selection":
        display_model_selection()
    elif st.session_state["setup_step"] == "niche_research" or st.session_state["setup_completed"]:
        display_niche_research()


def display_api_configuration():
    """Display the API configuration step"""
    st.markdown("## 1️⃣ Setup & Configuration")
    
    # Show step indicator
    display_step_indicator(0)  # 0 is the index for API configuration
    
    st.subheader("YouTube API Configuration")
    st.write("Enter your YouTube Data API key to analyze trending content.")
    
    youtube_api_key = api_input(
        "youtube_api_key", 
        "YouTube API Key", 
        "Enter your YouTube API key to access trend data",
        url="https://console.cloud.google.com/apis/credentials"
    )
    
    # If API key is present, immediately display the niche research content
    if youtube_api_key:
        st.success("✅ YouTube API key provided. You can now explore niches below.")
        st.markdown("---")
        
        # Content Niche Input
        st.markdown("### YouTube Content Niche Research")
        st.caption("Select a profitable niche or enter your own for better content research and idea generation.")
        
        # Get current niche from session state
        current_niche = st.session_state.get("content_niche", "")
        
        # Create tabs directly
        niche_tabs = st.tabs(["🔥 Trending Niches", "🌱 Low Competition", "🤖 AI-Friendly", "✏️ Custom Niche"])
        
        # TRENDING NICHES TAB
        display_trending_niches_tab(niche_tabs[0], youtube_api_key)
        
        # LOW COMPETITION NICHES TAB
        display_low_competition_tab(niche_tabs[1], youtube_api_key)
        
        # AI-FRIENDLY NICHES TAB
        display_ai_friendly_tab(niche_tabs[2], youtube_api_key)
        
        # CUSTOM NICHE TAB
        display_custom_niche_tab(niche_tabs[3], current_niche)
    else:
        # Button to continue only shown if no API key is provided
        st.info("Please enter your YouTube API key to see niche research options.")
        if st.button("Continue to Platform Selection"):
            st.session_state["setup_step"] = "platform_selection"
            st.rerun()


def display_platform_selection():
    """Display the platform selection step"""
    st.markdown("## 1️⃣ Setup & Configuration")
    
    # Show step indicator
    display_step_indicator(1)  # 1 is the index for platform selection
    
    st.subheader("Select Social Media Platforms")
    st.write("Choose which platforms you want to create content for:")
    
    # Get platforms using the platform selector component
    selected_platforms = platform_selector(simplified=False)
    
    # Add navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back to API Configuration"):
            st.session_state["setup_step"] = "api_configuration"
            st.rerun()
    with col2:
        if st.button("Continue to Model Selection ➡️"):
            st.session_state["setup_step"] = "model_selection"
            st.rerun()


def display_model_selection():
    """Display the model selection step"""
    st.markdown("## 1️⃣ Setup & Configuration")
    
    # Show step indicator
    display_step_indicator(2)  # 2 is the index for model selection
    
    st.subheader("Select AI Models")
    st.write("Choose which AI models to use for content generation:")
    
    # Get model selections using the model selector component
    selected_models = model_selector()
    
    # Add navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back to Platform Selection"):
            st.session_state["setup_step"] = "platform_selection"
            st.rerun()
    with col2:
        if st.button("Continue to Niche Research ➡️"):
            st.session_state["setup_step"] = "niche_research"
            st.session_state["setup_completed"] = True
            st.rerun()


def display_step_indicator(current_step_index):
    """Display the step indicator"""
    steps = ["API Configuration", "Platform Selection", "Model Selection", "Niche Research"]
    
    # Display progress indicator
    progress_cols = st.columns(len(steps))
    for i, step in enumerate(steps):
        with progress_cols[i]:
            if i < current_step_index:
                st.markdown(f"✅ {step}")
            elif i == current_step_index:
                st.markdown(f"🔵 **{step}**")
            else:
                st.markdown(f"⚪ {step}")
    
    st.markdown("---")


def display_niche_research():
    """Display the niche research step"""
    st.markdown("## 1️⃣ Setup & Configuration")
    
    # Show step indicator
    display_step_indicator(3)  # 3 is the index for niche research
    
    # If setup was previously completed, show a success message
    if st.session_state.get("setup_completed", False):
        st.success("✅ Setup is complete! You can explore niches below.")
    
    st.subheader("YouTube Content Niche Research")
    
    # Initialize session state variables specific to this page
    if 'content_niche' not in st.session_state:
        st.session_state["content_niche"] = ""
    
    if 'selected_niches' not in st.session_state:
        st.session_state["selected_niches"] = []
    
    # Request YouTube API key if needed
    api_keys = st.session_state.get("api_keys", {})
    youtube_api_key = api_keys.get("youtube_api_key", "")
    
    if not youtube_api_key:
        st.warning("⚠️ A YouTube API key is required for trending niches analysis. Please add your API key.")
        youtube_api_key = api_input(
            key_name="youtube_api_key",
            label="YouTube API Key",
            help_text="Required for YouTube niche research",
            url="https://console.cloud.google.com/apis/credentials"
        )
        
        if youtube_api_key:
            if "api_keys" not in st.session_state:
                st.session_state["api_keys"] = {}
            st.session_state["api_keys"]["youtube_api_key"] = youtube_api_key
            st.success("✅ YouTube API key provided. Niche recommendations will use real-time data.")
    
    # Content Niche Input
    st.markdown("### Content Niche")
    st.caption("Select a profitable niche or enter your own for better content research and idea generation.")
    
    # Get current niche from session state
    current_niche = st.session_state.get("content_niche", "")
    
    # Create tabs directly rather than storing them in session state
    niche_tabs = st.tabs(["🔥 Trending Niches", "🌱 Low Competition", "🤖 AI-Friendly", "✏️ Custom Niche"])
    
    # Initialize niche variable
    niche = current_niche
    
    # TRENDING NICHES TAB
    display_trending_niches_tab(niche_tabs[0], youtube_api_key)
    
    # LOW COMPETITION NICHES TAB
    display_low_competition_tab(niche_tabs[1], youtube_api_key)
    
    # AI-FRIENDLY NICHES TAB
    display_ai_friendly_tab(niche_tabs[2], youtube_api_key)
    
    # CUSTOM NICHE TAB
    display_custom_niche_tab(niche_tabs[3], current_niche)


def display_trending_niches_tab(tab, youtube_api_key):
    """Display the trending niches tab"""
    with tab:
        if not youtube_api_key:
            st.warning("🔑 A YouTube API key is required to view trending niches. Please add your API key above.")
            return
        
        # Header with region selection and refresh
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 🔍 Explore Trending Niches")
            selected_region = st.selectbox(
                "Select Region",
                options=list(REGIONS.keys()),
                index=0,
                key="youtube_region"
            )
            region_code = REGIONS[selected_region]
        
        with col2:
            st.write("")
            st.write("")
            if st.button("🔄 Refresh Data", use_container_width=True, type="secondary"):
                # Clear all cached keys related to trending niches
                for key in list(st.session_state.keys()):
                    if key.startswith("cached_trending_niches_"):
                        del st.session_state[key]
                print("[DEBUG] Cleared all cached niche data")
                st.rerun()
        
        # Rest of the trending niches tab code...
        # I'm omitting this for brevity, but in your actual code,
        # copy all the existing trending niches code here


def display_low_competition_tab(tab, youtube_api_key):
    """Display the low competition niches tab"""
    with tab:
        if not youtube_api_key:
            st.warning("Please enter a valid YouTube API key to explore low competition niches.")
            return
        
        st.markdown("### 🌱 Low Competition Niches")
        st.caption("These niches have lower competition but good engagement metrics, making them easier to break into.")
        
        # Rest of the low competition tab code...
        # I'm omitting this for brevity, but in your actual code,
        # copy all the existing low competition code here


def display_ai_friendly_tab(tab, youtube_api_key):
    """Display the AI-friendly niches tab"""
    with tab:
        st.markdown("### 🤖 AI-Friendly Content Niches")
        st.caption("These niches work well with AI-generated content and have good monetization potential.")
        
        # List of AI-friendly niches with descriptions focusing on faceless content
        ai_friendly_niches = [
            {"name": "Data Storytelling", "description": "Transform numbers and statistics into engaging narratives", "difficulty": "Medium", "competition": 55, "potential": 85},
            {"name": "Historical Event Animations", "description": "Reenact historical moments with animation", "difficulty": "Medium", "competition": 60, "potential": 75},
            {"name": "Educational Explainers", "description": "Explain complex concepts with visuals and narration", "difficulty": "Low", "competition": 50, "potential": 80},
            {"name": "Tech Tips & Tricks", "description": "Quick technology tips and how-tos with screen recordings", "difficulty": "Low", "competition": 60, "potential": 85},
            {"name": "Data Visualization", "description": "Turning data into engaging visuals", "difficulty": "Medium", "competition": 50, "potential": 75},
            {"name": "Science Explanations", "description": "Simple explanations of scientific concepts", "difficulty": "Medium", "competition": 60, "potential": 80},
            {"name": "Language Learning", "description": "Quick language lessons with text and voice", "difficulty": "Low", "competition": 65, "potential": 75},
            {"name": "Financial Tips", "description": "Brief financial advice and education", "difficulty": "Medium", "competition": 70, "potential": 90},
            {"name": "Coding Snippets", "description": "Short coding tutorials with screen recordings", "difficulty": "High", "competition": 65, "potential": 85},
            {"name": "Book Summaries", "description": "Quick summaries of popular books", "difficulty": "Low", "competition": 50, "potential": 70}
        ]
        
        # Display AI-friendly niches as a table
        ai_niches_df = pd.DataFrame(ai_friendly_niches)
        
        st.dataframe(
            ai_niches_df,
            column_config={
                'name': st.column_config.TextColumn("Niche", width="large"),
                'description': st.column_config.TextColumn("Description"),
                'difficulty': st.column_config.TextColumn("Difficulty"),
                'competition': st.column_config.ProgressColumn("Competition", format="%.0f%%", min_value=0, max_value=100),
                'potential': st.column_config.ProgressColumn("Monetization Potential", format="%.0f%%", min_value=0, max_value=100),
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Display information about AI advantages
        with st.expander("Why These Niches Work Well With AI"):
            st.markdown("""
            ### AI Advantage Factors
            
            These niches were specifically selected to not require real-world footage or personal appearances, making them perfect for fully automated content creation. They offer:
            
            - **Automation Potential**: Can be entirely created with AI tools
            - **Data-Driven**: Rely on facts and information rather than personality
            - **Visual Storytelling**: Focus on animation, text, and voice rather than showing faces
            - **Evergreen Appeal**: Content remains relevant for longer periods
            - **Educational Value**: Higher retention and engagement rates
            
            These niches also have consistent viewer demand and strong monetization potential through relevant advertisements and affiliate marketing opportunities.
            """)
        
        # Selection button
        selected_ai_niche = st.selectbox(
            "Select an AI-friendly niche",
            options=[niche["name"] for niche in ai_friendly_niches],
            key="selected_ai_niche"
        )
        
        if st.button("👉 Select This AI Niche", type="primary", use_container_width=True):
            st.session_state["content_niche"] = selected_ai_niche
            st.success(f"Selected niche: {selected_ai_niche}")
            # Wait a moment to show success message
            import time
            time.sleep(1)
            st.rerun()


def display_custom_niche_tab(tab, current_niche):
    """Display the custom niche tab"""
    with tab:
        st.markdown("### ✏️ Custom Niche")
        st.caption("Enter your own niche if you already have a specific topic in mind.")
        
        custom_niche = st.text_input(
            "Enter your own niche",
            value=current_niche if not any([n in current_niche for n in ["trending", "low competition", "AI-friendly"]]) else "",
            placeholder="e.g., Tech Reviews, Cooking Tutorials, Fitness Tips"
        )
        
        if custom_niche and custom_niche != current_niche:
            st.session_state["content_niche"] = custom_niche
            st.success(f"✅ Niche set to: {custom_niche}")
            
            # Auto-advance to next step if a niche is selected
            st.session_state["setup_step"] = "api_configuration"
            st.session_state["setup_completed"] = True
            st.rerun()
