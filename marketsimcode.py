import datetime as dt                                                                                         
import os   
import numpy as np  
import pandas as pd   
 

def compute_portvals(orders_df, start_date, end_date, start_val=100000, commission=0.0, impact=0.0):                                                                                            

    df = orders_df

    # Sort orders by date 
    df['Date'] = pd.to_datetime(df['Date'])
    df.index = df['Date']
    df.index.names = ['Date_Index']
    df.sort_index()
    df.sort_index(ascending=True, inplace=True)
 
    symbol = list(df["Symbol"].unique())

    df.loc[df["Order"] == "SELL", "Shares"] = -df.loc[df["Order"] == "SELL", "Shares"] 
    df_copy = df.copy()
    df_copy.reset_index(drop=True, inplace=True)
    df_copy = df_copy.drop(["Order"], axis=1)

    # df_price
    df_price = get_data(symbol, pd.date_range(start_date, end_date))
    df_price["CASH"] = 1.0
    df_price["Date"] = df_price.index
    df_price = df_price.sort_values(by='Date', ascending=True)

    # Adjust the start date for benchmark
    if df_copy.shape[0] == 1 and df_copy["Date"].iloc[0] < df_price["Date"].iloc[0]:
        df_copy.loc[0, "Date"] = df_price["Date"].iloc[0]

    # df_trades
    df_trades = pd.DataFrame()

    i = 0
    for index, row in df_copy.iterrows():
        df_trades.loc[i, "Date"] = row["Date"]
        df_trades.loc[i, row["Symbol"]] = row["Shares"]
        i += 1

    df_trades.fillna(0, inplace=True)

    all_stock_symbols = df_trades.columns.drop("Date")
    df_trades.columns = map(lambda x: x+"_SHARE" if x != "Date" else x, df_trades.columns)
    df_trades = df_trades.merge(df_price, how="right", on="Date")
    df_trades = df_trades.sort_values(["Date"])
    df_trades.reset_index(drop=True, inplace=True)
    df_trades.fillna(0, inplace=True)
    df_trades["FEE"] = 0.0

    for i, row in df_trades.iterrows():
        for sym in all_stock_symbols:
            sym_share = sym + "_SHARE"
            if row[sym_share] != 0:
                # Calculate transaction fees
                df_trades.loc[i, "FEE"] += commission
                # Calculate price impacts
                # Buying
                if row[sym_share] > 0:
                    df_trades.loc[i, sym] *= (1+impact)

                # Selling
                elif row[sym_share] < 0:
                    df_trades.loc[i, sym] *= (1-impact)


    df_trades["CASH"] = 0.0
    for sym in all_stock_symbols:
        sym_share = sym + "_SHARE"
        df_trades["CASH"] += -df_trades[sym]*df_trades[sym_share]

    df_trades["CASH"] -= df_trades["FEE"]
    df_trades = df_trades.drop(all_stock_symbols, axis=1).drop(["SPY", "FEE"], axis=1)
    df_trades = df_trades.groupby(by=["Date"], as_index=False).sum()

    # df_holdings
    df_holdings = df_trades.copy()

    for i, row in df_holdings.iterrows():

        if i == 0:
            df_holdings.loc[i, "CASH"] += start_val
            continue

        for sym in all_stock_symbols:

            sym_share = sym + "_SHARE"
            df_holdings.loc[i, sym_share] += df_holdings.loc[i-1, sym_share]

        df_holdings.loc[i, "CASH"] += df_holdings.loc[i-1, "CASH"]


    # df_value
    df_value = df_holdings.merge(df_price.drop(["SPY", "CASH"], axis=1), on="Date")

    for sym in all_stock_symbols:
        df_value[sym] *= df_value[sym + "_SHARE"]
    
    columns_to_drop = map(lambda x: x+"_SHARE", all_stock_symbols)
    df_value = df_value.drop(columns_to_drop, axis=1)
    df_value['portvals'] = np.sum(df_value, axis=1)                                                                                         
    df_value.set_index("Date", inplace=True)      
    df_value.rename(columns={"portvals": 0}, inplace=True)
                                                                    
    return df_value[[0]]                                                                             
                                                                                                                                                                                         
                                                                                          
if __name__ == "__main__":                                                                                            
    compute_portvals()                                                                                             
