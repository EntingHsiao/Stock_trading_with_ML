
import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
from util import get_data, plot_data

# prepare the data
def normalize_stocks(prices):
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)
    return prices / prices.iloc[0]


#The function to return SMA
# price < sma, BUY
# price > sma, SELL


"""Calculate simple moving average indicator
Parameters:
price: Normalized adjusted close price
rolling_mean: Rolling mean of certain numbers of days
Returns: SMA
"""

def compute_sma(normalized_price, rolling_days):
    columns = ['SMA']
    sma = pd.DataFrame(0, index = normalized_price.index, columns = columns)
    sma['SMA'] = normalized_price.rolling(window=rolling_days, min_periods = rolling_days).mean()
    return sma

# the function to return momentum
# negative --> postive, Buy
# postive --> negative, Sell

"""Calculate momentum indicator: 
momentum[t] = (price[t]/price[t-rolling_days]) - 1

Parameters:
price: Normalized adjusted close price 
rolling_days: Number of days to look back
Returns: Momentum
"""   

def compute_momentum(normalized_price, rolling_days):
    momentum = pd.DataFrame(0, index = normalized_price.index, columns = ['Momentum'])
    momentum['Momentum'] = (normalized_price/normalized_price.shift(rolling_days))-1
    return momentum
 
# the function to return Exponential moving average (EMA) 
# price < ema, BUY
# price > ema, SELL

"""Calculate EMA indicator: 
EMA = Closing price x multiplier + EMA (previous day) x (1-multiplier)

Parameters:
price: Normalized adjusted close price 
rolling_days: Number of days to look back
Returns: EMA
"""   

def compute_ema(normalized_price, rolling_days):
    ema = pd.DataFrame(0, index = normalized_price.index, columns = ['EMA'])
    ema['EMA'] =normalized_price.ewm(span= rolling_days,adjust=False).mean()
    return ema

 # MACD: Moving Average Convergence Divergence
# Signal Line > MACD Line , SELL
# Signal Line < MACD Line, BUY

"""Calculate MACD indicator: 
MACD Line: (12-day EMA - 26-day EMA)
Signal Line: 9-day EMA of MACD Line

Parameters:
price: Normalized adjusted close price 
Returns: MACD line and Signal line
"""

def compute_macd(normalized_price): 
    macd = pd.DataFrame(0, index = normalized_price.index, columns = ['ema_12','ema_26','macd_raw','MACD'])
    macd['ema_12'] = normalized_price.ewm(span=12, adjust=False).mean()
    macd['ema_26'] = normalized_price.ewm(span=26, adjust=False).mean()
    macd['MACD'] = macd['ema_12'] - macd['ema_26']
    macd['Signal'] = macd['MACD'].ewm(span=9, adjust=False).mean()
    macd['MACD_diff'] = macd['Signal'] - macd['MACD']
    return macd['MACD_diff']

# Stochastic Oscillator
# signal line (%D) > indicator line (%K), Overbought, SELL
# signal line (%D) < indicator line (%K), Oversold, BUY 

"""Calculate Stochastic Oscillator indicator: 

Indicator line (%K): (C−L14/H14−L14)*100
C = The most recent closing price
L14 = The lowest price traded of the 14 previous trading sessions
H14 = The highest price traded during the same 14-day period
%K = The current value of the stochastic indicator

Signal line (%D): D=100*(H3/L3)
H3=Highest of the three previous trading sessions
L3=Lowest price traded during the same three-day period
%D = The current value of the stochastic signal

Parameters:
price: Normalized adjusted close price 
Returns: %K and %D 
"""

def compute_kd(normalized_price): 
    KD = pd.DataFrame(0, index = normalized_price.index, columns = ['%K','%D'])
    #compute K%
    L14= normalized_price.rolling(14).min()
    H14= normalized_price.rolling(14).max()
    KD['%K']= ((normalized_price- L14)/ (H14-L14))*100
    KD['%D']= KD['%K'].rolling(3).mean()
    KD['%KD'] = KD['%D'] -KD['%K']
    return KD['%KD']

