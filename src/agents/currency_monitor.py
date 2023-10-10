# Import necessary libraries
import os
import requests
from uagents import Agent, Context
import pandas as pd

# User input values
BASE_CURRENCY = "USD"
THRESHOLDS = {
    "JPY": {"High": 120.0, "Low": 130.0},
    "INR": {"Low": 100.0}
}

with open(os.path.join("src",".key","api_key.txt"), 'r') as f:
    API_KEY = f.readline()

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

    for FOREIGN_CURRENCY in THRESHOLDS.keys():

        for ALERT_PARAM in THRESHOLDS[FOREIGN_CURRENCY].keys():

            CURRENT_VALUE = currency_exchange_rate(BASE_CURRENCY, FOREIGN_CURRENCY, API_KEY)
            df = pd.read_csv(os.path.join("src","data","user_settings.csv"), header=0)
            df.loc[df['Foreign_Currency'] == FOREIGN_CURRENCY, 'Exchange_Rate'] = CURRENT_VALUE
            df.to_csv(os.path.join("src","data","user_settings.csv"), index=False)

            if ALERT_PARAM == "High":

                if CURRENT_VALUE > THRESHOLDS[FOREIGN_CURRENCY][ALERT_PARAM]:
                    ctx.logger.info(f'{FOREIGN_CURRENCY} has exceeded the threshold {THRESHOLDS[FOREIGN_CURRENCY][ALERT_PARAM]}')

            elif ALERT_PARAM == "Low":

                if CURRENT_VALUE < THRESHOLDS[FOREIGN_CURRENCY][ALERT_PARAM]:
                    ctx.logger.info(f'{FOREIGN_CURRENCY} has fallen below the threshold {THRESHOLDS[FOREIGN_CURRENCY][ALERT_PARAM]}')

if __name__ == "__main__":
    agent.run()