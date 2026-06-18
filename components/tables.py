import streamlit as st


def data_table(df):
    st.dataframe(df, use_container_width=True)