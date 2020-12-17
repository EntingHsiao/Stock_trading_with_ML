# Stock_trading_with_ML
## Compare the performance of 3 portfolios: hand-crafted strategy, benchmark and Machine Learning Strategy 


In this project, I compared three stock portfolios below:
* Manual Strategy portfolio: I implemented a set of hand crafted rules using 3 technical indicators, Simple Moving Average(SMA), moving average convergence divergence (MACD) and stochastic oscillator, to determine a buy/sell signal.
* Strategy Learner portfolio: I developed a random forest learner that can learn a trading policy using the same technical indicators above.
* Benchmark portfolio : The performance of a portfolio starting with $100,000 cash, investing in 1000 shares of the symbol "JPM" in use on the first trading day, and holding that position. Include transaction costs.



Below are the descriptions for all related files:


* ManualStrategy.py: The function testPolicy under the class ManualStrategy will return a data frame containing trades. Part of this code also call marketsimcode.py to generate the plots used in the report. 

* StrategyLearner.py: The function add_evidence in StrategyLearner is used to train the ML model. The function testPolicy is used to make predictions.

* indicators.py: Both of ManualStrategy and StrategyLearner call indicators.py to compute the selected indicators.

* experiment1.py: The code calls ManualStrategy and StrategyLearner to compare the performance of your Manual Strategy with your Strategy Learner in-sample trading JPM.

* experiment2.py: This code calls StrategyLearner to conduct an experiment that shows how changing the value of impact should affect in-sample trading behavior.

* marketsimcode.py: The code is used in ManualStrategy, StrategyLearner, experiment1, experiment2 to compute the portfolio values for generating metrics and charts.  

* testproject.py: This is an entry point to test all the codes against the report and it will output all necessary charts and statistics for your report.

* RTLearner.py: The code is called in StrategyLearner to train and test the model. It is the base learner used in BagLearner.py

* BagLearner.py: The code is called in StrategyLearner to train and test the model.



