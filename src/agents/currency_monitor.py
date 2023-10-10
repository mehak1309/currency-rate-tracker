# Import necessary libraries
import os
import requests
from uagents import Agent, Context
import pandas as pd
from utils.functions import currency_exchange_rate

# Read data
df = pd.read_csv(os.path.join("src","data","user_settings.csv"), header=0)
with open(os.path.join("src",".key","api_key.txt"), 'r') as f:
    API_KEY = f.readline()
    f.close()

# User inputs
base_currency = df.Base_Currency.unique()[0]
thresholds = {}

for idx, row in df.iterrows():
    if row.Foreign_Currency not in thresholds.keys():
        thresholds[row.Foreign_Currency] = {}
    thresholds[row.Foreign_Currency][row.Option] = float(row.Threshold)

#UAgents
agent = Agent(name="currency_monitor", seed="seed goes here")

@agent.on_interval(period=252)
async def currency_monitor(ctx: Context):
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
        
