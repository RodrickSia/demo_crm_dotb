import streamlit as st
from src.shared.api import fetch_lead_score, fetch_activity_summary, fetch_followup_action
from src.shared.config import FOLLOWUP_ACTION_COLORS


def render_lead_score_button(user_id):
    if st.button("Generate Lead Score", key="score_btn", help="AI-powered lead scoring"):
        with st.spinner("Analyzing lead quality..."):
            result = fetch_lead_score(user_id)
            score = result.get("score", 0)
            explanation = result.get("explanation", "")
            
            st.markdown(f"""
            <div class="action-card gradient-card-1">
                <div class="score-circle">
                    <div class="score-inner">{score}</div>
                </div>
                <div class="action-title">Lead Score</div>
                <p>{explanation}</p>
            </div>
            """, unsafe_allow_html=True)


def render_activity_summary_button(user_id):
    if st.button("Summarize Activity", key="summary_btn", help="Get key insights from activity history"):
        with st.spinner("Analyzing activities..."):
            result = fetch_activity_summary(user_id)
            summary = result.get("summary", "")
            explanation = result.get("explanation", "")
            
            st.markdown(f"""
            <div class="action-card gradient-card-2">
                <div style="font-size: 40px; margin-bottom: 10px;">📊</div>
                <div class="action-title">Activity Summary</div>
                <p style="font-size: 0.9rem; margin-top: 10px;">{summary}</p>
                <div style="margin-top: 15px; font-size: 0.85rem; background: rgba(255,255,255,0.2); padding: 10px; border-radius: 8px;">
                    <strong>Key Insights:</strong><br>{explanation}
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_followup_action_button(user_id):
    if st.button("Suggest Next Action", key="action_btn", help="Recommended next step"):
        with st.spinner("Determining best next step..."):
            result = fetch_followup_action(user_id)
            action = result.get("action", "Unknown")
            explanation = result.get("explanation", "")
            
            color = FOLLOWUP_ACTION_COLORS.get(action, "#6b7280")
            
            st.markdown(f"""
            <div class="action-card gradient-card-3">
                <div style="font-size: 40px; margin-bottom: 10px;">🚀</div>
                <div class="action-title">Recommended Action</div>
                <div style="background: white; color: {color}; padding: 8px 16px; border-radius: 20px; font-weight: bold; margin: 10px auto; display: inline-block;">
                    {action}
                </div>
                <p style="margin-top: 10px;">{explanation}</p>
            </div>
            """, unsafe_allow_html=True)
