import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    .stApp {background:#0b1020;color:white;}
    section[data-testid="stSidebar"]{background:#111827;}
    div[data-testid="metric-container"]{
        background:#111827;
        border:1px solid #1f2937;
        padding:10px;
        border-radius:14px;
    }
    </style>
    """, unsafe_allow_html=True)