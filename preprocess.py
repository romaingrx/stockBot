#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Wednesday, 19 March 2020
"""
from settings import *
import datetime


def df_preprocess_alpha_vantage(df):
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df = df.sort_index()
    for days in [5, 10, 15]:
        df['MA%d'%days]  = df['Close'].rolling(window='%dd'%days).mean() # Compute the moving average for {days} days
        df['Vol%d'%days] = df['Close'].rolling(window='%dd'%days).std() # Compute the volability for {days} days
    MACD = df['Close'].rolling(window='12d').mean() - df['Close'].rolling(window='26d').mean()
    df['MACD-Signal'] = MACD - MACD.rolling(window='9d').mean()
    return df

def df_preprocess_yfinance(df):
    df = df.drop(['Dividends', 'Stock Splits'], axis=1)
    df = df.sort_index()
    for days in [5, 10, 15]:
        df['MA%d'%days]  = df['Close'].rolling(window='%dd'%days).mean() # Compute the moving average for {days} days
        df['Vol%d'%days] = df['Close'].rolling(window='%dd'%days).std() # Compute the volability for {days} days
    MACD = df['Close'].rolling(window='12d').mean() - df['Close'].rolling(window='26d').mean()
    df['MACD-Signal'] = MACD - MACD.rolling(window='9d').mean()
    return df