def compute_indicators(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), \
    syms=['JPM']):

    # Read in date range, prices and symbols
    symbol = syms[0]
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates) 
    prices = prices_all[syms]  # portfolio symbols
    prices_SPY = prices_all['SPY']  # SPY, for comparison
    prices_SPY_normalized = normalize_stocks(prices_SPY)
    normalized_price = normalize_stocks(prices)

    rolling_days = 20

    sma = compute_sma(normalized_price, rolling_days)
    columns = ['Price/SMA']
    prices_sma_ratio = pd.DataFrame(0, index = normalized_price.index, columns = columns)
    prices_sma_ratio['Price/SMA'] = normalized_price[symbol]/sma['SMA']
    momentum = compute_momentum(normalized_price, rolling_days)
    ema = compute_ema(normalized_price, rolling_days)
    columns = ['Price/EMA']
    prices_ema_ratio = pd.DataFrame(0, index = normalized_price.index, columns = columns)
    prices_ema_ratio['Price/EMA'] = normalized_price[symbol]/ema['EMA']
    macd = compute_macd(normalized_price)
    kd = compute_kd(normalized_price)
        

    sma_plot = pd.concat([normalized_price, sma, prices_sma_ratio], axis=1)
    sma_plot.columns = [symbol, 'SMA', 'Price/SMA']
    sma_plot.plot(grid=True, title='Simple Moving Average', use_index=True)
    plt.savefig("sma.png")


    momentum_plot = pd.concat([normalized_price, momentum], axis=1)
    momentum_plot.plot(grid=True, title='Momentum', use_index=True)
    plt.savefig("momentum.png")


    ema_plot = pd.concat([normalized_price, ema, prices_ema_ratio], axis=1)
    ema_plot.columns = [symbol, 'EMA', 'Price/EMA']
    ema_plot.plot(grid=True, title='Exponential Moving Average', use_index=True)
    plt.savefig("ema.png")
    
    
    macd_plot = pd.DataFrame(0, index = normalized_price.index, columns = columns)
    macd_plot = pd.concat([normalized_price, macd['ema_12'], macd['ema_26'],macd['MACD'],macd['Signal']], axis=1)
    macd_plot.columns = [symbol, '12 days EMA', '26 days EMA', 'MACD','Signal']
    fig, axes = plt.subplots(2, 1)
    fig.suptitle('Moving Average Convergence Divergence')
  

    axes[0].plot(macd_plot["JPM"])
    axes[0].plot(macd_plot["12 days EMA"])
    axes[0].plot(macd_plot["26 days EMA"])
    
    axes[1].plot(macd_plot["MACD"])
    axes[1].plot(macd_plot["Signal"])

    #axes[0].legend(loc="lower left")
    #axes[1].legend(loc="lower left")
    axes[0].get_xaxis().set_visible(False)
    axes[0].get_yaxis().set_visible(True)
    axes[1].tick_params(labelrotation=45)
    plt.savefig("macd.png")
    
    kd_plot = pd.DataFrame(0, index = normalized_price.index, columns = columns)
    kd_plot = pd.concat([normalized_price, kd['%K'], kd['%D']], axis=1)
    kd_plot.columns = [symbol, '%K', '%D']
    fig, axes = plt.subplots(2, 1)
    fig.suptitle('Stochastic Oscillator')


    axes[0].plot(kd_plot["JPM"])
    
    axes[1].plot(kd_plot["%K"])
    axes[1].plot(kd_plot["%D"])

    #axes[0].legend(loc="lower left")
    #axes[1].legend(loc="lower left")
    axes[0].get_xaxis().set_visible(False)
    axes[0].get_yaxis().set_visible(True)
    axes[1].tick_params(labelrotation=45)
    plt.savefig("kd.png")




def test_code():
    compute_indicators()

if __name__ == "__main__":
    test_code()
