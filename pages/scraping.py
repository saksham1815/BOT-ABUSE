import pandas as pd
import streamlit as st

from components.charts import geo_map
from llm.ollama_client import ask_llm
from llm.prompts import scraping_prompt


SCRAPING_PATTERNS = [
    "pricing",
    "catalog",
    "search",
    "api",
    "products",
    "inventory"
]

BOT_SIGNATURES = [
    "HeadlessChrome",
    "Playwright",
    "Selenium",
    "Scrapy",
    "python-requests",
    "curl",
    "Go-http-client"
]


def render(df, intel):

    st.title("Scraping Intelligence")

    scraping_df = df[
        df["url"].str.contains(
            "|".join(SCRAPING_PATTERNS),
            case=False,
            na=False
        )
    ]

    scraper_requests = scraping_df["requests"].sum()

    revenue_leak = scraper_requests * 0.18

    infra_cost = scraper_requests * 0.04

    protected_value = revenue_leak + infra_cost

    api_abuse_score = min(
        round((scraper_requests / max(intel["total_requests"], 1)) * 100, 1),
        100
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Scraper Requests",
            f"{scraper_requests:,.0f}"
        )

    with c2:
        st.metric(
            "Revenue Exposure",
            f"${revenue_leak:,.0f}"
        )

    with c3:
        st.metric(
            "Protected Value",
            f"${protected_value:,.0f}"
        )

    with c4:
        st.metric(
            "API Abuse Score",
            f"{api_abuse_score}%"
        )

    st.divider()

    endpoint_risk = (
        scraping_df
        .groupby("url")["requests"]
        .sum()
        .reset_index()
        .sort_values(by="requests", ascending=False)
    )

    endpoint_risk["risk_score"] = (
        endpoint_risk["requests"] /
        endpoint_risk["requests"].max()
    ) * 100

    endpoint_risk["severity"] = endpoint_risk[
        "risk_score"
    ].apply(
        lambda x:
        "Critical" if x > 80 else
        "High" if x > 60 else
        "Medium" if x > 40 else
        "Low"
    )

    st.subheader("Endpoint Activity")

    st.dataframe(
        endpoint_risk[
            ["url", "requests", "risk_score", "severity"]
        ],
        use_container_width=True
    )

    st.divider()

    fingerprints = []

    for sig in BOT_SIGNATURES:

        count = scraping_df[
            scraping_df["useragent"].str.contains(
                sig,
                case=False,
                na=False
            )
        ]["requests"].sum()

        fingerprints.append({
            "signature": sig,
            "requests": count
        })

    fp_df = pd.DataFrame(fingerprints)

    st.subheader("Automation Fingerprints")

    st.dataframe(
        fp_df.sort_values(
            by="requests",
            ascending=False
        ),
        use_container_width=True
    )

    st.divider()

    st.subheader("Traffic Origins")

    st.plotly_chart(
        geo_map(intel["geo"]),
        use_container_width=True
    )

    st.divider()

    suspicious_geo = (
        scraping_df
        .groupby("countrycode")["requests"]
        .sum()
        .reset_index()
        .sort_values(by="requests", ascending=False)
    )

    st.subheader("Regional Concentration")

    st.dataframe(
        suspicious_geo,
        use_container_width=True
    )

    st.divider()

    st.subheader("Operational Impact")

    st.warning(f"""
Estimated pricing intelligence exposure:
${revenue_leak:,.0f}

Estimated infrastructure amplification:
${infra_cost:,.0f}

High-frequency automation targeting catalog and
inventory endpoints detected.
""")

    st.divider()

    with st.spinner("Analyzing scraping behavior..."):

        summary = ask_llm(
            scraping_prompt(intel)
        )
    st.subheader("Important Points")
    st.info(summary)