import streamlit as st


def render_users_metrics(df):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", len(df))
    with col2:
        if "created_at" in df.columns:
            st.metric("Latest Entry", str(df["created_at"].max())[:10] if not df.empty else "N/A")
        else:
            st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Data Retrieved", "✅ Success")


def render_search_bar():
    return st.text_input("🔍 Search students", placeholder="Search by any field...")


def filter_dataframe(df, search_term):
    if search_term:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]
        st.info(f"Found {len(filtered_df)} matching students")
        return filtered_df
    return df


def render_data_table(df):
    st.dataframe(
        df,
        use_container_width=True,
        height=600,
        hide_index=True
    )


def render_export_options(df):
    st.markdown("---")
    col1, col2 = st.columns([1, 4])
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="students_data.csv",
            mime="text/csv"
        )
    with col2:
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
