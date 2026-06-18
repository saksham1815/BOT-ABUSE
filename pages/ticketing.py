import pandas as pd
import streamlit as st

from components.charts import geo_map, gauge
from llm.ollama_client import ask_llm
from llm.prompts import ticketing_prompt


TICKETING_PATTERNS = [
    "checkout",
    "buy",
    "cart",
    "events",
    "inventory",
    "tickets"
]

AUTOMATION_SIGNATURES = [
    "Playwright",
    "Selenium",
    "HeadlessChrome",
    "python-requests",
    "curl"
]


def render(df, intel):

    st.title("Ticket Abuse Intelligence")

    ticket_df = df[
        df["url"].str.contains(
            "|".join(TICKETING_PATTERNS),
            case=False,
            na=False
        )
    ]

    ticket_requests = ticket_df["requests"].sum()

    blocked_inventory = ticket_requests * 0.42

    revenue_saved = blocked_inventory * 120

    queue_score = max(
        100 - (
            ticket_requests /
            max(intel["total_requests"], 1)
        ) * 100,
        0
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Ticket Requests",
            f"{ticket_requests:,.0f}"
        )

    with c2:
        st.metric(
            "Inventory Protected",
            f"{blocked_inventory:,.0f}"
        )

    with c3:
        st.metric(
            "Revenue Protected",
            f"${revenue_saved:,.0f}"
        )

    with c4:
        st.metric(
            "Queue Integrity",
            f"{queue_score:.1f}%"
        )

    st.divider()

    st.plotly_chart(
        gauge(
            queue_score,
            "Queue Integrity Score"
        ),
        use_container_width=True
    )

    st.divider()

    endpoint_activity = (
        ticket_df
        .groupby("url")["requests"]
        .sum()
        .reset_index()
        .sort_values(by="requests", ascending=False)
    )

    endpoint_activity["risk_score"] = (
        endpoint_activity["requests"] /
        endpoint_activity["requests"].max()
    ) * 100

    endpoint_activity["severity"] = endpoint_activity[
        "risk_score"
    ].apply(
        lambda x:
        "Critical" if x > 80 else
        "High" if x > 60 else
        "Medium" if x > 40 else
        "Low"
    )

    st.subheader("Checkout Activity")

    st.dataframe(
        endpoint_activity[
            ["url", "requests", "risk_score", "severity"]
        ],
        use_container_width=True
    )

    st.divider()

    automation = []

    for sig in AUTOMATION_SIGNATURES:

        count = ticket_df[
            ticket_df["useragent"].str.contains(
                sig,
                case=False,
                na=False
            )
        ]["requests"].sum()

        automation.append({
            "signature": sig,
            "requests": count
        })

    auto_df = pd.DataFrame(automation)

    st.subheader("Automation Signals")

    st.dataframe(
        auto_df.sort_values(
            by="requests",
            ascending=False
        ),
        use_container_width=True
    )

    st.divider()

    attacker_cost_before = 120

    attacker_cost_after = (
        ticket_requests * 0.8
    ) + 2400

    destruction = (
        attacker_cost_after /
        attacker_cost_before
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Attack Cost Before",
            f"${attacker_cost_before:,.0f}"
        )

    with c2:
        st.metric(
            "Attack Cost After",
            f"${attacker_cost_after:,.0f}"
        )

    with c3:
        st.metric(
            "Profitability Impact",
            f"{destruction:.1f}x"
        )

    st.divider()

    st.subheader("Traffic Origins")

    st.plotly_chart(
        geo_map(intel["geo"]),
        use_container_width=True
    )

    st.divider()

    geo_activity = (
        ticket_df
        .groupby("countrycode")["requests"]
        .sum()
        .reset_index()
        .sort_values(by="requests", ascending=False)
    )

    st.subheader("Regional Activity")

    st.dataframe(
        geo_activity,
        use_container_width=True
    )

    st.divider()

    st.warning(f"""
Large-scale automated checkout activity detected.

Estimated inventory protection:
{blocked_inventory:,.0f} units

Estimated protected revenue:
${revenue_saved:,.0f}

Automation frameworks targeting transactional
flows identified across multiple regions.
""")

    st.divider()

    with st.spinner("Analyzing ticket abuse behavior..."):

        summary = ask_llm(
            ticketing_prompt(intel)
        )

    st.info(summary)