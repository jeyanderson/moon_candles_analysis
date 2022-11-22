import ccxt
import pandas as pd
import time
from datetime import datetime
from math import floor
bybit=ccxt.bybit({
            "apiKey":'apiKey',
            "secret":'apiSecret',
            "options": {'defaultType': 'future' }
        })
symbol='ETHUSDT'
tf='1m'
df=bybit.fetch_ohlcv(symbol,tf,limit=30)
df=pd.DataFrame(df)
df.columns=['timestamp','open','high','low','close','volume']
df['timestamp']=[datetime.fromtimestamp((x/1000)) for x in df['timestamp']]
df=df.set_index('timestamp')
df['candlesize']=df['high']-df['low']
df['avgSize']=df['candlesize'].rolling(30).mean()
df['stdSize']=df['candlesize'].rolling(30).std()
sigma=4.5
side=1 if df.iloc[-1]['close'] > df.iloc[-2]['close'] else 0
range=df.iloc[-1]['high']-df.iloc[-1]['low']
if range>=(df.iloc[-1]['avgSize']+df.iloc[-1]['stdSize']*sigma):
    balance=bybit.fetch_balance()
    balance=float(balance['USDT']['free'])
    portion=floor(balance/2)
    price=bybit.fetch_ticker(symbol)
    price=float(price['ask'])
    size=float(bybit.amount_to_precision(symbol,portion/price))
    # if side:
    #     bybit.create_market_sell_order(symbol,size)
    # else:
    #     bybit.create_market_buy_order(symbol,size)
    # time.sleep(1200)
    # if side:
    #     bybit.create_market_buy_order(symbol,size,params={'reduce_only':True})
    # else:
    #     bybit.create_market_sell_order(symbol,size,params={'reduce_only':True})
