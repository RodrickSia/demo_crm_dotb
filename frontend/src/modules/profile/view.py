import streamlit as st
from src.shared.api import fetch_all_students, fetch_user_data
from src.shared.ui.styles import ACTION_CARD_CSS
from src.shared.config import ENDPOINTS_CONFIG
from src.modules.crm.cards import (
    render_lead_score_button,
    render_activity_summary_button,
    render_followup_action_button
)
from src.modules.profile.components import (
    render_user_selector,
    render_basic_info,
    render_data_tabs,
    render_data_summary
)


def render_profile_page():
    st.set_page_config(layout="wide", page_title="User Profile", page_icon="👤")

    st.title("User Profile")
    st.write("Comprehensive view of student data and AI-powered insights")

    students_data = fetch_all_students()

    if students_data:
        selected_user_id = render_user_selector(students_data)
        
        user_details = next((s for s in students_data if s.get('id') == selected_user_id), None)
        
        if user_details:
            st.header(f"{user_details.get('name', 'Unknown')} {user_details.get('surname', '')}")
            st.write(f"Student ID: {user_details.get('id', 'N/A')}")
            
            st.markdown("---")
            
            render_basic_info(user_details)
            
            st.markdown("---")
            
            st.subheader("AI-Powered Insights")
            
            st.markdown(ACTION_CARD_CSS, unsafe_allow_html=True)
            
            action_cols = st.columns(3)
            
            with action_cols[0]:
                render_lead_score_button(selected_user_id)
            
            with action_cols[1]:
                render_activity_summary_button(selected_user_id)
            
            with action_cols[2]:
                render_followup_action_button(selected_user_id)
            
            st.markdown("---")
            
            st.subheader("Student Data")
            
            render_data_tabs(selected_user_id, ENDPOINTS_CONFIG, fetch_user_data)
            
            render_data_summary(selected_user_id, ENDPOINTS_CONFIG, fetch_user_data)
        
        else:
            st.error("User details not found.")

    else:
        st.error("No Users Available")
        st.info("Make sure the backend API is running at http://127.0.0.1:8000")
        st.code("python backend/app.py", language="bash")
