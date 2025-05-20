import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import the rest of the modules
import streamlit as st

# Import UI modules using direct imports
from ui.pages.setup import show as show_setup
from ui.pages.research import show as show_research
from ui.pages.generation import show as show_generation
from ui.pages.upload import show as show_upload
from ui.pages.analytics import show as show_analytics

from ui.utils.state_management import initialize_session_state

# App styling and configuration
st.set_page_config(
    page_title="Social Media Shorts Automation",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Apply custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        color: #FF4B4B !important;
    }
    .sub-header {
        font-size: 1.5rem !important;
        font-weight: 500 !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    .step-complete {
        color: #00CA61 !important;
        font-weight: 600 !important;
    }
    .step-current {
        color: #FF9D00 !important;
        font-weight: 600 !important;
    }
    .step-pending {
        color: #808495 !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main app header
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("<h1 class='main-header'>Social Media Shorts Video Automation</h1>", unsafe_allow_html=True)
    with col2:
        st.image("https://img.icons8.com/fluency/96/000000/video.png", width=70)
    
    st.markdown("<p class='sub-header'>Create, generate, and upload viral short-form videos across platforms</p>", 
              unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/youtube-shorts.png", width=100)
        st.title("Navigation")
        st.caption("Follow these steps in order:")
        
        # Navigation steps with status indicators
        step_status = {
            "setup": st.session_state.get("setup_complete", False),
            "research": st.session_state.get("research_complete", False),
            "generation": st.session_state.get("generation_complete", False),
            "upload": st.session_state.get("upload_complete", False),
            "analytics": True  # Always available
        }
        
        # Determine current step
        current_step = st.session_state.get("current_step", "setup")
        
        # Create navigation
        pages = {
            "setup": "1️⃣ Setup & Configuration",
            "research": "2️⃣ Content Research",
            "generation": "3️⃣ Content Generation",
            "upload": "4️⃣ Upload & Schedule",
            "analytics": "5️⃣ Performance Analytics"
        }
        
        for page_id, page_name in pages.items():
            # Determine status and prepare label without HTML tags
            if step_status[page_id]:
                prefix = "✓"
                button_type = "primary"
            elif page_id == current_step:
                prefix = "➤"
                button_type = "primary"
            else:
                prefix = " "
                button_type = "secondary"
                
            # Create the navigation button with appropriate styling
            button_label = f"{prefix} {page_name}"
            disabled = not (step_status[page_id] or page_id == current_step)
            
            # Use container to apply custom styling
            button_container = st.container()
            with button_container:
                if st.button(button_label, disabled=disabled, use_container_width=True, key=f"nav_{page_id}", type=button_type):
                    st.session_state["current_step"] = page_id
                    st.rerun()
        
        # Add help information
        with st.expander("❓ Need Help?"):
            st.write("""
            Follow each step of the workflow to create and upload viral short-form videos.
            
            1. **Setup**: Configure your API keys and platform settings
            2. **Research**: Analyze trending content in your niche
            3. **Generation**: Create videos, audio, and metadata
            4. **Upload**: Review and publish your content
            5. **Analytics**: Track performance and optimize
            """)
            st.markdown("[📚 View Full Documentation](https://github.com/yourusername/social-media-shorts-video-automation/blob/main/DOCUMENTATION.md)")
    
    # Main content area - show the selected page
    current_page = st.session_state["current_step"]
    
    if current_page == "setup":
        show_setup()
    elif current_page == "research":
        show_research()
    elif current_page == "generation":
        show_generation()
    elif current_page == "upload":
        show_upload()
    elif current_page == "analytics":
        show_analytics()

if __name__ == "__main__":
    main()
