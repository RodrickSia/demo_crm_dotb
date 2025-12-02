import streamlit as st
from services.api_service import fetch_lead_score


def render_lead_score_button(user_id):
    st.markdown('<div class="action-card">', unsafe_allow_html=True)
    
    # Weight sliders
    st.markdown("### Customize Scoring Weights")
    st.markdown("<p style='font-size: 12px; color: #6b7280;'>Adjust importance of each factor (must sum to 1.0)</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        demographics = st.slider(
            "Demographics",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.05,
            key="demographics_weight"
        )
        
        acedemic_background = st.slider(
            "Academic Background",
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.05,
            key="acedemic_background_weight"
        )
        
        activities_history = st.slider(
            "Activities History",
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.05,
            key="activities_history_weight"
        )
    
    with col2:
        payment_history = st.slider(
            "Payment History",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.05,
            key="payment_history_weight"
        )
        
        learning_history = st.slider(
            "Learning History",
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.05,
            key="learning_history_weight"
        )
    
    # Calculate total weight
    total_weight = demographics + acedemic_background + activities_history + payment_history + learning_history
    
    # Display weight sum with color coding
    if abs(total_weight - 1.0) < 0.01:
        st.markdown(f"<p style='color: #22c55e; font-weight: bold;'>Total: {total_weight:.2f} ✓</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color: #ef4444; font-weight: bold;'>Total: {total_weight:.2f} (must be 1.0)</p>", unsafe_allow_html=True)
    
    # Button is only enabled if weights sum to 1.0
    button_disabled = abs(total_weight - 1.0) >= 0.01
    
    if st.button("Get Lead Score", key="lead_score_btn", use_container_width=True, disabled=button_disabled):
        with st.spinner("Calculating AI lead score..."):
            weights = {
                'demographics': demographics,
                'acedemic_background': acedemic_background,
                'activities_history': activities_history,
                'payment_history': payment_history,
                'learning_history': learning_history
            }
            data = fetch_lead_score(user_id, weights=weights)
            st.session_state['lead_score_data'] = data
    
    if 'lead_score_data' in st.session_state:
        data = st.session_state['lead_score_data']
        score = data.get('score', 0)
        explanation = data.get('explanation', '')
        progress_degrees = int((score / 100) * 360)
        st.markdown(f"""
        <div class="score-circle" style="background: conic-gradient(#4ade80 {progress_degrees}deg, #e5e7eb {progress_degrees}deg);">
            <div class="score-inner">{score}</div>
        </div>
        <p class="action-title">Lead Score</p>
        <div style="background: white; color: #1f2937; padding: 12px; border-radius: 8px; margin-top: 10px; text-align: left; font-size: 13px;">
            <strong>Why this score?</strong><br/>
            <p style="margin-top: 6px; line-height: 1.5;">{explanation}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="score-circle" style="background: #e5e7eb;">
            <div class="score-inner" style="color: #9ca3af;">?</div>
        </div>
        <p class="action-title">Lead Score</p>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
