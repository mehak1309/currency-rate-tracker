# Import necessary libraries
import requests
from uagents import Agent, Context

# User input values
BASE_CURRENCY = "USD"
THRESHOLDS = {
    "JPY": {"High": 120.0, "Low": 130.0},
    "INR": {"Low": 100.0}
}

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

agent = Agent(name="currency_monitor", seed="alice recovery phrase")

@agent.on_interval(period=252)
async def currency_monitor(ctx: Context):

    for FOREIGN_CURRENCY in THRESHOLDS.keys():

        for ALERT_PARAM in THRESHOLDS[FOREIGN_CURRENCY].keys():

            if ALERT_PARAM == "High":

                if currency_exchange_rate(BASE_CURRENCY, FOREIGN_CURRENCY, API_KEY) > THRESHOLDS[FOREIGN_CURRENCY][ALERT_PARAM]: #API_KEY not available
                    ctx.logger.info(f'{FOREIGN_CURRENCY} has exceeded the threshold {THRESHOLDS[FOREIGN_CURRENCY][ALERT_PARAM]}')

            elif ALERT_PARAM == "Low":

                if currency_exchange_rate(BASE_CURRENCY, FOREIGN_CURRENCY, API_KEY) < THRESHOLDS[FOREIGN_CURRENCY][ALERT_PARAM]: #API_KEY not available
                    ctx.logger.info(f'{FOREIGN_CURRENCY} has fallen below the threshold {THRESHOLDS[FOREIGN_CURRENCY][ALERT_PARAM]}')

if __name__ == "__main__":
    agent.run()
