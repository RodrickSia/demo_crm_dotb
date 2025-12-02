import streamlit as st
from services.api_service import fetch_followup_action
from utils.config import FOLLOWUP_ACTION_COLORS


def render_followup_action_button(user_id):
    st.markdown('<div class="action-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">', unsafe_allow_html=True)
    
    if st.button("Get Next Follow-Up Action", key="followup_action_btn", use_container_width=True):
        with st.spinner("Analyzing next best action..."):
            data = fetch_followup_action(user_id)
            st.session_state['followup_action_data'] = data
    
    if 'followup_action_data' in st.session_state:
        data = st.session_state['followup_action_data']
        action = data.get('action', 'Unknown')
        explanation = data.get('explanation', '')
        color = FOLLOWUP_ACTION_COLORS.get(action, "#6b7280")
        st.markdown(f"""
        <div style="background: white; color: {color}; padding: 20px; border-radius: 10px; margin-top: 10px; font-size: 20px; font-weight: bold; text-align: center;">
            {action}
        </div>
        <p class="action-title" style="margin-top: 10px;">Recommended Action</p>
        <div style="background: white; color: #1f2937; padding: 12px; border-radius: 8px; margin-top: 10px; text-align: left; font-size: 13px;">
            <strong>Why this action?</strong><br/>
            <p style="margin-top: 6px; line-height: 1.5;">{explanation}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p style="margin-top: 40px; font-size: 14px;">Click to get recommended follow-up action</p>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
