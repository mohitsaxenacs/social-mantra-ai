import streamlit as st
from ui.utils.state_management import save_api_key, get_api_key

def api_input(key_name, label, help_text, placeholder="Enter your API key", password=True, url=None):
    """Reusable component for API key input with help tooltip
    
    Args:
        key_name: The identifier for this API key in session state
        label: Display label for the input
        help_text: Help text explaining what this key is for
        placeholder: Placeholder text for the input field
        password: Whether to mask the input as a password
        url: Optional URL for where to get the API key
    """
    # Get current value from session state
    current_value = get_api_key(key_name)
    
    # Create columns for label, input, and help button
    cols = st.columns([3, 6, 1])
    
    # Label column
    with cols[0]:
        st.markdown(f"<div style='margin-top: 12px; text-align: right;'><b>{label}:</b></div>", unsafe_allow_html=True)
    
    # Input column
    with cols[1]:
        # Create unique key for this input
        input_key = f"api_input_{key_name}"
        
        # Create the input field
        new_value = st.text_input(
            label="",
            value=current_value,
            placeholder=placeholder,
            type="password" if password else "default",
            key=input_key,
            label_visibility="collapsed",
            help=help_text  # Use Streamlit's built-in help parameter
        )
        
        # Save value when changed
        if new_value != current_value:
            save_api_key(key_name, new_value)
    
    # Help column is no longer needed as we're using the built-in help parameter
    
    # Show URL if provided
    if url:
        with cols[1]:
            st.caption(f"[Get your {label} here]({url})")
    
    return new_value

def api_file_input(key_name, label, help_text, url=None):
    """Component for API key files (like client_secrets.json)
    
    Args:
        key_name: The identifier for this API key in session state
        label: Display label for the input
        help_text: Help text explaining what this key is for
        url: Optional URL for where to get the API key
    """
    # Get current value from session state
    current_value = get_api_key(key_name)
    
    # Create columns for label, input, and help button
    cols = st.columns([3, 6, 1])
    
    # Label column
    with cols[0]:
        st.markdown(f"<div style='margin-top: 12px; text-align: right;'><b>{label}:</b></div>", unsafe_allow_html=True)
    
    # Input column
    with cols[1]:
        # Create unique key for this input
        input_key = f"api_file_{key_name}"
        
        # Create the file uploader with help text
        uploaded_file = st.file_uploader(
            label="",
            type=["json"],
            key=input_key,
            label_visibility="collapsed",
            help=help_text  # Use Streamlit's built-in help parameter
        )
        
        # Show current file if exists
        if current_value:
            st.caption(f"File uploaded: {current_value}")
        
        # Save file path when uploaded
        if uploaded_file is not None:
            # In a real app, we would save the file to disk here
            # For demo purposes, just store the filename
            filename = uploaded_file.name
            save_api_key(key_name, filename)
    
    # Show URL if provided
    if url:
        with cols[1]:
            st.caption(f"[Get your {label} here]({url})")
    
    return current_value
