import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

st.set_page_config(
    layout="wide",
    page_title="CRM Dashboard",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

st.title("CRM Dashboard")
st.write("Welcome to your Customer Relationship Management System")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Users")
    st.write("View and manage all students")

with col2:
    st.subheader("User Profile")
    st.write("Detailed user information & insights")

with col3:
    st.subheader("AI Features")
    st.write("Lead scoring & predictions")

st.markdown("---")

st.subheader("Getting Started")
st.write("Use the sidebar to navigate between different sections of the CRM system.")

st.write("- **Users:** Browse all students and search through their data")
st.write("- **User Profile:** View detailed information for individual students including all their activity")
st.write("- **AI Insights:** Get lead scores, activity summaries, and stage predictions")

st.info("Select a page from the sidebar to get started")
