from src.dune import return_dataframe
from src.ga_api import run_request

import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache
def load_data(time_group_by):
    dune_df = return_dataframe()
    ga_df = run_request()
    df = pd.merge(dune_df, ga_df, left_on="block_time", right_on="date", how="left")
    dff = df.groupby(pd.Grouper(freq=time_group_by, key="block_time")).sum().reset_index()
    dff["conversion"] = dff["count"] / dff["activeUsers"]
    return dff


time_group_by = st.sidebar.selectbox("Select a time:", ["D", "W", "M"])

df = load_data(time_group_by)

st.header("Multi Source Dashboard Example")

fig = px.bar(
    df,
    x="block_time",
    y="activeUsers",
    title="Daily CoWSwap.exchange visitors (GA)",
    labels={"block_time": "Date", "activeUsers": "Visitors (#)",},
)
st.plotly_chart(fig)

fig = px.bar(
    df,
    x="block_time",
    y="count",
    title="Daily trades (Dune)",
    labels={"block_time": "Date", "count": "Trades (#)",},
)
st.plotly_chart(fig)

fig = px.bar(
    df,
    x="block_time",
    y="conversion",
    title="Daily conversion rate (GA+Dune)",
    labels={"block_time": "Date", "conversion": "Conversion (%)",},
)
fig.update_layout(yaxis_range=[0, 1])
st.plotly_chart(fig)
