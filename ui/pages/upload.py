import streamlit as st
from ui.utils.state_management import mark_step_complete, go_to_next_step

def show():
    """Display the upload & scheduling page"""
    st.markdown("## 4️⃣ Upload & Schedule")
    st.caption("Review, upload, and schedule your content")
    
    # Create tabs for the upload workflow
    review_tab, upload_tab, schedule_tab = st.tabs(["Review Content", "Upload", "Schedule"])
    
    # Tab 1: Review Content
    with review_tab:
        st.markdown("### Review Content")
        st.caption("Review your generated content before upload")
        
        # Placeholder for content review
        st.text("This tab will show your generated videos for review.")
    
    # Tab 2: Upload Content
    with upload_tab:
        st.markdown("### Upload Content")
        st.caption("Upload your content to selected platforms")
        
        # Placeholder for upload interface
        st.text("This tab will allow you to upload content to your selected platforms.")
        
        # Upload button placeholder
        if st.button("Upload as Private", key="upload_private_btn"):
            with st.spinner("Uploading content..."):
                # Placeholder for actual upload logic
                st.success("Content uploaded as private for review!")
    
    # Tab 3: Schedule Content
    with schedule_tab:
        st.markdown("### Schedule Content")
        st.caption("Schedule your content for future publication")
        
        # Placeholder for scheduling interface
        st.text("This tab will allow you to schedule your uploaded content.")
        
        # Schedule options
        st.markdown("#### Publication Date")
        st.date_input("Select publication date")
        
        st.markdown("#### Publication Time")
        st.time_input("Select publication time")
        
        # Staggered release option
        st.checkbox("Stagger release times (30 min between each post)")
        
        # Schedule button placeholder
        if st.button("Schedule Publication", key="schedule_btn"):
            with st.spinner("Scheduling content..."):
                # Placeholder for actual scheduling logic
                st.success("Content scheduled for publication!")
    
    # Add navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Back to Generation"):
            st.session_state["current_step"] = "generation"
            st.rerun()
    
    with col3:
        if st.button("Continue to Analytics ➡️"):
            # Mark this step as complete
            mark_step_complete("upload")
            # Go to next step
            go_to_next_step()
            st.rerun()
