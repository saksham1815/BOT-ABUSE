import streamlit as st
from llm.ollama_client import ask_llm

def scenario_prompt(
    growth,
    mitigation,
    vendor_cost,
    projected_requests,
    fraud_loss,
    savings
):
    return f"""
You are a senior bot mitigation strategist advising a Fortune 500 CISO.

Scenario Inputs:
- Attack Growth Multiplier: {growth}x
- Mitigation Improvement: {mitigation}%
- Vendor Cost: ${vendor_cost}
- Projected Requests: {projected_requests}
- Estimated Fraud Loss: ${fraud_loss}
- Estimated Savings: ${savings}

Provide:

1. Executive summary
2. Primary business risks
3. Financial exposure
4. Recommended controls
5. Priority actions for next 90 days
6. Whether current defenses are sufficient
7. Board-level takeaway

Keep concise and strategic.
"""

def render(df, intel):

    st.title("Scenario Lab")

    st.markdown("""
Simulate future attack conditions, mitigation strategies,
and financial outcomes using AI-driven security modeling.
""")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        growth = st.slider(
            "Attack Growth Multiplier",
            1,
            10,
            2
        )

        mitigation = st.slider(
            "Mitigation Effectiveness %",
            0,
            100,
            65
        )

    with col2:
        vendor_cost = st.slider(
            "Annual Vendor Cost ($)",
            10000,
            500000,
            120000,
            step=10000
        )

        conversion_loss = st.slider(
            "Conversion Impact %",
            1,
            50,
            12
        )

    st.divider()

    base_requests = intel["total_requests"]

    projected_requests = base_requests * growth

    fraud_loss = projected_requests * 0.08

    prevented_loss = fraud_loss * (mitigation / 100)

    savings = prevented_loss - vendor_cost

    roi = (
        (savings / vendor_cost) * 100
        if vendor_cost > 0 else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Projected Requests",
            f"{projected_requests:,.0f}"
        )

    with c2:
        st.metric(
            "Estimated Fraud Loss",
            f"${fraud_loss:,.0f}"
        )

    with c3:
        st.metric(
            "Prevented Loss",
            f"${prevented_loss:,.0f}"
        )

    with c4:
        st.metric(
            "ROI",
            f"{roi:.1f}%"
        )

    st.divider()

    st.subheader("Strategic Assessment")

    with st.spinner("Running scenario intelligence engine..."):

        prompt = scenario_prompt(
            growth,
            mitigation,
            vendor_cost,
            projected_requests,
            fraud_loss,
            savings
        )

        summary = ask_llm(prompt)

    st.info(summary)

    st.divider()

    st.subheader("Strategic Insights")

    if roi > 150:
        st.success(
            "Mitigation investment is highly favorable."
        )

    elif roi > 50:
        st.warning(
            "Moderate ROI — defenses should be optimized."
        )

    else:
        st.error(
            "Current mitigation strategy may not justify spend."
        )

    if growth >= 5:
        st.error(
            "High attack growth detected — executive escalation recommended."
        )

    if mitigation < 40:
        st.warning(
            "Defense effectiveness is critically low."
        )

    if conversion_loss > 20:
        st.warning(
            "Customer experience degradation risk elevated."
        )