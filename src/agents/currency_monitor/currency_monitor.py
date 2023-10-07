#import libraries
import requests, json

def currency_exchange_rate(from_currency, to_currency, api_key):    
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=Z1WC0QSKNTR4JP1G'
    r = requests.get(url)
    data = r.json()
    return data

