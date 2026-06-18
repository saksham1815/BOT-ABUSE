import streamlit as st
import requests
from core.config import OLLAMA_URL, OLLAMA_MODEL

def render(df, intel):
    st.title("Copilot")

    q = st.text_area("Ask a question")

    if st.button("Analyze"):
        prompt = f"""
        User Question: {q}

        Requests: {intel['total_requests']}
        Login Requests: {intel['login_requests']}
        Scraping Requests: {intel['scraping_requests']}
        Alerts: {len(intel['alerts'])}
        """

        r = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        st.write(r.json()["response"])