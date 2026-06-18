import streamlit as st

from core.theme import apply_theme
from core.database import init_db, save_alert
from engines.log_parser import load_logs
from engines.detection_engine import analyze_logs
from components.sidebar import render_sidebar

from pages import (
    executive,
    ato,
    scraping,
    ticketing,
    risk,
    scenarios,
    reports,
    rule_assistant,
    copilot,
    settings,
    bot_intelligence
)


# -------------------
# App Config
# -------------------

st.set_page_config(
    page_title="Bot Abuse Intelligence Platform",
    layout="wide",
    page_icon="🛡️"
)


apply_theme()
init_db()


# -------------------
# Sidebar
# -------------------

page = render_sidebar()


uploaded = st.sidebar.file_uploader(
    "Upload CSV Logs",
    type=["csv"]
)


# -------------------
# Load Logs
# -------------------

if uploaded:
    df = load_logs(uploaded)

else:
    df = load_logs(
        "data/data_3.csv"
    )


# -------------------
# Intelligence Engine
# -------------------

intel = analyze_logs(df)


# -------------------
# Save Alerts
# -------------------

if "alerts_saved" not in st.session_state:

    for alert in intel.get("alerts", []):

        save_alert(
            alert.get("type"),
            alert.get("message"),
            alert.get("severity")
        )


    st.session_state["alerts_saved"] = True



# -------------------
# Pages
# -------------------

routes = {

    "Executive":
        executive.render,

    "ATO":
        ato.render,

    "Scraping":
        scraping.render,

    "Ticketing":
        ticketing.render,

    "Risk":
        risk.render,

    "Scenarios":
        scenarios.render,

    "Reports":
        reports.render,

    "Rule Assistant":
        rule_assistant.render,

    "Bot Intelligence":
        bot_intelligence.render,

    "AI Copilot":
        copilot.render,

    "Settings":
        settings.render
}



# -------------------
# Render Selected Page
# -------------------

if page in routes:

    routes[page](
        df,
        intel
    )

else:

    st.error(
        "Invalid page selected"
    )