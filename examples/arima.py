#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Wednesday, 19 March 2020
"""

import sys
for path in ['.', '..']:
    sys.path.append(path)
import matplotlib.pyplot as plt
import alpha_vantage
import numpy as np
import pandas as pd
from stockBot.preprocess.preprocess import df_preprocess_alpha_vantage
from stockBot.visualizer.visualizer import plot_test_prediction
from statsmodels.tsa.arima_model import ARIMA
from sklearn.model_selection import train_test_split

TS = alpha_vantage.timeseries.TimeSeries(output_format='pandas')
df_alpha_vantage = TS.get_intraday('SPCE', outputsize='full', interval='30min')[0]
df = df_preprocess_alpha_vantage(df_alpha_vantage)
df_train, df_test = train_test_split(df, test_size=0.2, shuffle=False) # Get train and test data
predictions = list() # All forecasts of ARIMA model
history = [value for value in df_train['Close'].values] # Get the history of data to predict
for t in range(len(df_test.index)):
    model = ARIMA(history, (5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    predictions.append(*output[0])
    history.append(df_test['Close'][t])

df_test['PredictedClose'] = pd.Series(np.array(predictions), index=df_test.index)

plt.figure()
plot_test_prediction(df['Close'], df_test['PredictedClose'], mse=True)
plt.legend()
plt.show()
