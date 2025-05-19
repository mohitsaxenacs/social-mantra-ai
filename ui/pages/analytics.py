import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def show():
    """Display the analytics page"""
    st.markdown("## 5️⃣ Performance Analytics")
    st.caption("Track and analyze your content performance")
    
    # Create tabs for the analytics
    overview_tab, platform_tab, recommendations_tab = st.tabs(["Performance Overview", "Platform Comparison", "Recommendations"])
    
    # Tab 1: Performance Overview
    with overview_tab:
        st.markdown("### Performance Overview")
        st.caption("Overview of your content performance across platforms")
        
        # Placeholder for overview metrics
        st.text("This tab will show an overview of your content performance.")
        
        # Generate sample data for demonstration
        with st.container():
            # Create columns for metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(label="Total Views", value="24,892", delta="+12%")
            
            with col2:
                st.metric(label="Engagement Rate", value="5.7%", delta="+2.1%")
            
            with col3:
                st.metric(label="Shares", value="1,204", delta="+18%")
            
            with col4:
                st.metric(label="New Followers", value="843", delta="+9%")
        
        # Sample chart
        st.markdown("### Weekly Performance")
        chart_data = pd.DataFrame(
            np.random.randn(7, 3) * [3000, 200, 500] + [15000, 1000, 2500],
            index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            columns=["Views", "Likes", "Shares"]
        )
        st.bar_chart(chart_data)
    
    # Tab 2: Platform Comparison
    with platform_tab:
        st.markdown("### Platform Comparison")
        st.caption("Compare content performance across different platforms")
        
        # Placeholder for platform comparison
        st.text("This tab will show a comparison of your content performance across platforms.")
        
        # Sample platform comparison
        platform_data = pd.DataFrame({
            "Platform": ["YouTube Shorts", "Facebook Reels", "Instagram Reels"],
            "Views": [15432, 5821, 3639],
            "Likes": [982, 421, 275],
            "Comments": [143, 52, 38],
            "Shares": [721, 312, 171],
            "Avg. Watch Time": ["0:28", "0:21", "0:19"],
            "Engagement Rate": ["6.3%", "5.2%", "4.8%"]
        })
        
        st.dataframe(platform_data)
        
        # Sample platform metrics chart
        st.markdown("### Platform Metrics Comparison")
        chart_data = pd.DataFrame([
            {"Platform": "YouTube", "Views": 15432, "Likes": 982, "Shares": 721},
            {"Platform": "Facebook", "Views": 5821, "Likes": 421, "Shares": 312},
            {"Platform": "Instagram", "Views": 3639, "Likes": 275, "Shares": 171}
        ])
        
        # Pivot the data for charting
        chart_pivot = pd.melt(chart_data, id_vars=['Platform'], value_vars=['Views', 'Likes', 'Shares'])
        chart_pivot['value'] = chart_pivot['value'].astype(float)
        
        st.bar_chart(chart_pivot, x="Platform", y="value", color="variable")
    
    # Tab 3: Recommendations
    with recommendations_tab:
        st.markdown("### Content Recommendations")
        st.caption("Get recommendations to improve your content performance")
        
        # Placeholder for recommendations
        st.text("This tab will provide recommendations based on your content performance.")
        
        # Sample recommendations
        st.markdown("#### YouTube Shorts Recommendations")
        st.info("""
        - **Optimal Length**: Your 25-30 second videos perform best
        - **Post Time**: Post between 6-8 PM for maximum engagement
        - **Content Type**: Tutorial-style content receives 32% more views
        - **Hashtags**: Use trending hashtags like #learnontiktok in your descriptions
        """)
        
        st.markdown("#### Facebook Reels Recommendations")
        st.info("""
        - **Optimal Length**: Keep videos under 20 seconds for highest completion rate
        - **Captions**: Videos with captions receive 48% more engagement
        - **Sound**: Original audio performs better than trending sounds
        - **Call to Action**: Videos with a clear CTA get 27% more shares
        """)
        
        st.markdown("#### Instagram Reels Recommendations")
        st.info("""
        - **Hashtags**: Limit to 5-7 highly relevant hashtags
        - **Transitions**: Videos with transitions get 41% more views
        - **Trending Audio**: Using trending audio increases discovery by 35%
        - **Post Time**: Post between 9-11 AM for best results
        """)
    
    # Reset workflow button
    st.markdown("---")
    col1, col2 = st.columns([8, 2])
    
    with col2:
        if st.button("Start New Workflow"):
            # Reset the workflow state
            from ui.utils.state_management import reset_workflow
            reset_workflow()
            st.rerun()
