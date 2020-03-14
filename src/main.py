#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Friday, 03 February 2020
"""

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from visualizer import plot_prediction

tsla = yf.Ticker("TSLA")
hist = tsla.history(period="max")


# Scale prices between 0 and 1
openScaler = MinMaxScaler()
openValues = hist['Open'].values.reshape((-1,1))
hist['OpenScaled'] = openScaler.fit_transform(openValues)

def get_epochs(data, window):
    """ Roll data to make a training set """
    return data[np.arange(data.shape[0]-window+1)[:,None] + np.arange(window)] 

# Get training and validate set
OpenScaledValues = hist['OpenScaled'].values 
TrainingSet = get_epochs(OpenScaledValues, 50)

#plt.Figure()
#hist.plot(y=['Open', 'Close'])
#plt.show()

if __name__=='__main__':
    TICK = 'SPCE'
    SPCE = yf.Ticker(TICK)
    hist = SPCE.history(period='max')
    plot_prediction("Preedict", hist, hist, ['Close','Open'])
