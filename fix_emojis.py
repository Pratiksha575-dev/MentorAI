import codecs

# 1. Fix config/constants.py
with codecs.open('config/constants.py', 'r', 'utf-8') as f:
    content = f.read()
    
# We will just rewrite the navigation and trait meta
constants_code = '''
NAVIGATION = [
    ("HOME", "??", "Dashboard"),
    ("REGISTER_MENTOR", "?????", "Register Mentor"),
    ("CREATE_GROUP", "??", "Create Student Group"),
    ("DIRECTORY", "??", "Directory"),
    ("MENTOR_MATCH", "??", "Run Allocation"),
]

DOMAIN_OPTIONS = [
    "Fintech",
    "Education",
    "Healthcare",
    "Environment / Sustainability",
    "E-commerce",
    "Gaming",
    "Machine Learning",
    "Natural Language Processing (NLP)",
    "Computer Vision",
    "Data Science",
    "App Development",
    "Web Development",
    "Cloud Computing",
    "Cybersecurity",
    "Blockchain",
    "Robotics",
    "IoT (Internet of Things)"
]

TRAIT_META = {
    "Extraversion": {"color": "#3b82f6", "icon": "???"},
    "Neuroticism": {"color": "#ef4444", "icon": "??"},
    "Agreeableness": {"color": "#10b981", "icon": "??"},
    "Conscientiousness": {"color": "#f59e0b", "icon": "??"},
    "Openness": {"color": "#8b5cf6", "icon": "??"}
}

CLUSTER_INFO = {}
'''
with codecs.open('config/constants.py', 'w', 'utf-8') as f:
    f.write(constants_code)

# 2. Fix ui/sidebar.py
sidebar_code = '''
import streamlit as st
from config.constants import NAVIGATION

def render_sidebar():
    with st.sidebar:
        st.markdown(
            \"\"\"
            <div class="sidebar-logo">
                ?? MentorAI
            </div>
            <div class="sidebar-tagline">
                Intelligent Mentor-Mentee Project Alignment
            </div>
            \"\"\",
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
'''
with codecs.open('ui/sidebar.py', 'w', 'utf-8') as f:
    f.write(sidebar_code)
    
# 3. Fix ui/pages/home.py
home_code = '''
import streamlit as st
from database import get_all_mentors, get_all_groups
from ui.components import page_header

def render_home():
    page_header("MentorAI Dashboard", "Command center for the mentorship program.", "??")
    
    mentors = get_all_mentors()
    groups = get_all_groups()
    
    c1, c2 = st.columns(2)
    c1.metric("Registered Mentors", len(mentors))
    c2.metric("Student Groups", len(groups))
    
    st.markdown("### Welcome to MentorAI v2")
    st.write("Use the sidebar to register new mentors, create student groups, and run the AI allocation engine.")
'''
with codecs.open('ui/pages/home.py', 'w', 'utf-8') as f:
    f.write(home_code)
