import streamlit as st
import pandas as pd
from src.shared.api import fetch_all_students
from src.modules.users.components import (
    render_search_bar,
    filter_dataframe,
    render_data_table,
    render_export_options
)


def render_users_page():
    st.set_page_config(layout="wide", page_title="Users", page_icon="👥")

    st.title("All Users")
    st.write("Manage and view all students in the system")

    with st.spinner("Loading students..."):
        students_data = fetch_all_students()

    if students_data:
        df = pd.DataFrame(students_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Students", len(df))
        
        with col2:
            if "created_at" in df.columns:
                st.metric("Latest Entry", str(df["created_at"].max())[:10] if not df.empty else "N/A")
            else:
                st.metric("Data Columns", len(df.columns))
        
        with col3:
            st.metric("Status", "Active")
        
        with col4:
            st.metric("Database", "Connected")
        
        st.markdown("---")
        
        search_term = render_search_bar()
        filtered_df = filter_dataframe(df, search_term)
        
        render_data_table(filtered_df)
        
        render_export_options(filtered_df)

    else:
        st.error("No Data Available")
        st.info("Make sure the backend API is running at http://127.0.0.1:8000")
        st.code("python backend/app.py", language="bash")
