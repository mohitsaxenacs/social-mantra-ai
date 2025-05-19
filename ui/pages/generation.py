import streamlit as st
from ui.utils.state_management import mark_step_complete, go_to_next_step, get_content_niche

def show():
    """Display the content generation page"""
    st.markdown("## 3️⃣ Content Generation")
    st.caption("Generate content ideas, scripts, audio, and videos")
    
    # Get content niche from session state
    niche = get_content_niche()
    
    # Create tabs for the different generation steps
    ideas_tab, metadata_tab, audio_tab, video_tab = st.tabs(["Content Ideas", "Metadata", "Audio", "Video"])
    
    # Tab 1: Content Ideas
    with ideas_tab:
        st.markdown("### Generate Content Ideas")
        st.caption(f"Create viral content ideas for your niche: {niche}")
        
        # Placeholder for idea generation
        st.text("This tab will allow you to generate and select viral content ideas.")
        
        if st.button("Generate Ideas", key="gen_ideas_btn"):
            with st.spinner("Generating content ideas..."):
                # Placeholder for actual generation logic
                st.success("Generated 10 content ideas!")
    
    # Tab 2: Metadata
    with metadata_tab:
        st.markdown("### Generate Metadata")
        st.caption("Create optimized metadata for each platform")
        
        # Placeholder for metadata generation
        st.text("This tab will show platform-specific metadata for each content idea.")
    
    # Tab 3: Audio
    with audio_tab:
        st.markdown("### Generate Audio")
        st.caption("Create voiceovers and background music")
        
        # Placeholder for audio generation
        st.text("This tab will allow you to generate and preview voiceovers and background music.")
    
    # Tab 4: Video
    with video_tab:
        st.markdown("### Generate Videos")
        st.caption("Create videos with selected models")
        
        # Placeholder for video generation
        st.text("This tab will allow you to generate videos using the selected AI models.")
    
    # Add navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back to Research"):
            st.session_state["current_step"] = "research"
            st.rerun()
    
    with col3:
        if st.button("Continue to Upload →"):
            # Mark this step as complete
            mark_step_complete("generation")
            # Go to next step
            go_to_next_step()
            st.rerun()
