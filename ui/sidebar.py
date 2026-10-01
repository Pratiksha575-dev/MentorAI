
import streamlit as st
from config.constants import NAVIGATION

def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-logo">
                🧠 MentorAI
            </div>
            <div class="sidebar-tagline">
                Intelligent Mentor-Mentee Project Alignment
            </div>
            """,
            unsafe_allow_html=True
        )
        st.divider()

        st.caption("NAVIGATION")
        labels = [f"{icon}  {label}" for _, icon, label in NAVIGATION]
        current_page = st.session_state.get("current_page", "Dashboard")
        
        try:
            default_index = [n[2] for n in NAVIGATION].index(current_page)
        except ValueError:
            default_index = 0

        selection = st.radio(
            "Go to",
            labels,
            index=default_index,
            label_visibility="collapsed"
        )
        
        selected_page = selection.split("  ", 1)[1]
        st.session_state.current_page = selected_page
        
        return selected_page
