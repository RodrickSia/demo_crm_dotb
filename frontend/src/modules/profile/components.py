import streamlit as st
import pandas as pd


def render_user_selector(students_data):
    st.sidebar.header("Select User")
    
    user_options = {
        f"{student.get('id', 'N/A')} - {student.get('name', 'Unknown')} {student.get('surname', '')}": student.get('id')
        for student in students_data
    }
    
    selected_user_display = st.sidebar.selectbox(
        "Choose a user",
        options=list(user_options.keys())
    )
    
    selected_user_id = user_options[selected_user_display]
    
    if st.sidebar.button("Refresh All Data"):
        st.cache_data.clear()
        st.rerun()
    
    return selected_user_id


def render_weight_sliders():
    st.sidebar.markdown("---")
    st.sidebar.subheader("Lead Scoring Weights")
    with st.sidebar.expander("Adjust Weights", expanded=False):
        demographics = st.slider("Demographics", 0.0, 1.0, 0.1, 0.05)
        acedemic = st.slider("Academic Background", 0.0, 1.0, 0.2, 0.05)
        activities = st.slider("Activities History", 0.0, 1.0, 0.2, 0.05)
        payment = st.slider("Payment History", 0.0, 1.0, 0.3, 0.05)
        learning = st.slider("Learning History", 0.0, 1.0, 0.2, 0.05)
        
        total = demographics + acedemic + activities + payment + learning
        st.write(f"Total: {total:.2f}")
        
        if not (0.99 <= total <= 1.01):
            st.warning("Weights should sum to 1.0")
            
    return {
        "demographics": demographics,
        "acedemic_background": acedemic,
        "activities_history": activities,
        "payment_history": payment,
        "learning_history": learning
    }


def render_basic_info(user_details):
    with st.expander("Basic Information", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; text-align: center;">
                <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">User ID</p>
                <p style="color: #1f2937; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0 0 0;">{user_details.get('id', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; text-align: center;">
                <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">Name</p>
                <p style="color: #1f2937; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0 0 0;">{user_details.get('name', '')} {user_details.get('surname', '')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; text-align: center;">
                <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">Email</p>
                <p style="color: #1f2937; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0 0 0;">{user_details.get('email', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; text-align: center;">
                <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">Phone</p>
                <p style="color: #1f2937; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0 0 0;">{user_details.get('phone', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Complete Student Details:**")
        df_student = pd.DataFrame([user_details])
        st.dataframe(df_student, use_container_width=True, hide_index=True)


def render_data_tabs(user_id, endpoints_config, fetch_user_data_func):
    tabs = st.tabs([config['name'] for config in endpoints_config])
    
    for idx, config in enumerate(endpoints_config):
        with tabs[idx]:
            with st.spinner(f"Loading {config['name']}..."):
                data = fetch_user_data_func(user_id, config['endpoint'])
            
            if data and len(data) > 0:
                df = pd.DataFrame(data)
                
                st.info(f"Total {config['name']}: **{len(df)}**")
                
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"Download {config['name']} CSV",
                    data=csv,
                    file_name=f"user_{user_id}_{config['name'].lower()}.csv",
                    mime="text/csv",
                    key=f"download_{config['endpoint']}"
                )
            else:
                st.warning(f"No {config['name']} data found for this user.")


def render_data_summary(user_id, endpoints_config, fetch_user_data_func):
    st.markdown("---")
    st.subheader("Data Summary")
    
    summary_cols = st.columns(len(endpoints_config))
    for idx, config in enumerate(endpoints_config):
        data = fetch_user_data_func(user_id, config['endpoint'])
        count = len(data) if data else 0
        with summary_cols[idx]:
            st.metric(config['name'], count)
