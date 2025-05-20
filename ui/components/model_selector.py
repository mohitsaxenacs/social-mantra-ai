import streamlit as st
from ui.utils.state_management import save_model_selection, get_model_selection

def model_selector():
    """Component for selecting AI models for content generation
    
    Returns:
        dict: Dictionary of selected models {model_type: model_name}
    """
    # Initialize models if not in session state
    if "models" not in st.session_state:
        st.session_state["models"] = {
            "voice": "gtts",  # Default to free option
            "video": "placeholder",  # Default to placeholder
            "image": "dalle_mini"  # Default to free option
        }
    
    # Get current model selections
    try:
        current_models = {
            "voice": get_model_selection("voice"),
            "video": get_model_selection("video"),
            "image": get_model_selection("image")
        }
    except Exception as e:
        print(f"Error getting model selections: {e}")
        # Fallback to defaults
        current_models = {
            "voice": "gtts",
            "video": "placeholder",
            "image": "dalle_mini"
        }
        # Save defaults to session state
        for model_type, model_name in current_models.items():
            save_model_selection(model_type, model_name)
    
    # Voice Generation Section
    st.subheader("Voice Generation Models")
    st.caption("Select the model to use for generating voiceovers")
    
    # Create radio buttons for voice model selection
    voice_options = {
        "gtts": "Google Text-to-Speech (Free)",
        "elevenlabs_basic": "ElevenLabs Basic Voices (Free Trial)",
        "elevenlabs_premium": "ElevenLabs Premium Voices (Paid) - RECOMMENDED"
    }
    
    voice_model = st.radio(
        "Select Voice Model",
        options=list(voice_options.keys()),
        format_func=lambda x: voice_options[x],
        index=list(voice_options.keys()).index(current_models["voice"]) if current_models["voice"] in voice_options else 0,
        key="voice_model_selector"
    )
    
    # Help information about voice models
    with st.expander("Voice Model Comparison"):
        st.markdown("""
        | Model | Quality | Naturalness | Cost | API Required |
        | ----- | ------- | ----------- | ---- | ------------ |
        | Google TTS | Medium | Robotic | Free | No |
        | ElevenLabs Basic | High | Good | Free Trial | Yes |
        | ElevenLabs Premium | Excellent | Very Natural | $0.003/sec | Yes |
        
        **Our Recommendation (2025):** ElevenLabs Premium with the "Adam" (male) or "Rachel" (female) voices 
        provides the most natural-sounding results for viral social media content.
        """)
    
    # Save voice model selection if changed
    if voice_model != current_models["voice"]:
        save_model_selection("voice", voice_model)
    
    # Add a separator between sections
    st.markdown("---")
    
    # Image Generation Section (moved up before video for better visibility)
    st.subheader("Thumbnail Image Generation")
    st.caption("Select the model to use for generating thumbnail images")
    
    # Create radio buttons for image model selection with clear descriptions
    image_options = {
        "builtin_templates": "Basic Templates (Free)",
        "stable_diffusion": "Stable Diffusion (Free, Open Source)",
        "huggingface_free": "HuggingFace Free Models (Free)",
        "craiyon": "Craiyon AI (Free)",
        "dalle_mini": "DALL-E Mini (Free)",
        "stability_ai": "Stability AI (Paid)",
        "dalle3": "DALL-E 3 (Paid) - RECOMMENDED",
        "midjourney": "Midjourney v6 (Paid - Premium Quality)"
    }
    
    # Determine default selection based on session state
    current_image_model = current_models.get("image", "builtin_templates")
    default_index = 0
    if current_image_model in image_options:
        default_index = list(image_options.keys()).index(current_image_model)
    
    # Display radio buttons with clear options
    image_model = st.radio(
        "Select Image Model",
        options=list(image_options.keys()),
        format_func=lambda x: image_options[x],
        index=default_index,
        key="image_model_selector"
    )
    
    # Help information about image models
    with st.expander("Image Model Comparison"):
        st.markdown("""
        | Model | Quality | Style Range | Cost | API Required |
        | ----- | ------- | ----------- | ---- | ------------ |
        | Basic Templates | Simple | Very Limited | Free | No |
        | Stable Diffusion | Good | Wide | Free (Local) | No |
        | HuggingFace Free | Good | Wide | Free | No |
        | Craiyon AI | Basic | Good | Free | No |
        | DALL-E Mini | Basic | Limited | Free | No |
        | Stability AI | Good | Wide | ~$0.02/image | Yes |
        | DALL-E 3 | Excellent | Versatile | ~$0.04/image | Yes |
        | Midjourney v6 | Premium | Photorealistic | ~$0.10/image | Yes |
        
        **Free Options (2025):**
        - **Stable Diffusion**: The best free option that runs locally on your computer. Great quality but requires some GPU power.
        - **HuggingFace Free Models**: Access to various free AI image generators through simple API calls. Good balance of quality and ease of use.
        - **Craiyon AI**: Formerly DALL-E Mini, provides reasonable results without any API key.
        
        **Paid Recommendations (2025):** DALL-E 3 provides excellent quality thumbnails with good text integration,
        which is important for social media thumbnails. Midjourney v6 offers the highest visual quality but at a premium price.
        """)
    
    # Save image model selection if changed
    if image_model != current_models["image"]:
        save_model_selection("image", image_model)
    
    # Add a separator between sections
    st.markdown("---")
    
    # Video Generation Section
    st.subheader("Video Generation Models")
    st.caption("Select the model to use for generating videos")
    
    # Create radio buttons for video model selection
    video_options = {
        "placeholder": "Basic Placeholder Videos (Free)",
        "stable_video": "Stable Video Diffusion (Free)",
        "runway": "RunwayML Gen-2 (Paid) - RECOMMENDED",
        "pika": "Pika Labs (Paid - Premium Quality)"
    }
    
    video_model = st.radio(
        "Select Video Model",
        options=list(video_options.keys()),
        format_func=lambda x: video_options[x],
        index=list(video_options.keys()).index(current_models["video"]) if current_models["video"] in video_options else 0,
        key="video_model_selector"
    )
    
    # Help information about video models
    with st.expander("Video Model Comparison"):
        st.markdown("""
        | Model | Quality | Capabilities | Cost | API Required |
        | ----- | ------- | ------------ | ---- | ------------ |
        | Placeholder | Basic | Text over background | Free | No |
        | Stable Video | Medium | Simple animations | Free | No |
        | RunwayML Gen-2 | High | Realistic videos | ~$0.10/sec | Yes |
        | Pika Labs | Excellent | High-quality, complex | ~$0.25/sec | Yes |
        
        **Our Recommendation (2025):** RunwayML Gen-2 offers the best balance of quality and cost 
        for viral short-form videos. For premium results, Pika Labs produces the highest quality but at a higher cost.
        """)
    
    # Save video model selection if changed
    if video_model != current_models["video"]:
        save_model_selection("video", video_model)
    
    # Return the updated model selections
    return {
        "voice": voice_model,
        "video": video_model,
        "image": image_model
    }
