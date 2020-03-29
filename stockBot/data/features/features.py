#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Sunday, 29 March 2020
"""

import yfinance as yf

SP500 = '^GSPC'

def basic_features(df):
    SP = yf.Ticker(SP500).history('max')
    inter_index = SP.index.intersection(df.index)
    # df['SP500'] = SP['Close'].loc[inter_index]
    # df['SP500_vol5d'] = df['SP500'].rolling(window='5d').std()
    for days in [10, 15, 20]:
        df['MA%d'%days]  = df['Close'].rolling(window='%dd'%days).mean() # Compute the moving average for {days} days
        df['Vol%d'%days] = df['Close'].rolling(window='%dd'%days).std() # Compute the volability for {days} days
        df['EWM%d'%days] = df['Close'].ewm(span=days).mean() # Compute the exponential moving average for {days} days
    # MACD = df['Close'].rolling(window='12d').mean() - df['Close'].rolling(window='26d').mean()
    # df['MACD-Signal'] = MACD - MACD.rolling(window='9d').mean()
    return df
