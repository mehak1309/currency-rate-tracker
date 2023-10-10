import os
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from src.utils.playSound import play_sound

st.set_page_config(
    page_title="Currency Exchange Monitor",
    layout="wide"
)

header1 = st.container()
header2 = st.container()
user = st.container()

#data
user_data = pd.read_csv(os.path.join("src", "data", "user_settings.csv"))
alert_info = ["USD", "JPY", "CHF"]
base_currency = user_data.Base_Currency.unique()[0]

with header1:
    st.title("Currency Exchange Rate Monitor")

with header2:
    st.text(f"Base Currency: {base_currency}")

with user:
    graph_options = ["Exchange_Rate", "Threshold"]
    currency_options = user_data["Foreign_Currency"].tolist()

    graph_option = st.selectbox("Select Graph", options=graph_options, index=0)
    currency = st.multiselect("Choose Currency", options=currency_options, default=currency_options)

    graph_data = user_data[user_data["Foreign_Currency"].isin(currency)]

    first_column, second_column = st.columns(2)
    fig = px.bar(graph_data, x="Foreign_Currency", y=graph_option, color="Foreign_Currency")
    fig.update_layout(width=450)
    first_column.write(fig)


    if alert_info:
        second_column.markdown("<br>" * 3, unsafe_allow_html=True)
        for foreign_currency in alert_info:
            play_sound()
            second_column.write("\n")
            st.write(user_data[user_data['Foreign_Currency'] == foreign_currency]) 
            second_column.info(f"Alert: {foreign_currency} exchange rate reached the value {user_data[user_data['Foreign_Currency'] == foreign_currency]['Threshold']}.")

