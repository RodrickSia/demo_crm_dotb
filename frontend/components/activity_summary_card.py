import streamlit as st
from services.api_service import fetch_activity_summary


def render_activity_summary_button(user_id):
    st.markdown('<div class="action-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">', unsafe_allow_html=True)
    
    if st.button("Generate Activity Summary", key="activity_summary_btn", use_container_width=True):
        with st.spinner("Generating AI-powered summary..."):
            data = fetch_activity_summary(user_id)
            st.session_state['activity_summary_data'] = data
    
    if 'activity_summary_data' in st.session_state:
        data = st.session_state['activity_summary_data']
        summary_text = data.get('summary', '')
        explanation_text = data.get('explanation', '')
        
        st.markdown(f"""
        <div style="background: white; color: #1f2937; padding: 15px; border-radius: 10px; margin-top: 10px; text-align: left; font-size: 14px;">
            <strong>AI Activity Summary:</strong><br/>
            <p style="margin-top: 8px; line-height: 1.6;">{summary_text if summary_text else 'No summary available'}</p>
        </div>
        <div style="background: white; color: #1f2937; padding: 12px; border-radius: 8px; margin-top: 10px; text-align: left; font-size: 13px;">
            <strong>Key Insights & Recommendations:</strong><br/>
            <p style="margin-top: 6px; line-height: 1.5;">{explanation_text if explanation_text else 'No insights available'}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p style="margin-top: 40px; font-size: 14px;">Click to generate AI-powered activity summary</p>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
