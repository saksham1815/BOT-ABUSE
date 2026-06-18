import streamlit as st
from llm.ollama_client import ask_llm


def ato_prompt(intel):
    return f"""
You are a fraud prevention strategist.

Login Requests: {intel['login_requests']}
Alerts: {len(intel['alerts'])}

Explain:
1. likely attack type
2. severity
3. best mitigations

Keep concise and executive friendly.
"""


def render(df, intel):
    st.title("ATO Defense")

    st.metric("Login Requests", f"{intel['login_requests']:,.0f}")
    st.metric("Estimated Attack Rate", "8.4%")
    st.metric("Session Trust Score", "71/100")

    with st.spinner("Analyzing login abuse..."):
        summary = ask_llm(ato_prompt(intel))

    st.subheader("Threat Assessment")
    st.warning(summary)