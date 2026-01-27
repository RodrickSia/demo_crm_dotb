import streamlit as st


def apply_custom_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    h1 {
        color: #1f2937;
        font-weight: 700;
        padding-bottom: 1rem;
        border-bottom: 3px solid #3b82f6;
    }
    
    h2 {
        color: #374151;
        font-weight: 600;
        margin-top: 2rem;
    }
    
    h3 {
        color: #4b5563;
        font-weight: 500;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f9fafb;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f9fafb;
        border-radius: 8px;
        font-weight: 600;
        padding: 1rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] .stSelectbox {
        margin-bottom: 1.5rem;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: white;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: white;
        color: #667eea;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.75rem 1.5rem;
        border: 2px solid white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 100%;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.9);
        color: #764ba2;
        border-color: white;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    /* Sidebar page navigation links */
    [data-testid="stSidebarNav"] [data-testid="stSidebarNavLink"] {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
        font-weight: 500;
        font-size: 1rem;
        color: white;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebarNav"] [data-testid="stSidebarNavLink"]:hover {
        background: rgba(255, 255, 255, 0.25);
        color: white;
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="stSidebarNav"] [data-testid="stSidebarNavLink"][aria-current="page"] {
        background: white;
        color: #667eea;
        border-color: white;
        font-weight: 600;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
        padding: 1rem;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #3b82f6;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Action cards gradient backgrounds */
    .gradient-card-1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .gradient-card-2 {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .gradient-card-3 {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #e5e7eb;
    }
    </style>
    """, unsafe_allow_html=True)


def render_metric_card(label, value):
    st.markdown(f"""
    <div class="card" style="text-align: center; padding: 1.5rem;">
        <p style="color: #6b7280; font-size: 0.9rem; margin: 0; font-weight: 500;">{label}</p>
        <p style="color: #1f2937; font-size: 2rem; margin: 0.5rem 0 0 0; font-weight: 700;">{value}</p>
    </div>
    """, unsafe_allow_html=True)


def render_header(title, subtitle=None):
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="margin: 0; color: #1f2937; font-size: 2.5rem;">{title}</h1>
        {f'<p style="color: #6b7280; font-size: 1.1rem; margin-top: 0.5rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_divider():
    st.markdown('<hr style="margin: 2rem 0; border-top: 2px solid #e5e7eb;">', unsafe_allow_html=True)


def render_empty_state(title, message):
    st.markdown(f"""
    <div style="text-align: center; padding: 4rem 2rem; background: #f9fafb; border-radius: 12px;">
        <h3 style="color: #374151; margin-bottom: 0.5rem;">{title}</h3>
        <p style="color: #6b7280; font-size: 1rem;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
