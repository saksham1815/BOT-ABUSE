import streamlit as st
from components.cards import metric_card
from components.charts import donut, gauge, geo_map
from llm.ollama_client import ask_llm
from llm.prompts import executive_prompt


def render(df, intel):
    st.title("Executive Overview")

    # -------------------------
    # KPI Cards
    # -------------------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Total Requests", f"{intel['total_requests']:,.0f}")

    with c2:
        metric_card("ATO Requests", f"{intel['login_requests']:,.0f}")

    with c3:
        metric_card("Scraping Requests", f"{intel['scraping_requests']:,.0f}")

    with c4:
        metric_card("Alerts", len(intel["alerts"]))

    # -------------------------
    # AI Summary
    # -------------------------
    with st.spinner("Generating executive insights..."):
        summary = ask_llm(executive_prompt(intel))

    st.subheader("Executive Summary")
    st.info(summary)

    # -------------------------
    # Charts
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            donut(
                ["Humans", "Bots", "Suspicious"],
                [68, 21, 11],
                "Human Authenticity Score"
            ),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            gauge(
                intel["frictionless_score"],
                "Frictionless Control Score"
            ),
            use_container_width=True
        )

    # -------------------------
    # Threat Map
    # -------------------------
    st.subheader("Threat Origin Map 🌍")

    st.plotly_chart(
        geo_map(intel["geo"]),
        use_container_width=True
    )

    # -------------------------
    # Alerts
    # -------------------------
    if intel["alerts"]:
        st.subheader("Active Alerts")

        for a in intel["alerts"]:
            st.error(
                f"{a['severity']} - {a['message']}"
            )