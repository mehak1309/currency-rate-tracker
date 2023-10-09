#import libraries
import requests, json
from uagents import Agent, Context 

#user input values
BASE_CURRENCY = "USD"
THRESHOLDS={"JPY": {120.0, "low"}, "IND":{100, "high"}}
API_KEY = "BYQ8L1U8PWKZ2NKL"


def currency_exchange_rate(from_currency, to_currency, api_key, country=True): 
    """
    This function takes input two country codes: from_currency and to_currency and outputs the exchnage rate in real time.
    """ 
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='+from_currency+'&to_currency='+to_currency+'&apikey='+api_key
    r = requests.get(url)
    data = r.json()
    return float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

print(currency_exchange_rate("USD", "JPY", "BYQ8L1U8PWKZ2NKL"))
alice = Agent(name="alice", seed="alice recovery phrase")
@alice.on_interval(period=20)
async def say_hello(ctx: Context):
    for FOREIGN_CURRENCY in THRESHOLDS.keys():
        if currency_exchange_rate(BASE_CURRENCY, FOREIGN_CURRENCY, API_KEY) > THRESHOLDS[FOREIGN_CURRENCY]:
            ctx.logger.info(f'{FOREIGN_CURRENCY} has exceeded the threshold {THRESHOLDS[FOREIGN_CURRENCY]}')

if __name__ == "__main__":
    alice.run()


