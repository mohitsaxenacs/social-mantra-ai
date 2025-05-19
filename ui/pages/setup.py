import streamlit as st
from ui.components.api_input import api_input, api_file_input
from ui.components.platform_selector import platform_selector
from ui.components.model_selector import model_selector
from ui.utils.state_management import mark_step_complete, go_to_next_step

def show():
    """Display the setup and configuration page"""
    # Initialize session state variables if they don't exist
    if "setup_completed" not in st.session_state:
        st.session_state["setup_completed"] = False
    if "setup_step" not in st.session_state:
        st.session_state["setup_step"] = "platform_selection"
    
    st.markdown("## 1️⃣ Setup & Configuration")
    
    # If setup was previously completed, show a success message and option to edit
    if st.session_state.get("setup_completed", False):
        st.success("✅ Setup is complete! You can edit your configuration below.")

    # Create a visual progress indicator
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("Step 1: Platform & Niche 👈")
    with col2:
        st.caption("Step 2: API Configuration")
    with col3:
        st.caption("Step 3: Model Selection")
    
    st.markdown("### Select Target Platforms")
    st.caption("Choose which platforms you want to publish your videos to. You'll only need to configure APIs for selected platforms.")
    
    # Select platforms first - using simplified=True to avoid duplicate headers
    selected_platforms = platform_selector(simplified=True)
    
    # Show platform requirements directly under selection
    if any(selected_platforms.values()):
        platforms_selected = []
        if selected_platforms.get("youtube"):
            platforms_selected.append("YouTube")
        if selected_platforms.get("facebook"):
            platforms_selected.append("Facebook")
        if selected_platforms.get("instagram"):
            platforms_selected.append("Instagram")
        
        st.success(f"✅ Selected: {', '.join(platforms_selected)}")
        
        with st.expander("Platform Requirements"):
            if selected_platforms.get("youtube"):
                st.markdown("""
                **YouTube Shorts:**
                - 9:16 vertical format
                - Up to 60 seconds
                - 1080x1920 resolution recommended
                """)
                
            if selected_platforms.get("facebook"):
                st.markdown("""
                **Facebook Reels:**
                - 9:16 vertical format
                - 15-30 seconds recommended (max 60s)
                - 1080x1920 resolution recommended
                """)
                
            if selected_platforms.get("instagram"):
                st.markdown("""
                **Instagram Reels:**
                - 9:16 vertical format
                - 15-30 seconds optimal (max 60s)
                - 1080x1920 resolution recommended
                """)
    
    # Content Niche Input with clearer guidance
    st.markdown("### Content Niche")
    st.caption("Be specific about your content focus for better research and idea generation.")
    
    # Get current niche from session state
    current_niche = st.session_state.get("content_niche", "")
    
    # Create niche input with detailed help
    col1, col2 = st.columns([8, 2])
    with col1:
        niche = st.text_input(
            "Enter your content niche",
            value=current_niche,
            placeholder="e.g., quick healthy lunch recipes, beginner yoga tutorials",
            help="Specific niches produce better results than broad categories."
        )
    
    with col2:
        st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
        with st.expander("Niche Examples"):
            st.markdown("""
            ✅ **Good Examples:**
            - Beginner yoga tutorials for flexibility
            - 5-minute healthy breakfast recipes
            - Budget travel hacks for Europe
            - Tech reviews of budget smartphones
            
            ❌ **Too Broad:**
            - Fitness
            - Cooking
            - Travel
            - Technology
            """)
    
    # Save niche when changed
    if niche != current_niche:
        st.session_state["content_niche"] = niche
    
    # Check if at least one platform is selected and niche is provided
    platforms_selected = any(selected_platforms.values())
    has_niche = bool(niche.strip())
    can_continue_to_api = platforms_selected and has_niche
    
    # Provide clear feedback on what's needed to continue
    remaining_requirements = []
    if not platforms_selected:
        remaining_requirements.append("Select at least one platform")
    if not has_niche:
        remaining_requirements.append("Enter your content niche")
    
    if not can_continue_to_api:
        st.warning(f"📝 **To continue, please:** {', '.join(remaining_requirements)}")
    else:
        st.success("✅ Basic setup complete! You can now configure the required APIs.")
    
    # Continue to API configuration button
    col1, col2 = st.columns([2, 8])
    with col1:
        continue_to_api = st.button("Next: API Setup ➡️", disabled=not can_continue_to_api, use_container_width=True)
    
    # Only show API configuration if at least one platform is selected and niche is provided
    if can_continue_to_api and continue_to_api:
        st.session_state["setup_step"] = "api_config"
        st.rerun()
    
    # API CONFIGURATION SECTION - only show after API configuration
    if can_continue_to_api and st.session_state.get("setup_step") == "api_config":
        st.markdown("---")
        # Update progress indicator
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("Step 1: Platform & Niche ✅")
        with col2:
            st.info("Step 2: API Configuration 👈")
        with col3:
            st.caption("Step 3: Model Selection")
        
        st.markdown("### 2️⃣ API Configuration")
        st.caption("Enter API keys only for the platforms you've selected.")
        
        # Create tabs for each selected platform to keep the interface clean
        selected_tabs = []
        api_keys_set = True  # Track if all required API keys are provided
        
        if selected_platforms.get("youtube"):
            selected_tabs.append("YouTube")
        if selected_platforms.get("facebook"):
            selected_tabs.append("Facebook")
        if selected_platforms.get("instagram"):
            selected_tabs.append("Instagram")
        
        # Only create tabs if there are selected platforms
        if selected_tabs:
            tabs = st.tabs(selected_tabs)
            
            tab_index = 0
            # YouTube API Configuration - only show if YouTube is selected
            if selected_platforms.get("youtube"):
                with tabs[tab_index]:
                    st.subheader("YouTube API Configuration")
                    st.caption("Configure YouTube API access for content research and uploads")
                    
                    # Simple API Key (for content research)
                    st.markdown("#### YouTube Data API Key")
                    st.info("This API key is **required** for researching trending content and video analytics.")
                    youtube_api_key = api_input(
                        key_name="youtube_api_key",
                        label="YouTube API Key",
                        help_text="API key for YouTube Data API v3. Required for content research.",
                        url="https://console.cloud.google.com/apis/credentials"
                    )
                    
                    # OAuth credentials (for uploading)
                    st.markdown("#### YouTube OAuth Credentials (Optional)")
                    st.info("This is only needed if you plan to automatically upload videos to your YouTube channel.")
                    youtube_client_secrets = api_file_input(
                        key_name="youtube_client_secrets",
                        label="OAuth Client Secrets",
                        help_text="client_secrets.json file for authenticating with your YouTube account. Only needed for uploading videos.",
                        url="https://console.cloud.google.com/apis/credentials"
                    )
                    
                    with st.expander("How to get YouTube API credentials"):
                        st.markdown("""
                        **1. YouTube Data API Key (For Research)**
                        1. Go to [Google Cloud Console](https://console.cloud.google.com/)
                        2. Create a new project or select an existing project
                        3. Enable the YouTube Data API v3
                        4. Go to Credentials and create an **API Key**
                        5. No restrictions are required for basic usage, but you can restrict to YouTube API only
                        6. Copy and paste your API key above
                        
                        **Cost**: Free for 10,000 units/day, then $0.005 per 1,000 units after that
                        
                        **2. YouTube OAuth Credentials (For Uploads - Optional)**
                        1. In the same Google Cloud project, go to Credentials
                        2. Create an **OAuth client ID** (select Web Application or Desktop type)
                        3. Add authorized redirect URIs if needed
                        4. Download the client_secrets.json file
                        5. Upload the file above
                        
                        **Cost**: Uses the same quota as the Data API above
                        """)
                    
                    # Show warning only if they plan to upload but didn't provide OAuth
                    if not st.session_state.get("api_keys", {}).get("youtube_api_key"):
                        st.warning("❗ A YouTube API Key is required for content research functionality.")
                tab_index += 1
            
            # Facebook API Configuration
            if selected_platforms.get("facebook"):
                with tabs[tab_index]:
                    st.subheader("Facebook API Configuration")
                    facebook_app_id = api_input(
                        key_name="facebook_app_id",
                        label="Facebook App ID",
                        help_text="Required for Facebook Reels uploads.",
                        url="https://developers.facebook.com/"
                    )
                    
                    facebook_app_secret = api_input(
                        key_name="facebook_app_secret",
                        label="Facebook App Secret",
                        help_text="Required for Facebook Reels uploads.",
                        url="https://developers.facebook.com/"
                    )
                    
                    facebook_access_token = api_input(
                        key_name="facebook_access_token",
                        label="Access Token",
                        help_text="Long-lived access token for Facebook API.",
                        url="https://developers.facebook.com/tools/explorer/"
                    )
                    
                    facebook_page_id = api_input(
                        key_name="facebook_page_id",
                        label="Page ID",
                        help_text="ID of your Facebook page for Reels uploads.",
                        password=False
                    )
                    
                    with st.expander("How to get Facebook API credentials"):
                        st.markdown("""
                        1. Visit [Facebook for Developers](https://developers.facebook.com/)
                        2. Create a new app (Business type)
                        3. Add the 'Facebook Login' product
                        4. Configure settings and obtain App ID, App Secret
                        5. Generate a long-lived access token using [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
                        6. Find your Page ID in your Facebook Page settings
                        """)
                    
                    if not all([st.session_state.get("facebook_app_id"), 
                              st.session_state.get("facebook_app_secret"), 
                              st.session_state.get("facebook_access_token"), 
                              st.session_state.get("facebook_page_id")]):
                        api_keys_set = False
                        st.warning("All Facebook API fields are required.")
                tab_index += 1
            
            # Instagram Configuration
            if selected_platforms.get("instagram"):
                with tabs[tab_index]:
                    st.subheader("Instagram Credentials")
                    instagram_username = api_input(
                        key_name="instagram_username",
                        label="Instagram Username",
                        help_text="Your Instagram username (creator account).",
                        password=False
                    )
                    
                    instagram_password = api_input(
                        key_name="instagram_password",
                        label="Instagram Password",
                        help_text="Your Instagram password."
                    )
                    
                    with st.expander("How to prepare your Instagram account"):
                        st.markdown("""
                        1. Convert your account to a Creator or Business account in Instagram settings
                        2. Make sure 2FA is disabled during setup (you can enable it later)
                        3. Use a dedicated account for automation rather than your personal account
                        """)
                    
                    if not st.session_state.get("instagram_username") or not st.session_state.get("instagram_password"):
                        api_keys_set = False
                        st.warning("Both Instagram username and password are required.")
        
        # API Configuration Continue Button
        col1, col2, col3 = st.columns([6, 2, 2])
        
        with col1:
            # Add info about which channel will be used
            if selected_platforms.get("youtube"):
                st.info("Videos will be uploaded to the YouTube channel associated with your provided API credentials.")
            if selected_platforms.get("facebook"):
                st.info("Videos will be uploaded to the Facebook page specified in your API setup.")
            if selected_platforms.get("instagram"):
                st.info("Videos will be uploaded to the Instagram account you've provided credentials for.")
        
        with col3:
            # Force the button to be enabled - we'll show warnings if needed but let the user proceed
            # This fixes the issue where the button wouldn't enable despite credentials being present
            continue_to_models = st.button("Next: Model Selection ➡️", use_container_width=True)
        
        # Proceed to model selection
        if continue_to_models:
            st.session_state["setup_step"] = "model_selection"
            st.rerun()
    
    # MODEL SELECTION SECTION - only show after API configuration
    if can_continue_to_api and (st.session_state.get("setup_step") == "model_selection" or st.session_state.get("setup_completed", False)):
        st.markdown("---")
        # Update progress indicator
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("Step 1: Platform & Niche ✅")
        with col2:
            st.caption("Step 2: API Configuration ✅")
        with col3:
            st.info("Step 3: Model Selection 👈")
        
        st.markdown("### 3️⃣ AI Model Selection")
        st.caption("Choose which AI models to use for content generation.")
        
        # AI Models Selection with clearer UI
        selected_models = model_selector()
        
        # Show API key inputs conditionally based on model selection
        missing_api_keys = []
        
        # ElevenLabs for premium voice
        if selected_models.get("voice", "").startswith("elevenlabs"):
            st.subheader("Voice Generation API")
            elevenlabs_api_key = api_input(
                key_name="elevenlabs_api_key",
                label="ElevenLabs API Key",
                help_text="Required for premium voice generation.",
                url="https://elevenlabs.io/"
            )
            if not st.session_state.get("elevenlabs_api_key"):
                missing_api_keys.append("ElevenLabs API key for premium voice")
        
        # RunwayML for premium video
        if selected_models.get("video", "") == "runway":
            st.subheader("Video Generation API")
            runway_api_key = api_input(
                key_name="runway_api_key",
                label="RunwayML API Key",
                help_text="Required for premium video generation.",
                url="https://runwayml.com/"
            )
            if not st.session_state.get("runway_api_key"):
                missing_api_keys.append("RunwayML API key for premium video")
        
        # Pika Labs for premium video
        if selected_models.get("video", "") == "pika":
            st.subheader("Video Generation API")
            pika_api_key = api_input(
                key_name="pika_api_key",
                label="Pika Labs API Key",
                help_text="Required for premium video generation.",
                url="https://pika.art/"
            )
            if not st.session_state.get("pika_api_key"):
                missing_api_keys.append("Pika Labs API key for premium video")
        
        # Only show OpenAI API key input for paid OpenAI models
        if selected_models.get("image", "") == "dalle3":  
            st.subheader("DALL-E 3 Image Generation API")
            openai_api_key = api_input(
                key_name="openai_api_key",
                label="OpenAI API Key",
                help_text="Required for DALL-E 3 image generation.",
                url="https://platform.openai.com/"
            )
            if not st.session_state.get("openai_api_key"):
                missing_api_keys.append("OpenAI API key for DALL-E 3 image generation")
                
        # Stability AI API key for paid Stability AI model
        if selected_models.get("image", "") == "stability_ai":  
            st.subheader("Stability AI Generation API")
            stability_api_key = api_input(
                key_name="stability_api_key",
                label="Stability AI API Key",
                help_text="Required for Stability AI image generation.",
                url="https://stability.ai/"
            )
            if not st.session_state.get("stability_api_key"):
                missing_api_keys.append("Stability AI API key for image generation")
                
        # Display information about free models if selected
        free_image_models = ["builtin_templates", "stable_diffusion", "huggingface_free", "craiyon", "dalle_mini"]
        if selected_models.get("image", "") in free_image_models:
            st.info(f"You've selected a free image generation model ({selected_models.get('image', '')}) which doesn't require an API key. Thumbnails will be generated using this method.")
            
            # Show additional setup instructions for Stable Diffusion
            if selected_models.get("image", "") == "stable_diffusion":
                with st.expander("Stable Diffusion Setup"):
                    st.markdown("""
                    **Stable Diffusion Local Setup (Optional):**
                    
                    1. If you have a GPU, the application will attempt to use the local Stable Diffusion installation
                    2. For higher quality results, we recommend installing [Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
                    3. Advanced users can specify a custom Stable Diffusion API endpoint in the settings
                    
                    If no local Stable Diffusion is detected, the application will fall back to the built-in templates.
                    """)
                    
            # Show additional information for HuggingFace models
            if selected_models.get("image", "") == "huggingface_free":
                with st.expander("HuggingFace Setup"):
                    st.markdown("""
                    **HuggingFace Free Models:**
                    
                    The application will use HuggingFace's free inference API for image generation.
                    No API key is required, but generation may be rate-limited.
                    
                    For higher quality and faster generation, you can optionally add a HuggingFace Pro API key:
                    """)
                    
                    huggingface_api_key = api_input(
                        key_name="huggingface_api_key",
                        label="HuggingFace API Key (Optional)",
                        help_text="Optional: Add this for higher rate limits and better performance.",
                        url="https://huggingface.co/settings/tokens"
                    )
        
        # Setup Summary
        st.markdown("---")
        st.markdown("### Setup Summary")
        
        # Create a summary of selections
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Platforms Selected:**")
            platform_list = []
            if selected_platforms.get("youtube"):
                platform_list.append("✅ YouTube Shorts")
            if selected_platforms.get("facebook"):
                platform_list.append("✅ Facebook Reels")
            if selected_platforms.get("instagram"):
                platform_list.append("✅ Instagram Reels")
            for platform in platform_list:
                st.markdown(f"- {platform}")
            
            st.markdown("**Content Niche:**")
            st.markdown(f"- {niche}")
            
            # Add upload information
            st.markdown("**Upload Control:**")
            st.markdown("- You control how many videos to generate and upload")
            st.markdown("- Videos can be previewed before uploading")
            st.markdown("- Schedule uploads or publish immediately")
        
        with col2:
            st.markdown("**Selected Models:**")
            st.markdown(f"- Voice: {selected_models.get('voice', 'Not selected')}")
            st.markdown(f"- Video: {selected_models.get('video', 'Not selected')}")
            st.markdown(f"- Image: {selected_models.get('image', 'Not selected')}")
            
            if missing_api_keys:
                st.markdown("**Missing API Keys (Recommended):**")
                for key in missing_api_keys:
                    st.markdown(f"- {key}")
        
        # Submit setup button
        st.markdown("---")
        complete_setup = st.button("Complete Setup", type="primary", use_container_width=True)
        
        if complete_setup:
            # Mark the setup as completed
            st.session_state["setup_completed"] = True
            
            # Mark all steps as complete for state management
            mark_step_complete("platform_selection")
            mark_step_complete("api_configuration")
            mark_step_complete("model_selection")
            
            # Proceed to next step in the workflow
            go_to_next_step()
            st.rerun()
        
        # Show warning about missing API keys
        if missing_api_keys:
            with col1:
                st.warning("⚠️ Some recommended API keys are missing. You can still continue, but some premium features may be limited to free tier.")
