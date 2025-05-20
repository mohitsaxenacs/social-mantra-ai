import streamlit as st
from ui.utils.state_management import save_selected_platforms, get_selected_platforms

def platform_selector(simplified=False):
    """Component for selecting target social media platforms
    
    Args:
        simplified: If True, hides the component's header and description
        
    Returns:
        dict: Dictionary of selected platforms {platform_name: bool}
    """
    # Initialize selected_platforms if it doesn't exist
    if "selected_platforms" not in st.session_state:
        st.session_state["selected_platforms"] = {
            "youtube": True,
            "facebook": False,
            "instagram": False
        }
    
    # Get current platform selections
    try:
        current_platforms = get_selected_platforms()
    except Exception as e:
        print(f"Error getting platforms: {e}")
        # Default fallback if there's an error
        current_platforms = {
            "youtube": True,
            "facebook": False,
            "instagram": False
        }
        # Save this default to session state
        save_selected_platforms(current_platforms)
    
    # Only show header and caption if not in simplified mode
    if not simplified:
        st.markdown("### Select Target Platforms")
        st.caption("Choose which platforms you want to upload content to.")
    
    # Create container with custom styling
    with st.container():
        # Add some spacing
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        # Platform selection with icons and descriptions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            youtube = st.checkbox(
                "YouTube Shorts",
                value=current_platforms.get("youtube", True),
                key="platform_youtube"
            )
            st.caption("Vertical videos up to 60 seconds")
            st.image("https://img.icons8.com/color/96/000000/youtube-shorts.png", width=40)
        
        with col2:
            facebook = st.checkbox(
                "Facebook Reels",
                value=current_platforms.get("facebook", False),
                key="platform_facebook"
            )
            st.caption("Short videos with trending music")
            st.image("https://img.icons8.com/color/96/000000/facebook-new.png", width=40)
        
        with col3:
            instagram = st.checkbox(
                "Instagram Reels",
                value=current_platforms.get("instagram", False),
                key="platform_instagram"
            )
            st.caption("Creative short videos for Instagram")
            st.image("https://img.icons8.com/fluency/96/000000/instagram-new.png", width=40)
    
    # Create and save the platforms dictionary
    selected_platforms = {
        "youtube": youtube,
        "facebook": facebook,
        "instagram": instagram
    }
    
    # Only save if there's a change
    if selected_platforms != current_platforms:
        save_selected_platforms(selected_platforms)
    
    # Show warning if no platforms selected and not in simplified mode
    if not any(selected_platforms.values()) and not simplified:
        st.warning("Please select at least one platform to continue.")
    
    return selected_platforms
