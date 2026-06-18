import streamlit as st

def init_state():
    defaults = {
        "bot_blocked": 84,
        "human_friction": 2.1,
        "annual_savings": 2400000,
        "login_requests": 145000,
        "scraper_requests": 18400000,
        "ticket_inventory_saved": 12000
    }

    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v