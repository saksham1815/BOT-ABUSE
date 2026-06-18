import streamlit as st

def render_sidebar():
    st.sidebar.title("🛡️ Abuse Intel")
    return st.sidebar.radio(
        "Navigation",
        [
            "Executive",
            "ATO",
            "Scraping",
            "Ticketing",
            "Risk",
            "Scenarios",
            "Reports",
            "Rule Assistant",
            "Bot Intelligence",
            "AI Copilot",
            "Settings"
        ]
    )