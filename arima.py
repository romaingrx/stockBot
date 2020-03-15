#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 14 March 2020
"""

from settings import *
from visualizer import plot_prediction
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
from pandas.plotting import autocorrelation_plot
from sklearn.model_selection import train_test_split



df_train, df_test = train_test_split(df, test_size=TESTSIZE, shuffle=False) # Get train and test data
predictions = list() # All forecasts of ARIMA model
history = [value for value in df_train['Close'].values] # Get the history of data to predict
for t in range(len(df_test.index)):
    model = ARIMA(history, (5,1,0)) 
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    predictions.append(*output[0]) 
    history.append(df_test['Close'][t])

df_test['Close'] = predictions
plot_prediction("Arima forecast", df, df_test, ['Close'], mse=True)
