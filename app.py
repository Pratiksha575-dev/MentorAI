import streamlit as st
from database import init_db
from ui.styles import load_styles
from ui.sidebar import render_sidebar

from ui.pages.home import render_home
from ui.pages.register_mentor import render_register_mentor
from ui.pages.create_group import render_create_group
from ui.pages.directory import render_directory
from ui.pages.ml_insights import render_ml_insights
from ui.pages.graph_ml import render_graph_ml
from ui.pages.mentor_match import render_mentor_match

st.set_page_config(
    page_title="MentorAI",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global HTML Fix
_original_markdown = st.markdown
def _connectai_markdown(body="", *args, **kwargs):
    if kwargs.get("unsafe_allow_html", False) and isinstance(body, str):
        body = "\n".join([line.lstrip() for line in body.splitlines()]).strip()
    return _original_markdown(body, *args, **kwargs)
st.markdown = _connectai_markdown

# Styles
load_styles()

# DB
init_db()

# Session State Defaults
defaults = {
    "current_page": "Dashboard"
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Sidebar
page = render_sidebar()

# Routing
if page == "Dashboard":
    render_home()
elif page == "Register Mentor":
    render_register_mentor()
elif page == "Create Student Group":
    render_create_group()
elif page == "Directory":
    render_directory()
elif page == "ML Insights":
    render_ml_insights()
elif page == "Neural Web":
    render_graph_ml()
elif page == "Run Allocation":
    render_mentor_match()
