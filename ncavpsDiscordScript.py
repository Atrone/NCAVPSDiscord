import discord
from discord.ext import tasks
import requests
import pandas as pd

client = discord.Client()

def goodNCAVPSStocksNASDAQ():
    NetCurrentAssetValueperShare = {}

    querytickers = requests.get(
        f'https://financialmodelingprep.com/api/v3/search?query=&exchange=NASDAQ&apikey=6bec761839671e40cb1be089b7d3a0e5')
    querytickers = querytickers.json()
    list_500 = querytickers
    stocks = []
    for item in list_500:
        # Stop after storing 100 stocks
        stocks.append(item['symbol'])
    for company in stocks:
        Balance_Sheet = requests.get(
            f'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{company}?period=quarter&apikey=6bec761839671e40cb1be089b7d3a0e5')
        Balance_Sheet = Balance_Sheet.json()
        try:
            total_current_assets = float(Balance_Sheet['financials'][0]['Total current assets'])
            total_liabilities = float(Balance_Sheet['financials'][0]['Total liabilities'])
            sharesnumber = requests.get(
                f'https://financialmodelingprep.com/api/v3/enterprise-value/{company}?apikey=6bec761839671e40cb1be089b7d3a0e5')
            sharesnumber = sharesnumber.json()
            price = float(sharesnumber['enterpriseValues'][0]['Stock Price'])
            sharesnumber = float(sharesnumber['enterpriseValues'][0]['Number of Shares'])

            NCAVPS = (total_current_assets - total_liabilities) / sharesnumber
            # only companies where NCAVPS is below the stock price
            if (0.67 * NCAVPS) > (price):
                NetCurrentAssetValueperShare[company] = NCAVPS
        except:
            pass
    return NetCurrentAssetValueperShare


@tasks.loop(hours=1)
async def loop():
    channel = client.get_channel(684550807068082226)
    await channel.send(str(goodNCAVPSStocksNASDAQ()))

@client.event
async def on_ready():
    loop.start()

client.run('NzU5NjYxNDY4OTk1NDIwMTYx.X3Av4A.hcvHQndrcDxL-g8U2MyadzLJc_w')
