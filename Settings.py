import os
import streamlit as st
import requests
import pandas as pd
import random, string
from src.utils.functions import currency_exchange_rate

# Page configuration
st.set_page_config(
    page_title="Currency Exchange Monitor",
    layout="wide"
)

header = st.container()
user_data = st.container()

@st.cache_data
def get_data(filename):
    """
    Reads data from a CSV file and returns it.
    Parameters:
        filename (str): The path to the CSV file to be read.
    Returns:
        pd.DataFrame: A Pandas DataFrame containing the data from the CSV file.
    """
    data = pd.read_csv(filename)
    return data

input_rows = []

data = get_data(os.path.join("src", "data", "currency_codes.csv"))
currency_codes = data['Codes'].tolist()

with header:
    st.title("Please Enter the Following Details")

# Taking input from the user
with user_data:
    api_key = st.text_input("API Key")
    base_currency = st.selectbox("Base Currency", options=currency_codes, index=0)
    st.text("Get Notified When:")
    first_column, second_column, third_column = st.columns(3)
    first_column.write("Foreign Currency")
    third_column.write("Threshold")

    for i in range(3):
        first_column, second_column, third_column = st.columns(3)
        foreign_currency = first_column.selectbox(f"Foreign Currency {i}",
                                                options=currency_codes,
                                                index=1,
                                                label_visibility="hidden")
        mode = second_column.selectbox(f"Option {i}",
                                    options=[">", "<"],
                                    index=0,
                                    label_visibility="hidden")
        threshold = third_column.text_input(f"Threshold {i}",
                                            label_visibility="hidden")

        input_rows.append({"foreign_currency": foreign_currency, "mode": mode, "threshold": threshold})

    st.write("")

    col1, col2, col3, col4, col5 = st.columns(5)
    if col3.button("Submit"):
        with open(os.path.join("src", ".key", "api_key.txt"), 'w') as f:
            f.write(api_key)

        d = {"Base_Currency": [],
                "Foreign_Currency": [],
                "Option": [],
                "Threshold": [],
                "Exchange_Rate": []}

        # Updating user_settings.csv
        for row in input_rows:

            d["Base_Currency"].append(base_currency)
            d["Foreign_Currency"].append(row["foreign_currency"])
            d["Option"].append(row["mode"])
            d["Threshold"].append(row["threshold"])
            with open(os.path.join("src",".key","api_key.txt"), 'r') as f:
                api_key = f.readline()
            d["Exchange_Rate"].append(currency_exchange_rate(base_currency, row["foreign_currency"], api_key))
        
        df = pd.DataFrame.from_dict(d)
        df.to_csv(os.path.join("src", "data", "user_settings.csv"), index=False)


