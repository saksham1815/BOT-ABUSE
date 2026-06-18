import streamlit as st

def metric_card(title, value, delta=None):
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric(title, value, delta)
    st.markdown("</div>", unsafe_allow_html=True)