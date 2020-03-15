#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 14 March 2020
"""

from settings import *
import tensorflow as tf
import xgboost as xgb
from sklearn.model_selection import train_test_split 
import seaborn as sns, numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# [1] Importance of features from xgb

#df_train, df_test = train_test_split(df, test_size=TESTSIZE, shuffle=False)
#X, features = ['Close'], ['Volume']
#eval_set = [(X_train, Y_train), (X_test, Y_test)] = [(df_train[X], df_train[features]), (df_test[X], df_test[features])]
#
#regressor = xgb.XGBRegressor(gamma=0.0, n_estimators=150, base_score=0.7, colsample_bytree=1, learning_rate=0.05)
#xgbModel = regressor.fit(X_train, Y_train, eval_set=eval_set, verbose=False)
#eval_result = regressor.evals_result()
#
#fig = plt.figure(figsize=(8,8))
#plt.xticks(rotation='vertical')
#plt.bar([i for i in range(len(xgbModel.feature_importances_))], xgbModel.feature_importances_.tolist(), tick_label=X_test.columns)
#plt.title('Feature importance of the technical indicators.')
#plt.show()

# [2] Features correlation

def df_preprocess_yfinance(df):
    # Add MACD ou difference 
    df = df.drop(['Dividends', 'Stock Splits'], axis=1)
    for days in [5, 10, 30]:
        df['MA%d'%days]  = df['Close'].rolling(window=days).mean() # Compute the moving average for {days} days
        df['Vol%d'%days] = df['Close'].rolling(window=days).std() # Compute the volability for {days} days
    return df

def correlation(df):
    corrmat = df.corr()
    plt.figure()
    g = sns.heatmap(corrmat, annot=True, cmap='RdYlGn')
    plt.show()


if __name__=='__main__':
    df = df_preprocess_yfinance(df)
    df_to_plot = df.drop('Volume', axis=1)
    correlation(df)
