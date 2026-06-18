import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def donut(labels, values, title):
    fig = px.pie(
        names=labels,
        values=values,
        hole=0.65,
        title=title
    )
    fig.update_layout(template="plotly_dark")
    return fig

def gauge(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={"axis":{"range":[0,100]}}
    ))
    fig.update_layout(template="plotly_dark")
    return fig

import plotly.express as px

def geo_map(df):
    fig = px.scatter_geo(
        df,
        locations="geo_location",
        locationmode="country names",
        size="requests",
        hover_name="geo_location",
        projection="natural earth"
    )
    fig.update_layout(template="plotly_dark")
    return fig