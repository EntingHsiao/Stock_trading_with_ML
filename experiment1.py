"""
Experiment 1

Compare Manual Strategy with Strategy Learner in-sample trading JPM. Create a chart that shows:

Value of the ManualStrategy portfolio (normalized to 1.0 at the start)
Value of the StrategyLearner portfolio (normalized to 1.0 at the start)
Value of the Benchmark portfolio (normalized to 1.0 at the start)

The in-sample period is January 1, 2008 to December 31, 2009.
The out-of-sample/testing period is January 1, 2010 to December 31 2011.
"""

import datetime as dt
import pandas as pd
import util as ut
import random
import numpy as np
import StrategyLearner as st
import ManualStrategy as ms
from marketsimcode import compute_portvals
from util import get_data, plot_data
import matplotlib.pyplot as plt


def process_trades(df, symbol):
    df = df.loc[df[symbol] != 0]
    df["Order"] = df[symbol].apply(lambda x: "BUY" if x > 0 else "SELL")
    df["Shares"] = df[symbol].apply(lambda x: abs(x))
    df["Symbol"] = symbol
    df["Date"] = df.index
    return df
    
def experiment1():
    # setting the random seed
    np.random.seed(903648288)

    # input based on "DATA DETAILS, DATES & RULES"
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009, 12, 31)
    sv = 100000
    symbol = ['JPM']
    dates = pd.date_range(sd, ed)
    prices_all = ut.get_data(symbol, dates)
    
    # ManualStrategy
    manual = ms.ManualStrategy(verbose = False)
    ms_trades = manual.testPolicy(symbol='JPM', sd=sd ,ed=ed, sv=100000)
    ms_trades = process_trades(ms_trades, 'JPM')
    ms_portval = compute_portvals(ms_trades,sd,ed,100000,commission=9.95,impact=0.005)
    
    # Strategy Learner
    learner = st.StrategyLearner(verbose = False, impact=0.005)
    learner.add_evidence(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    st_test = learner.testPolicy(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    st_test = process_trades(st_test, 'JPM')
    st_portval = compute_portvals(st_test,sd,ed,sv,commission=9.95,impact=0.005)

    # Benchmark
    bench = pd.DataFrame([["BUY", 1000, "JPM", sd]], columns=["Order", "Shares", "Symbol", "Date"])
    bench_portval = compute_portvals(bench, sd, ed, sv, commission=9.95, impact=0.005)
    
    # Computing Portfolio statistics
    ma_dr = (ms_portval / ms_portval.shift(1)) - 1
    ma_dr = ma_dr[1:]
    ma_cr = (ms_portval.iloc[-1] / ms_portval.iloc[0]) - 1
    ma_adr = ma_dr.mean()
    ma_sddr = ma_dr.std()
    a = np.sqrt(252.0)
    ma_sr = (a*(ma_adr))/ma_sddr

    # Computing StrategyLearner statistics
    st_dr = (st_portval / st_portval.shift(1)) - 1
    st_dr = st_dr[1:]
    st_cr = (st_portval.iloc[-1] / st_portval.iloc[0]) - 1
    st_adr = st_dr.mean()
    st_sddr = st_dr.std()
    a = np.sqrt(252.0)
    st_sr = (a*(st_adr))/st_sddr
    
    # Printing Benchmark statistics
    bench_dr = (bench_portval / bench_portval.shift(1)) - 1
    bench_dr = bench_dr[1:]
    bench_cr = (bench_portval.iloc[-1] / bench_portval.iloc[0]) - 1
    bench_adr = bench_dr.mean()
    bench_sddr = bench_dr.std()
    a = np.sqrt(252.0)
    bench_sr = (a*(bench_adr))/bench_sddr

    print ("In Sample Cumulative Return of Manual Strategy: {}".format(ma_cr[0]))
    print ("In Sample Cumulative Return of Machine Learning Strategy: {}".format(st_cr[0]))
    print ("In Sample Cumulative Return of Benchmark: {}".format(bench_cr[0]))
    print
    print ("In Sample Standard Deviation of Manual Strategy: {}".format(ma_sddr[0]))
    print ("In Sample Standard Deviation of Machine Learning Strategy: {}".format(st_sddr[0]))
    print ("In Sample Standard Deviation of Benchmark: {}".format(bench_sddr[0]))
    print
    print ("In Sample Average Daily Return of Manual Strategy: {}".format(ma_adr[0]))
    print ("In Sample Average Daily Return of Machine Learning Strategy: {}".format(st_adr[0]))
    print ("In Sample Average Daily Return of Benchmark: {}".format(bench_adr[0]))
    print
    print ("In Sample Sharpe Ratio of Manual Strategy: {}".format(ma_sr[0]))
    print ("In Sample Sharpe Ratio of Machine Learning Strategy: {}".format(st_sr[0]))
    print ("In Sample Sharpe Ratio of Benchmark: {}".format(bench_sr[0]))
    print
    print ("In Sample Final Portfolio Value of Manual Strategy: {}".format(ms_portval.iloc[-1,0]))
    print ("In Sample Final Portfolio Value of Machine Learning Strategy: {}".format(st_portval.iloc[-1,0]))
    print ("In Sample Final Portfolio Value of Benchmark: {}".format(bench_portval.iloc[-1,0]))

    # Plotting charts
    ms_portval = ms_portval / ms_portval.iloc[0, 0]
    st_portval = st_portval / st_portval.iloc[0, 0]
    bench_portval = bench_portval / bench_portval.iloc[0, 0]
    fig = plt.figure(figsize=(10,5), dpi=80)
    plt.plot(st_portval, color='r', label='Portfolio(Strategy_Learner)')
    plt.plot(bench_portval, color='g', linestyle=':', linewidth=2, label='Benchmark')
    plt.plot(ms_portval, color='b', label='Manual')
    plt.xlabel('Dates', fontsize=14)
    plt.ylabel('Portfolio value', fontsize=14)
    
    fig.suptitle('Experiment 1 : In-Sample Comparisons among Benchmark vs Manual vs Strategy', fontsize=12)
    fig.legend(loc=3, bbox_to_anchor=(0.08, 0.7))
    #plt.show()
    plt.savefig("Experiment_1.png")
    
    
