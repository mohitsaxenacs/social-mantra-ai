import streamlit as st

def initialize_session_state():
    """Initialize the session state variables if they don't already exist"""
    # Navigation state
    if "current_step" not in st.session_state:
        st.session_state["current_step"] = "setup"
    
    # Step completion flags
    if "setup_complete" not in st.session_state:
        st.session_state["setup_complete"] = False
    if "research_complete" not in st.session_state:
        st.session_state["research_complete"] = False
    if "generation_complete" not in st.session_state:
        st.session_state["generation_complete"] = False
    if "upload_complete" not in st.session_state:
        st.session_state["upload_complete"] = False
    
    # API key storage (these will be stored securely)
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
    
    # Selected platforms
    if "selected_platforms" not in st.session_state:
        st.session_state["selected_platforms"] = {
            "youtube": True,
            "facebook": False,
            "instagram": False
        }
    
    # Content niche
    if "content_niche" not in st.session_state:
        st.session_state["content_niche"] = ""
    
    # Model selections
    if "models" not in st.session_state:
        st.session_state["models"] = {
            "voice": "gtts",  # Default to free option
            "video": "placeholder",  # Default to placeholder
            "image": "dalle_mini"  # Default to free option
        }
    
    # Content generation results
    if "content_ideas" not in st.session_state:
        st.session_state["content_ideas"] = []
    if "metadata" not in st.session_state:
        st.session_state["metadata"] = {}
    if "audio_files" not in st.session_state:
        st.session_state["audio_files"] = {}
    if "video_files" not in st.session_state:
        st.session_state["video_files"] = {}

def mark_step_complete(step_name):
    """Mark a step as complete in the session state"""
    st.session_state[f"{step_name}_complete"] = True

def go_to_next_step():
    """Advance to the next step in the workflow"""
    current = st.session_state["current_step"]
    
    # Define the step order
    steps = ["setup", "research", "generation", "upload", "analytics"]
    
    # Find current step index
    try:
        current_index = steps.index(current)
        # Go to next step if not at the end
        if current_index < len(steps) - 1:
            st.session_state["current_step"] = steps[current_index + 1]
    except ValueError:
        # If current step not found, go to setup
        st.session_state["current_step"] = "setup"

def save_api_key(key_name, value):
    """Save an API key to the session state"""
    st.session_state["api_keys"][key_name] = value

def get_api_key(key_name):
    """Get an API key from the session state"""
    return st.session_state["api_keys"].get(key_name, "")

def save_selected_platforms(platforms_dict):
    """Save the selected platforms to the session state"""
    st.session_state["selected_platforms"] = platforms_dict

def get_selected_platforms():
    """Get the currently selected platforms"""
    return st.session_state["selected_platforms"]

def save_content_niche(niche):
    """Save the content niche to the session state"""
    st.session_state["content_niche"] = niche

def get_content_niche():
    """Get the content niche from the session state"""
    return st.session_state["content_niche"]

def save_model_selection(model_type, model_name):
    """Save a model selection to the session state"""
    st.session_state["models"][model_type] = model_name

def get_model_selection(model_type):
    """Get a model selection from the session state"""
    return st.session_state["models"].get(model_type, "")

def save_content_ideas(ideas):
    """Save generated content ideas to the session state"""
    st.session_state["content_ideas"] = ideas

def get_content_ideas():
    """Get the generated content ideas from the session state"""
    return st.session_state["content_ideas"]

def reset_workflow():
    """Reset the entire workflow state"""
    # Keep API keys but reset everything else
    api_keys = st.session_state["api_keys"].copy()
    
    # Reset all state
    initialize_session_state()
    
    # Restore API keys
    st.session_state["api_keys"] = api_keys
    
    # Reset to setup step
    st.session_state["current_step"] = "setup"
