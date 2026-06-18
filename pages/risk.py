import streamlit as st
import pandas as pd
import plotly.express as px

from llm.ollama_client import ask_llm


def calculate_endpoint_risk(df):

    endpoint_data = []

    grouped = df.groupby("url")

    for endpoint, group in grouped:

        total_hits = group["totalhitcount"].sum()

        blocked = len(
            group[
                group["requestresult"].astype(str).str.contains(
                    "BLOCK|CHALLENGE",
                    case=False,
                    na=False
                )
            ]
        )

        suspicious_agents = len(
            group[
                group["useragent"].astype(str).str.contains(
                    "python|curl|scrapy|headless|playwright|selenium|bot",
                    case=False,
                    na=False
                )
            ]
        )

        attack_hits = len(
            group[
                group["mainattack"].astype(str) != "None"
            ]
        )

        risk_score = (
            (blocked * 25)
            + (suspicious_agents * 20)
            + (attack_hits * 30)
            + (total_hits * 0.15)
        )

        risk_score = min(round(risk_score), 100)

        if risk_score >= 80:
            severity = "Critical"

        elif risk_score >= 60:
            severity = "High"

        elif risk_score >= 40:
            severity = "Medium"

        else:
            severity = "Low"

        endpoint_data.append({
            "Endpoint": endpoint,
            "Requests": int(total_hits),
            "Blocked Events": blocked,
            "Bot Signals": suspicious_agents,
            "Attack Events": attack_hits,
            "Risk Score": risk_score,
            "Severity": severity
        })

    risk_df = pd.DataFrame(endpoint_data)

    if not risk_df.empty:
        risk_df = risk_df.sort_values(
            by="Risk Score",
            ascending=False
        )

    return risk_df


def generate_risk_prompt(risk_df):

    top = risk_df.head(5).to_dict(orient="records")

    return f"""
You are a senior bot mitigation architect.

Analyze these risky endpoints:

{top}

Explain:

1. Which endpoint is most dangerous
2. Why attackers target it
3. Business impact
4. Recommended mitigations
5. Which issue should be prioritized first

Keep response concise and executive friendly.
"""


def render(df, intel):

    st.title("Risk Intelligence")

    if df is None or df.empty:
        st.warning("Upload logs to begin risk analysis.")
        return

    risk_df = calculate_endpoint_risk(df)

    if risk_df.empty:
        st.warning("No endpoint data available.")
        return

    st.subheader("Dynamic Risk Engine")

    st.dataframe(
        risk_df,
        use_container_width=True
    )

    fig = px.bar(
        risk_df.head(10),
        x="Endpoint",
        y="Risk Score",
        color="Severity",
        title="Endpoint Risk Scores"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Threat Heatmap")

    heat = px.density_heatmap(
        risk_df,
        x="Severity",
        y="Endpoint",
        z="Risk Score",
        text_auto=True
    )

    st.plotly_chart(
        heat,
        use_container_width=True
    )

    st.subheader("Risk Analysis")

    with st.spinner("Analyzing attack patterns with Gemma3..."):

        prompt = generate_risk_prompt(risk_df)

        analysis = ask_llm(prompt)

    st.info(analysis)