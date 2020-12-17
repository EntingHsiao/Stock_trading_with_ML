"""
testproject.py and implement the necessary calls (following each respective API) to 
Manual Strategy.py, StrategyLearner.py, experiment1.py and experiment2.py with the 
appropriate parameters to run everything needed for the report in a single Python call:


"""
# import warnings
# warnings.filterwarnings("ignore")

from util import get_data, plot_data
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from marketsimcode import compute_portvals
from indicators import *
import StrategyLearner as st
import ManualStrategy as ms
from experiment1 import *
from experiment2 import *


if __name__=="__main__":
    # setting the random seed
    np.random.seed(903648288)

    # input based on "DATA DETAILS, DATES & RULES"
    in_sd = dt.datetime(2008,1,1)
    in_ed = dt.datetime(2009, 12, 31)
    out_sd = dt.datetime(2010,1,1)
    out_ed = dt.datetime(2011, 12, 31)
    sv = 100000
    symbol = ['JPM']
    commission = 9.95
    impact = 0.005
    
    # ManualStrategy
    # In sample comparision 
    print("Manual Strategy - In sample comparision")
    manual = ms.ManualStrategy(verbose = False)
    df_benchmark = manual.benchmark(in_sd, in_ed, sv)
    df_optimized = manual.optimized(in_sd, in_ed, sv)
    manual.computeMetrics(df_benchmark, df_optimized[[0]])
    manual.chart_insample(df_benchmark, df_optimized)
    
    # Out sample comparision 
    print("Manual Strategy - Out sample comparision")
    manual = ms.ManualStrategy(verbose = False)
    df_benchmark = manual.benchmark(out_sd, out_ed, sv)
    df_optimized = manual.optimized(out_sd, out_ed, sv)
    manual.computeMetrics(df_benchmark, df_optimized[[0]])
    manual.chart_outsample(df_benchmark, df_optimized)

    # Expermiment 1 
    experiment1()
    
    # Experiment 2 
    experiment2()