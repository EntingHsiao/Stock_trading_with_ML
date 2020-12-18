"""
Experiment 2

An experiment with StrategyLearner that shows how changing the value of impact would affect
trading behavior.
Trade JPM on the in-sample period with a commission of $0.00.
The in-sample period is January 1, 2008 to December 31, 2009.
"""

import datetime as dt
import pandas as pd
import util as ut
import random
import numpy as np
import StrategyLearner as st
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
    

def experiment2():
    # setting the random seed
    np.random.seed(903648288)

    # input based on "DATA DETAILS, DATES & RULES"
    is_sd = dt.datetime(2008,1,1)
    is_ed = dt.datetime(2009, 12, 31)
    os_sd = dt.datetime(2010,1,1)
    os_ed = dt.datetime(2011, 12, 31)
    sv = 100000
    symbol = ['JPM']
    
    # Strategy Learner with impact=0.005
    learner = st.StrategyLearner(verbose = False, impact=0.005)
    learner.add_evidence("JPM",is_sd,is_ed ,sv=100000)
    st1_test = learner.testPolicy("JPM",is_sd,is_ed,sv=100000)
    st1_test = process_trades(st1_test, 'JPM')
    st1_portval = compute_portvals(st1_test, is_sd,is_ed,sv,commission=0.0,impact=0.005)

    # Strategy Learner with impact=0.0
    learner = st.StrategyLearner(verbose = False, impact=0.0)
    learner.add_evidence("JPM",is_sd,is_ed,sv=100000)
    st2_test = learner.testPolicy("JPM",is_sd,is_ed,sv=100000)
    st2_test = process_trades(st2_test, 'JPM')
    st2_portval = compute_portvals(st2_test,is_sd,is_ed,sv,commission=0.0,impact=0.0)
    
    # Strategy Learner with impact=0.05
    learner = st.StrategyLearner(verbose = False, impact=0.05)
    learner.add_evidence("JPM",is_sd,is_ed,sv=100000)
    st3_test = learner.testPolicy("JPM",is_sd,is_ed,sv=100000)
    st3_test = process_trades(st3_test, 'JPM')
    st3_portval = compute_portvals(st3_test,is_sd,is_ed,sv,commission=0.0,impact=0.05)


    # Computing StrategyLearner statistics with impact=0.005
    st1_dr = (st1_portval / st1_portval.shift(1)) - 1
    st1_dr = st1_dr[1:]
    st1_cr = (st1_portval.iloc[-1] / st1_portval.iloc[0]) - 1
    st1_adr = st1_dr.mean()
    st1_sddr = st1_dr.std()
    a = np.sqrt(252.0)
    st1_sr = (a*(st1_adr))/st1_sddr
    
    # Computing StrategyLearner statistics with impact=0.0
    st2_dr = (st2_portval / st2_portval.shift(1)) - 1
    st2_dr = st2_dr[1:]
    st2_cr = (st2_portval.iloc[-1] / st2_portval.iloc[0]) - 1
    st2_adr = st2_dr.mean()
    st2_sddr = st2_dr.std()
    a = np.sqrt(252.0)
    st2_sr = (a*(st2_adr))/st2_sddr
    
    # Computing StrategyLearner statistics with impact=0.05
    st3_dr = (st3_portval / st3_portval.shift(1)) - 1
    st3_dr = st3_dr[1:]
    st3_cr = (st3_portval.iloc[-1] / st3_portval.iloc[0]) - 1
    st3_adr = st3_dr.mean()
    st3_sddr = st3_dr.std()
    a = np.sqrt(252.0)
    st3_sr = (a*(st3_adr))/st3_sddr
    

    print ("In Sample Cumulative Return of StrategyLearner with impact=0.005: {}".format(st1_cr[0]))
    print ("In Sample Cumulative Return of StrategyLearner with impact=0: {}".format(st2_cr[0]))
    print ("In Sample Cumulative Return of StrategyLearner with impact=0.05: {}".format(st3_cr[0]))
    print
    print ("In Sample Standard Deviation of StrategyLearner with impact=0.005: {}".format(st1_sddr[0]))
    print ("In Sample Standard Deviation of StrategyLearner with impact=0: {}".format(st2_sddr[0]))
    print ("In Sample Standard Deviation of StrategyLearner with impact=0.05: {}".format(st3_sddr[0]))
    print
    print ("In Sample Average Daily Return of StrategyLearner with impact=0.005: {}".format(st1_adr[0]))
    print ("In Sample Average Daily Return of StrategyLearner with impact=0: {}".format(st2_adr[0]))
    print ("In Sample Average Daily Return of StrategyLearner with impact=0.05: {}".format(st3_adr[0]))
    print
    print ("In Sample Sharpe Ratio of StrategyLearner with impact=0.005: {}".format(st1_sr[0]))
    print ("In Sample Sharpe Ratio of StrategyLearner with impact=0: {}".format(st2_sr[0]))
    print ("In Sample Sharpe Ratio of StrategyLearner with impact=0.05: {}".format(st3_sr[0]))
    print
    print ("In Sample Final Portfolio Value of StrategyLearner with impact=0.005: {}".format(st1_portval.iloc[-1,0]))
    print ("In Sample Final Portfolio Value of StrategyLearner with impact=0: {}".format(st2_portval.iloc[-1,0]))
    print ("In Sample Final Portfolio Value of StrategyLearner with impact=0.05: {}".format(st3_portval.iloc[-1,0]))

    # Plotting charts
    st1_portval = st1_portval / st1_portval.iloc[0, 0]
    st2_portval = st2_portval / st2_portval.iloc[0, 0]
    st3_portval = st3_portval / st3_portval.iloc[0, 0]
    fig = plt.figure(figsize=(10,5), dpi=80)
    plt.plot(st1_portval, color='r', label='Impact = 0.005')
    plt.plot(st2_portval, color='g', linestyle=':', linewidth=2, label='Impact = 0')
    plt.plot(st3_portval, color='b', label='Impact = 0.05')
    plt.xlabel('Dates', fontsize=14)
    plt.ylabel('Portfolio value', fontsize=14)
    
    fig.suptitle('Experiment 2 : In-Sample Comparisons when Impact = 0.005/0/0.05', fontsize=12)
    fig.legend(loc=3, bbox_to_anchor=(0.08, 0.7))
    #plt.show()
    plt.savefig("Experiment_2.png")
