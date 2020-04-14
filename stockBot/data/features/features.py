#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Sunday, 29 March 2020
"""

import yfinance as yf
import numpy as np
import functools

SP500 = '^GSPC'

def log_diff(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        df = function(*args, **kwargs)
        df = df.apply(np.log).diff()
        return df.fillna(method='bfill')
    return wrapper

def log_log_diff(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        df = function(*args, **kwargs)
        df_log = df.apply(np.log)
        df_shift_log = df.shift(-1).apply(np.log)
        df.iloc[:,:] = df_log.values - df_shift_log.values
        return df.fillna(0)
    return wrapper

def basic_features(df):
    # SP = yf.Ticker(SP500).history('max')
    # inter_index = SP.index.intersection(df.index)
    # df['SP500'] = SP['Close'].loc[inter_index]
    # df['SP500_vol5d'] = df['SP500'].rolling(window='5d').std()
    for days in [5, 10]:
        df['MA%d'%days]  = df['Close'].rolling(window='%dd'%days).mean() # Compute the moving average for {days} days
        df['Vol%d'%days] = df['Close'].rolling(window='%dd'%days).std() # Compute the volability for {days} days
        df['EWM%d'%days] = df['Close'].ewm(span=days).mean() # Compute the exponential moving average for {days} days
    # MACD = df['Close'].rolling(window='12d').mean() - df['Close'].rolling(window='26d').mean()
    # df['MACD-Signal'] = MACD - MACD.rolling(window='9d').mean()
    return df

def practice_features(df):
    df['logdiff'] = df['Close'].apply(np.log).diff()
    df['diff'] = df['Close'].diff()
    for days in [10, 20]:
        df['MA%d'%days]  = df['Close'].rolling(window='%dd'%days).mean() # Compute the moving average for {days} days
        df['Vol%d'%days] = df['Close'].rolling(window='%dd'%days).std() # Compute the volability for {days} days
        df['EWM%d'%days] = df['Close'].ewm(span=days).mean() # Compute the exponential moving average for {days} days
    return df.fillna(0)

@log_diff
def stat(*args, **kwargs):
    return basic_features(*args, **kwargs)
