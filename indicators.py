from hook import RealTime,PriceHistory
import pandas as pd
import numpy as np
from datetime import datetime as dt
from time import sleep

def to_integer(dt_time):
    	return 10000*dt_time.hour + 100*dt_time.minute + dt_time.second

n = 4

def rma(x, n, y0):
	a = (n-1) / n
	ak = a**np.arange(len(x)-1, -1, -1)

	return np.r_[np.full(n, np.nan), y0, np.cumsum(ak * x) / ak / n + y0 * a**np.arange(1, len(x)+1)]

class Quote:
	def __init__(self):
		...

	def get(ticker):
		values = []
		times = []
		for i in range(60):
			quote = RealTime.get(ticker)
			values.append(quote[ticker][8])
			print(quote)
			times.append(to_integer(dt.now()))
			sleep(1)

		df = pd.DataFrame(columns={ 'Time','Value' })
		df['Time'] = times
		df['Value'] = values

		return df

class History:
	def __init__(self):
		...

	def get(ticker,pT,p,fT,f):
		df2 = PriceHistory.get(ticker,pT,p,fT,f)
		rt = RealTime.get(ticker)
		opens = []
		highs = []
		lows = []
		closes = []
		volumes = []
		times = []

		for i in range(len(df2)):
			row = df2.iloc[i]
			opens.append(row['candles']['open'])
			highs.append(row['candles']['high'])
			lows.append(row['candles']['low'])
			closes.append(row['candles']['close'])
			volumes.append(row['candles']['volume'])
			times.append(row['candles']['datetime'])

		df = pd.DataFrame(columns={ 'Time','Open','High','Low','Close','Volume' })
		df['Time'] = times
		df['Open'] = opens
		df['High'] = highs
		df['Low'] = lows
		df['Close'] = closes
		df['Volume'] = volumes

		return df

class Indicator:
	def __init__(self):
		...

	def set(df):
		change = df['Close'].diff()
		gain = change.mask(change < 0, 0.0)
		loss = -change.mask(change > 0, -0.0)
		avg_gain = rma(gain[n + 1:].to_numpy(), n, np.nansum(gain.to_numpy()[:n + 1]) / n)
		avg_loss = rma(loss[n + 1:].to_numpy(), n, np.nansum(loss.to_numpy()[:n + 1]) / n)
		rs = avg_gain / avg_loss
		
		#fiftytwoweekhigh = RealTime(ticker).get[0]
		#fiftytwoweeklow = RealTime(ticker).get[2]
		#HL2 = (fiftytwoweekhigh + fiftytwoweeklow) / 2
		
		ema_short = df['Close'].ewm(span=4, adjust=False).mean()
		ema_long = df['Close'].ewm(span=12, adjust=False).mean()
		ema = (ema_short + ema_long) / 2

		HL = df['High'] - df['Low']
		money_flow_multi = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / HL
		money_flow_vol = money_flow_multi * df['Volume']
		accum_dist_line = money_flow_vol.shift(1) + money_flow_vol

		df['RSI'] = 100 - (100 / (1 + rs))
		df['VWAP'] = (df['Volume'] * (df['High'] + df['Low']) / 2).cumsum() / df['Volume'].cumsum()
		df['MACD'] = (df['Close'] - ema)* .1538 + ema
		df['Chaikin'] = accum_dist_line.ewm(span=3, adjust=False).mean() - accum_dist_line.ewm(span=10, adjust=False).mean()

		return df
