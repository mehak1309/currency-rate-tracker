import os
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from src.utils.playSound import play_sound
from src.utils.functions import currency_exchange_rate
from time import sleep

# Page configuration
st.set_page_config(
    page_title="Currency Exchange Monitor",
    layout="wide"
)

header1 = st.container()
header2 = st.container()
user = st.container()

# Data
user_data = pd.read_csv(os.path.join("src", "data", "user_settings.csv"))
sleep(5)
base_currency = user_data.Base_Currency.unique()[0]

with open(os.path.join("src", ".key", "api_key.txt"), 'r') as f:
    api_key = f.readline()

# Populating alert info
alert_info = {}

for idx, row in user_data.iterrows():
    try:
        current_value = currency_exchange_rate(
            base_currency, row.Foreign_Currency, api_key)

        if row.Option == ">" and current_value > row.Threshold:
            alert_info[row.Foreign_Currency] = [">", row.Threshold]

        if row.Option == "<" and current_value < row.Threshold:
            alert_info[row.Foreign_Currency] = ["<", row.Threshold]
    except:
        pass

with header1:
    st.title("Currency Exchange Rate Monitor")

with header2:
    st.text(f"Base Currency: {base_currency}")

# Monitor
with user:

    # Creating graphs
    graph_options = ["Exchange_Rate", "Threshold"]
    currency_options = user_data["Foreign_Currency"].tolist()

    graph_option = st.selectbox("Select Graph", options=graph_options, index=0)
    currency = st.multiselect(
        "Choose Currency", options=currency_options, default=currency_options)

    graph_data = user_data[user_data["Foreign_Currency"].isin(currency)]

    first_column, second_column = st.columns(2)
    fig = px.bar(graph_data, x="Foreign_Currency",
                 y=graph_option, color="Foreign_Currency")
    fig.update_layout(width=450)
    first_column.write(fig)

    # Generating alerts based on conditions
    if alert_info:
        second_column.markdown("<br>" * 3, unsafe_allow_html=True)
        for foreign_currency in alert_info.keys():
            second_column.write("\n")

            if alert_info[foreign_currency][0] == ">":
                second_column.info(
                    f"Alert: {foreign_currency} exchange rate reached the value {user_data[user_data['Foreign_Currency'] == foreign_currency]['Threshold'].values[0]}")

            elif alert_info[foreign_currency][0] == "<":
                second_column.info(
                    f"Alert: {foreign_currency} exchange rate has fallen below the value {user_data[user_data['Foreign_Currency'] == foreign_currency]['Threshold'].values[0]}")

            play_sound()
