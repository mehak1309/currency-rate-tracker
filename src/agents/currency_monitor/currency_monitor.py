#import libraries
import requests, json

def currency_exchange_rate(from_currency, to_currency, api_key, country=True):  
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='+from_currency+'&to_currency='+to_currency+'&apikey='+api_key
    r = requests.get(url)
    data = r.json()
    return data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]

print(currency_exchange_rate("USD", "JPY", "YOUR_API_KEY"))
