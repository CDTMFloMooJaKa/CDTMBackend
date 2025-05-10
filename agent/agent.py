import argparse
import backtrader as bt
import yfinance as yf
import pandas as pd
import requests

# --- CLI Argument Parser ---
parser = argparse.ArgumentParser(description="Get trading decision for a stock based on ISIN")
parser.add_argument("isin", help="ISIN code to analyze")
parser.add_argument("--apikey", default="e6a8f0ce-648d-4f3a-8ba7-2f5638bdb65a", help="OpenFIGI API key")
args = parser.parse_args()

isin_code = args.isin
api_key = args.apikey

# --- ISIN to Ticker via OpenFIGI ---
def get_ticker_from_isin(isin, api_key):
    url = 'https://api.openfigi.com/v3/mapping'
    headers = {
        'Content-Type': 'application/json',
        'X-OPENFIGI-APIKEY': api_key
    }
    payload = [{'idType': 'ID_ISIN', 'idValue': isin}]
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    try:
        return response.json()[0]['data'][0]['ticker']
    except (KeyError, IndexError):
        raise Exception("Ticker not found for the provided ISIN")

try:
    ticker = get_ticker_from_isin(isin_code, api_key)
    print(f"✔ ISIN {isin_code} → Ticker {ticker}")
except Exception as e:
    print(f"❌ {str(e)}")
    exit(1)

# --- Download Data ---
df = yf.download(ticker, start='2020-01-01', end='2023-01-01')
df.columns = df.columns.get_level_values(0)
df.index = pd.to_datetime(df.index)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

# --- Backtrader Data Feed ---
data = bt.feeds.PandasData(
    dataname=df,
    datetime=None,
    open='Open',
    high='High',
    low='Low',
    close='Close',
    volume='Volume',
    openinterest=-1
)

# --- Strategy Definition ---
class FinalDayDecision(bt.Strategy):
    def __init__(self):
        self.sma1 = bt.ind.SMA(self.data.close, period=50)
        self.sma2 = bt.ind.SMA(self.data.close, period=200)
        self.final_action = None

    def next(self):
        if len(self.data) == len(self.data._dataname):
            if self.sma1[0] > self.sma2[0] and self.sma1[-1] <= self.sma2[-1]:
                self.final_action = 'BUY'
            elif self.sma1[0] < self.sma2[0] and self.sma1[-1] >= self.sma2[-1]:
                self.final_action = 'SELL'
            else:
                self.final_action = 'HOLD'

# --- Run ---
cerebro = bt.Cerebro()
strategy = cerebro.addstrategy(FinalDayDecision)
cerebro.adddata(data)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.01)
results = cerebro.run()

final_decision = results[0].final_action
print(f"\n📈 Final trading decision for {ticker}: {final_decision}")

