    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import datetime as dt                                                                                         
import random                                                                                         
import pandas as pd
from scipy import stats
import RTLearner as rt
import BagLearner as bl
from indicators import *  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		  	   		     		  		  		    	 		 		   		 		  
	     		  		  		    	 		 		   		 		  
   
    # constructor  		  	   		     		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.005, commission=9.95
):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Constructor method  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		     		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		     		  		  		    	 		 		   		 		  
        self.commission = commission  	
        self.learner = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size":10}, bags = 25, boost = False, verbose = False)
                                                                                          
                                                                                        
    def add_evidence(                                                                                         
        self,                                                                                         
        symbol="JPM",                                                                                         
        sd=dt.datetime(2008, 1, 1),                                                                                           
        ed=dt.datetime(2009, 12, 31),                                                                                           
        sv=10000,                                                                                         
    ):                                                                                            
                                                                                      
        syms = [symbol]                                                                                           
        dates = pd.date_range(sd, ed)                                                                                         
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY                                                                                           
        prices = prices_all[syms]  # only portfolio symbols                                                                                           
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later                                                                                          
        if self.verbose:                                                                                          
            print(prices)                                                                                        

        # Constructing features (trainX) - 3 indicators: SMA, MACD, Stochastic Oscillator 
        SMA = compute_sma(prices,20)
        MACD = compute_macd(prices)
        KD = compute_kd(prices)
        
        df1=SMA.rename(columns={symbol:'SMA'})
        df2=MACD.rename(columns={symbol:'MACD'})
        df3=KD.rename(columns={symbol:'KD'})
        features = pd.concat((df1,df2,df3),axis=1)
        features.fillna(0,inplace=True)
        features=features[:-5] 
        trainX = features.values
        
        # Constructing the labels (trainY) : +1(Long), -1(Short), 0(Cash) and the data will be based on 5 day return
        ret = prices.shift(-5)/prices - 1
        ret = ret.loc[ret[symbol].notnull(), symbol].values
        
        long_th = 0.02 + self.impact
        short_th = 0.0 - self.impact
        trainY = list(map(lambda x: 1 if x > long_th else -1 if x < short_th else 0, ret))
        trainY = np.array(trainY)

        # Training
        self.learner.add_evidence(trainX, trainY)
                

                                                                                       
    def testPolicy(                                                                                           
        self,                                                                                         
        symbol="JPM",                                                                                         
        sd=dt.datetime(2010, 1, 1),                                                                                           
        ed=dt.datetime(2011, 12, 31),                                                                                           
        sv=10000,                                                                                         
    ):                                                                                            
                                                                                       
        syms = [symbol]                                                                                                                                                               
        dates = pd.date_range(sd, ed)                                                                                         
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY 
        prices = prices_all[syms]  # only portfolio symbols 

        # Constructing features (testX) - 3 indicators: SMA, MACD, Stochastic Oscillator 
        SMA = compute_sma(prices,20)
        MACD = compute_macd(prices)
        KD = compute_kd(prices)
        
        df1=SMA.rename(columns={symbol:'SMA'})
        df2=MACD.rename(columns={symbol:'MACD'})
        df3=KD.rename(columns={symbol:'KD'})
        features = pd.concat((df1,df2,df3),axis=1)
        features.fillna(0,inplace=True)
        features=features[:-5] 
        testX = features.values
        
        
        # Querying the learner for testY
        testY=self.learner.query(testX)
        
        # Constructing trades DataFrame
        trades = prices_all[syms].copy()
        trades.loc[:]=0
        share = 0
        for i in range(0, len(prices) - 5):
            if testY[i] == -1:
                if share == 0:
                    share = -1000
                    trades.iloc[i, 0] = -1000
                elif share == 1000:
                    share = -1000
                    trades.iloc[i, 0] = -2000        
            if testY[i] == 1:
                if share == 0:
                    share = 1000
                    trades.iloc[i, 0] = 1000
                elif share == - 1000:
                    share = 1000
                    trades.iloc[i, 0] = 2000

        return trades
    	  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
