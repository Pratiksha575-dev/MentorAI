import streamlit as st

def load_styles():
    st.markdown('''
        <style>
            /* Keep hamburger menu but remove white bar and deploy button */
            [data-testid="stHeader"] {background: rgba(0,0,0,0) !important;}
            header {background: rgba(0,0,0,0) !important;}
            [data-testid="stAppDeployButton"] {display: none !important;}
            [data-testid="stToolbar"] {display: none !important;}
            #MainMenu {display: none !important;}
            
            /* Align Sidebar and Main Content perfectly */
            .block-container {
                padding-top: 1rem !important;
                margin-top: 0 !important;
            }
            [data-testid="stSidebarUserContent"] {
                padding-top: 1rem !important;
            }
            
            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background-color: #12151e !important;
                border-right: 1px solid rgba(255,255,255,0.05);
            }
            .page-subtitle {
                font-size: 18px;
                color: #94a3b8;
                margin-bottom: 10px;
                font-weight: 300;
            }
            
            /* Global Typography */
            .stApp {
                font-family: 'Inter', sans-serif;
            }
            
            /* Sidebar styling */
            [data-testid="stSidebar"] {
                border-right: 1px solid rgba(255,255,255,0.05);
                backdrop-filter: blur(10px);
            }
            
            .sidebar-logo {
                font-size: 28px;
                font-weight: 800;
                color: #a78bfa;
                margin-bottom: 0px;
                text-align: center;
                text-shadow: 0px 0px 10px rgba(167, 139, 250, 0.5);
            }
            
            .sidebar-tagline {
                font-size: 12px;
                color: #94a3b8;
                margin-bottom: 20px;
                text-align: center;
                letter-spacing: 1px;
            }

            /* Main Header styling */
            .eyebrow {
                font-size: 14px;
                font-weight: 700;
                color: #8b5cf6;
                text-transform: uppercase;
                letter-spacing: 2px;
                margin-bottom: -10px;
            }
            
            .page-title {
                font-size: 48px;
                font-weight: 900;
                background: -webkit-linear-gradient(45deg, #a78bfa, #f472b6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }
            
            .page-subtitle {
                font-size: 18px;
                color: #94a3b8;
                margin-bottom: 40px;
                font-weight: 300;
            }

            /* Buttons */
            .stButton>button {
                background: linear-gradient(45deg, #8b5cf6, #d946ef);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 24px;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
            }
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5);
                border: none;
                color: white;
            }

            /* Cards & Expanders */
            .streamlit-expanderHeader {
                background: rgba(255, 255, 255, 0.03) !important;
                border-radius: 8px !important;
                font-size: 16px !important;
                font-weight: 600 !important;
            }
            [data-testid="stExpander"] {
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                margin-bottom: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            /* Trait Cards */
            .trait-card {
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(217, 70, 239, 0.1) 100%);
                border: 1px solid rgba(217, 70, 239, 0.2);
                border-radius: 12px;
                padding: 15px;
                text-align: center;
                transition: transform 0.2s ease;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .trait-card:hover {
                transform: translateY(-5px);
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(217, 70, 239, 0.2) 100%);
            }
            
            /* Inputs */
            .stTextInput>div>div>input {
                background: rgba(0,0,0,0.2);
                border: 1px solid rgba(255,255,255,0.1);
                color: white;
                border-radius: 6px;
            }
            
            /* Main container top margin fix */
            .block-container {
                padding-top: 2rem !important;
            }
            
            /* Progress bars */
            .stProgress > div > div > div > div {
                background-image: linear-gradient(to right, #8b5cf6, #d946ef);
            }
            
            /* Metric Cards */
            [data-testid="stMetricValue"] {
                font-size: 42px;
                font-weight: 800;
                color: #a78bfa;
            }
            [data-testid="metric-container"] {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255,255,255,0.05);
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            }
            
            /* Tables */
            table {
                width: 100%;
                border-collapse: collapse;
                background: rgba(0,0,0,0.2);
                border-radius: 8px;
                overflow: hidden;
            }
            th {
                background: rgba(139, 92, 246, 0.2);
                color: #e2e8f0;
                font-weight: 600;
                text-align: left;
                padding: 12px;
            }
            td {
                padding: 10px;
                border-bottom: 1px solid rgba(255,255,255,0.05);
            }
        </style>
    ''', unsafe_allow_html=True)
