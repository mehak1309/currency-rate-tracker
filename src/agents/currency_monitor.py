# Import necessary libraries
import os
import requests
from uagents import Agent, Context
import pandas as pd

# Read data
df = pd.read_csv(os.path.join("src","data","user_settings.csv"), header=0)
with open(os.path.join("src",".key","api_key.txt"), 'r') as f:
    API_KEY = f.readline()
    f.close()

# User inputs
base_currency = df.Base_Currency.unique()[0]
thresholds = {}

for idx, row in df.iterrows():
    if row.foreign_currency not in thresholds.keys():
        thresholds[row.foreign_currency] = {}
    thresholds[row.foreign_currency][row.Option] = float(row.Threshold)

def currency_exchange_rate(from_currency, to_currency, api_key):
    """
    This function retrieves the real-time exchange rate between two currency codes using the AlphaVantage API.
    Parameters:
    - from_currency (str): The currency code you want to convert from.
    - to_currency (str): The currency code you want to convert to.
    - api_key (str): Your AlphaVantage API key for authentication.
    Returns:
    - float: The real-time exchange rate between the specified currencies.
    """
    # To construct the API request URL
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=' + from_currency + '&to_currency=' + to_currency + '&apikey=' + api_key
    # To send a GET request to the API
    r = requests.get(url)
    # To parse the JSON response
    data = r.json()
    # To extract and return the exchange rate
    return float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

agent = Agent(name="currency_monitor", seed="seed goes here")

@agent.on_interval(period=252)
async def currency_monitor(ctx: Context):
    try:
        for foreign_currency in thresholds.keys():
            for alert_param in thresholds[foreign_currency].keys():
                current_value = currency_exchange_rate(base_currency, foreign_currency, API_KEY)
                df = pd.read_csv(os.path.join("src","data","user_settings.csv"), header=0)
                df.loc[df['foreign_currency'] == foreign_currency, 'Exchange_Rate'] = current_value
                df.to_csv(os.path.join("src","data","user_settings.csv"), index=False)

                if alert_param == ">":
                    if current_value > thresholds[foreign_currency][alert_param]:
                        ctx.logger.info(f'{foreign_currency} has exceeded the threshold {thresholds[foreign_currency][alert_param]}')
                
                elif alert_param == "<":
                    if current_value < thresholds[foreign_currency][alert_param]:
                        ctx.logger.info(f'{foreign_currency} has fallen below the threshold {thresholds[foreign_currency][alert_param]}')
    except Exception as e:
        print(f"Error: {e}")
