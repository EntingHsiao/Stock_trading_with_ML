"""
Code implementing a TheoreticallyOptimalStrategy object
It should implement testPolicy() which returns a trades data frame
The main part of this code should call marketsimcode as necessary to generate the plots used in the report
"""



from util import get_data, plot_data
import datetime as dt
import pandas as pd
import numpy as np
from marketsimcode import compute_portvals
from indicators import *
import matplotlib.pyplot as plt


class ManualStrategy(object):

    # constructor
    def __init__(self, verbose = False):
        self.verbose = verbose

 
    
    def testPolicy(self, symbol, sd, ed, sv):
        df = get_data([symbol], pd.date_range(sd, ed))
        price_df = df[[symbol]]
        price_df = price_df.fillna(method='ffill')
        price_df = price_df.fillna(method='bfill')


        df_trades = df[['SPY']]
        df_trades = df_trades.rename(
        columns={'SPY': symbol}).astype({symbol: 'int32'})
        df_trades[:] = 0
        dates = df_trades.index

        #normalize prices 
        price_df = price_df / price_df.iloc[0]
        #use SMA to be the trade signal and set the rolling days # as 20
        price_df['SMA']= compute_sma(price_df, 20)
        #use MACD to be the trade signal 
        price_df['MACD']= compute_macd(price_df)
        #use KD to be the trade signal 
        price_df['%KD'] = compute_kd(price_df)
       # price_df['%KD'] is postive: sell; price_df['%KD'] is negative: buy  

        net_position = 0   

        for curr_date, row in price_df.iterrows():
            # signals indicates to buy
            if row['SMA'] < 0.730 and row['MACD'] > 0.0008 and row['%KD'] < -3.87:
                if net_position == 0:
                    net_position = 1000
                    df_trades.loc[curr_date, symbol] = 1000
                elif net_position == -1000:
                    net_position = 1000
                    df_trades.loc[curr_date, symbol] = 2000
                    
            # signals indicates to sell
            elif row['SMA'] > 0.757 and row['MACD'] < 0.0006 and row['%KD'] > 0.88:
                if net_position == 0:
                    net_position = -1000
                    df_trades.loc[curr_date, symbol] = -1000
                elif net_position == 1000:
                    net_position = -1000
                    df_trades.loc[curr_date, symbol] = -2000

        return df_trades     

    # starting with $100,000 cash, investing in 1000 shares of JPM and holding that position
    def benchmark(self,sd, ed, sv=100000):
        # initialize list of lists 
        data = [[sv, 'JPM', 'BUY', 1000]]
        df_trade_jpm = pd.DataFrame(data, columns=['Date', 'Symbol', 'Order', 'Shares']) 
        portvals = compute_portvals(df_trade_jpm, sd, ed, sv, commission=9.95, impact=0.005)
        return portvals


    def optimized(self, sd, ed, sv=100000):
        sym = "JPM"
        df_trade_optimal = self.testPolicy(sym, sd, ed, sv)
        df_trade_optimal = df_trade_optimal.loc[df_trade_optimal[sym] != 0]
        df_trade_optimal["Date"] = df_trade_optimal.index
        df_trade_optimal["Symbol"] = sym
        df_trade_optimal["Order"] = df_trade_optimal[sym].apply(lambda x: "BUY" if x > 0 else "SELL")
        df_trade_optimal["Shares"] = abs(df_trade_optimal[sym])
        df_trade_optimal = df_trade_optimal.drop([sym], axis=1)

        portvals = compute_portvals(df_trade_optimal, sd, ed, sv, commission=9.95, impact=0.005)
        df_trade_optimal.set_index("Date", inplace=True)
        df_trades = portvals.merge(df_trade_optimal, on="Date", how="left")
        return df_trades

    def computeMetrics(self, df_benchmark, df_optimal):

    #Cumulative return of the benchmark and portfolio
        cr_benchmark = df_benchmark[0][-1] / df_benchmark[0][0] - 1
        cr_optimal = df_optimal[0][-1] / df_optimal[0][0] - 1

    # daily return in percentage
        dp_benchmark = (df_benchmark / df_benchmark.shift() - 1).iloc[1:]
        dp_optimal = (df_optimal / df_optimal.shift() - 1).iloc[1:]

    #Stdev of daily returns of benchmark and portfolio
        sddr_benchmark = dp_benchmark.std()
        sddr_optimal = dp_optimal.std()

    #Mean of daily returns of benchmark and portfolio
        adr_benchmark = dp_benchmark.mean()
        adr_optimal = dp_optimal.mean()
        print("Cumulative return- Benchmark: " +str(cr_benchmark))
        print("Stdev of daily returns- Benchmark: " + str(sddr_benchmark.values[0]))
        print("Mean of daily returns - of Benchmark: " + str(adr_benchmark.values[0]))
        print("Cumulative returns- Manual Strategy: " + str(cr_optimal))
        print("Stdev of daily returns- Manual Strategy: " + str(sddr_optimal.values[0]))
        print("Mean of daily returns- Manual Strategy: " + str(adr_optimal.values[0]))


    def chart_insample(self, df_benchmark, df_optimal):
        
        # normalize 
        df_benchmark = df_benchmark / df_benchmark.iloc[0]
        df_optimal[0] = df_optimal[0] / df_optimal.iloc[0,0]
        
        plt.figure(figsize=(14,8))
        plt.title("Manual Strategy - In-sample")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.xticks(rotation=45)
        plt.grid()
        plt.plot(df_benchmark, label="benchmark", color = "green")
        plt.plot(df_optimal[0], label="Manual Strategy", color = "red")
        
        buy_dates = df_optimal.loc[df_optimal['Order'] == "BUY"].index
        for bd in buy_dates:
            plt.axvline(x=bd, color='b',label ="Long Entry Point")
        
        sell_dates = df_optimal.loc[df_optimal['Order'] == "SELL"].index
        for sd in sell_dates:
            plt.axvline(x=sd, color='k',label ="Short Entry Point")
        plt.legend()
        plt.savefig("Manual Strategy - In-sample.png", bbox_inches='tight')
        #plt.show()

    def chart_outsample(self,df_benchmark, df_optimal):
        
        # normalize 
        df_benchmark = df_benchmark / df_benchmark.iloc[0]
        df_optimal[0] = df_optimal[0] / df_optimal.iloc[0,0]
        
        plt.figure(figsize=(14,8))
        plt.title("Manual Strategy - Out-sample")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.xticks(rotation=45)
        plt.grid()
        plt.plot(df_benchmark, label="benchmark", color = "green")
        plt.plot(df_optimal[0], label="Manual Strategy", color = "red")
        
        buy_dates = df_optimal.loc[df_optimal['Order'] == "BUY"].index
        for bd in buy_dates:
            plt.axvline(x=bd, color='b',label ="Long Entry Point")
        
        sell_dates = df_optimal.loc[df_optimal['Order'] == "SELL"].index
        for sd in sell_dates:
            plt.axvline(x=sd, color='k',label ="Short Entry Point")
        plt.legend()
        plt.savefig("Manual Strategy - Out-sample.png", bbox_inches='tight')
        #plt.show()
