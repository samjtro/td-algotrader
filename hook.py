import requests
import json
import pandas as pd

# Account
    # .get
# RealTime
    # .get
# PriceHistory
    # .get
# Option
    # .chain
    # .spread
# Instrument
    # .search
    # .get
# Movers
    # .get

apikey = ''

endpoint_realtime = 'https://api.tdameritrade.com/v1/marketdata/quotes'                     # --> symbol
endpoint_pricehistory = 'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'        # --> symbol
endpoint_option = 'https://api.tdameritrade.com/v1/marketdata/chains'
endpoint_searchinstrument = 'https://api.tdameritrade.com/v1/instruments'
endpoint_getinstrument = 'https://api.tdameritrade.com/v1/instruments/{}'                   # --> cusip
endpoint_movers = 'https://api.tdameritrade.com/v1/marketdata/{}/movers'                    # --> index
endpoint_account = 'https://api.tdameritrade.com/v1/accounts/{}'                            # --> accountID

class Account:
    def __init__(self):
        ...

    def get(accountID, fields=''):
#fields default is balances; can also be positions, orders
        url = endpoint_account
        getr = requests.get(url=url.format(accountID), params={
            'apikey': apikey,
            'fields': fields
        })
        page = json.loads(getr.content)
    
        return page

class RealTime:
    def __init__(self):
        ...

    def get(ticker):
        url = endpoint_realtime
        getr = requests.get(url=url, params={
            'apikey': apikey,
            'symbol': ticker
        })
        page = json.loads(getr.content)
        quote = pd.DataFrame(page)

        return quote

class PriceHistory():
    def __init__(self):
        ...

    def get(ticker, pT, p, fT, f, ext='true'):
        '''
pT = Period Type (day, month, year, or ytd)
p = Period (int)
fT = Frequency Type; depends on the period (p:fT; day:minute, month:daily/weekly, year:daily/weekly/monthly, ytd:daily/weekly)
f = Frequency (int; minute:1/5/10/15/30, daily:1, weekly:1, monthly:1)
        '''
        url = endpoint_pricehistory.format(ticker)
        getr = requests.get(url=url, params={
            'apikey': apikey,
            'periodType': pT,
            'period': p,
            'frequencyType': fT,
            'frequency': f,
            'needExtendedHoursData': ext
        })
        page = json.loads(getr.content)
        quote = pd.DataFrame(page)

        return quote

class Option:
    def __init__(self):
        ...

    def chain(ticker, cT, sC, s, fD, tD, expM='ALL', oT='ALL', iQ='TRUE', r='ITM, NTM, SAK, SBK, SNK'):
        '''
Let's break down all of these params:
  cT = Contract Type (CALL, PUT, or ALL); type of contracts to return in the chain
  sC = Strike Count (type=int); # of strikes to return above and below the at-the-money (ATM) price
  s = Strike (type=int); returns options only at that strike price
  fD = From Date (ISO-8601['yyyy-mm-dd' or 'yyyy-MM-dd'T'HH:mm:ssz']); only return options after this date
  tD = To Date (ISO-8601['yyyy-mm-dd' or 'yyyy-MM-dd'T'HH:mm:ssz']); only return options before this date
  expM = Expiration Month (JAN-DEC, ALL); return only options expiring in the specified month                   *DEFAULT=ALL*
  oT = Option Type (S, NS, ALL); types of contracts to return (standard / non-standard)                         *DEFAULT=ALL*
  iQ = Include Quotes (TRUE, FALSE); include quotes for options in the option chain                             *DEFAULT=TRUE*
  r = Range (ITM, NTM, OTM, SAK, SBK, SNK, ALL); returns options for the given range                            *DEFAULT=ITM, NTM, SAK, SBK, SNK*
        '''
        url = endpoint_option
        getr = requests.get(url=url, params={
            'apikey': apikey,
            'symbol': ticker,
            'contractType': cT,
            'strikeCount': sC,
            'includeQuotes': iQ,
            'strike': s,
            'range': r,
            'fromDate': fD,
            'toDate': tD,
            'expMonth': expM,
            'optionType': oT
        })
        page = json.loads(getr.content)
        chain = pd.DataFrame(page)

        return chain

    def spread(ticker, cT, sC, s, fD, tD, strat, i, vol, uP, iR, d2e, expM='ALL', oT='ALL', iQ='TRUE', r='ITM, NTM, SAK, SBK, SNK'):
        '''
[advanced, proceed with caution -- aka, do NOT use these if you don't know what you're doing. i am not responsible for you losing your money on shit spreads.]
For Strategy Spreads:
  *DEFAULT=SINGLE* strat = Strategy (SINGLE, ANALYTICAL, COVERED, VERTICAL, CALENDAR, STRANGLE, STRADDLE, BUTTERFLY, CONDOR, DIAGONAL, COLLAR, or ROLL); Strategy Chain Type
  i = Interval (type=int); strike interval for spread strategy chains
  vol = Volatility (type=float); volatility for the underlying calculation
  uP = Underlying Price (type=float); underlying price for the underlying
  iR = Interest Rate (type=float); interest rate for the underlying
  d2e = Days-to-Expiration (type=int); days-to-expiration for the underlying
        '''
        url = endpoint_option
        getr = requests.get(url=url, params={
            'apikey': app_config['key'],
            'symbol': ticker,
            'contractType': cT,
            'strikeCount': sC,
            'includeQuotes': iQ,
            'strike': s,
            'range': r,
            'fromDate': fD,
            'toDate': tD,
            'expMonth': expM,
            'optionType': oT,
            'strategy': strat,
            'interval': i,
            'volatility': vol,
            'underlyingPrice': uP,
            'interestRate': iR,
            'daysToExpiration': d2e
        })       
        page = json.loads(getr.content)
        spread = pd.DataFrame(page)

        return spread

class Instrument:
    def __init__(self):
        ...
    
    def search(ticker,type):
        '''
Valid Type(s):
  - symbol-search = retrieve instrument data of a specific symbol or cusip
  - symbol-regex = retrieve instrument data for all symbols with matching regex ex. 'xyz.*' returns all symbols starting with 'xyz'
  - desc-search = retrieve instrument data for instruments whose descriptions contains the word supplied
  - desc-regex = search description with full regex support ex. 'xyz.[A-C]' returns all instruments whose desc contains a word beginning with xyz followed by character A-C
  - fundamental = returns fundamental data for a single instrument specified by an exact symbol
        '''
        url = endpoint_searchinstrument
        getr = requests.get(url=url, params={
            'apikey': apikey,
            'symbol': ticker,
            'projection': type
        })
        page = json.loads(getr.content)
        result = pd.DataFrame(page)

        return result

    def get(cusip):
        url = endpoint_getinstrument.format(cusip)
        getr = requests.get(url=url, params={
            'apikey': apikey
        })
        page = json.loads(getr.content)
        result = pd.DataFrame(page)

        return result

class Movers:
    def __init__(self):
        ...

    def get(index, direction, change):
        '''
index = '$COMP' / '$DJI' / '$SPX.X'
direction = 'up' / 'down'
change = 'percent' / 'value'
        '''
        url = endpoint_movers.format(index)
        getr = requests.get(url=url, params={
            'apikey': apikey,
            'direction': direction,
            'change': change
        })
        page = json.loads(getr.content)
        result = pd.DataFrame(page)

        return result
