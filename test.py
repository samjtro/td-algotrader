from indicators import History,Indicator

# create a dataframe (df) with PriceHistory of AAPL for the past 5 days, @ 15M intervals & set indicators
df = Indicator.set(History.get('AAPL','day','5','minute','15'))

print(df)