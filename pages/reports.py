import streamlit as st

from llm.ollama_client import ask_llm
from llm.prompts import (
    report_prompt,
    email_prompt
)

from engines.email_engine import send_email

from core.config import (
    DEFAULT_ANALYST,
    DEFAULT_EXECUTIVE
)


def render(df, intel):

    st.title("Reports & Communications")

    st.subheader("Incident Scope")

    col1, col2, col3 = st.columns(3)

    with col1:
        ato = st.checkbox(
            "ATO / Credential Stuffing",
            value=True
        )

    with col2:
        scraping = st.checkbox(
            "Scraping / API Abuse",
            value=True
        )

    with col3:
        ticketing = st.checkbox(
            "Ticketing Abuse",
            value=True
        )

    selected = []

    if ato:
        selected.append("ATO")

    if scraping:
        selected.append("Scraping")

    if ticketing:
        selected.append("Ticketing")

    modules = ", ".join(selected)

    st.divider()

    st.subheader("Recipients")

    exec_email = st.text_input(
        "Executive Email",
        value=DEFAULT_EXECUTIVE
    )

    analyst_email = st.text_input(
        "Analyst Email",
        value=DEFAULT_ANALYST
    )

    audience = st.selectbox(
        "Audience",
        [
            "Executive Leadership",
            "SOC Analysts",
            "Fraud Team",
            "Operations",
            "Board"
        ]
    )

    st.divider()

    # REPORT GENERATION

    if st.button("Generate Executive Report"):

        with st.spinner("Generating report..."):

            report = ask_llm(
                report_prompt(intel, modules)
            )

        st.session_state["generated_report"] = report

    # DISPLAY REPORT

    if "generated_report" in st.session_state:

        report = st.session_state["generated_report"]

        st.subheader("Generated Report")

        st.markdown(report)

        st.download_button(
            "Download Report",
            report,
            file_name="bot_abuse_report.md"
        )

        st.divider()

        # EMAIL GENERATION

        st.subheader("Executive Email")

        with st.spinner("Generating email draft..."):

            email_body = ask_llm(
                email_prompt(report, audience)
            )

        full_email = f"""
                Dear Team,

                {email_body}

                Regards,
                Security Operations
                """

        editable_email = st.text_area(
            "Generated Email",
            value=full_email,
            height=350
        )

        st.divider()

        col1, col2 = st.columns(2)

        # SEND TO EXECUTIVE

        with col1:

            if st.button("Send to Executive"):

                success, msg = send_email(
                    exec_email,
                    "Bot Abuse Intelligence Report",
                    editable_email
                )

                if success:
                    st.success(msg)
                else:
                    st.error(msg)

        # SEND TO ANALYST

        with col2:

            if st.button("Send to Analyst"):

                success, msg = send_email(
                    analyst_email,
                    "Bot Abuse Technical Incident Report",
                    editable_email
                )

                if success:
                    st.success(msg)
                else:
                    st.error(msg)