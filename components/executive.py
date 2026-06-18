import streamlit as st
from components.charts import geo_map

from llm.ollama_client import ask_llm

summary = ask_llm(prompt)
st.info(summary)

def render(df, intel):
    st.title("Executive Overview")

    c1,c2,c3 = st.columns(3)

    c1.metric("Total Requests", f"{intel['total_requests']:,.0f}")
    c2.metric("ATO Requests", f"{intel['login_requests']:,.0f}")
    c3.metric("Scraping Requests", f"{intel['scraping_requests']:,.0f}")

    if intel["alerts"]:
        for a in intel["alerts"]:
            st.error(f"{a['severity']} - {a['message']}")

    st.subheader("Threat Origin Map")
    st.plotly_chart(geo_map(intel["geo"]), use_container_width=True)