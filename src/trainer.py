#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 14 March 2020
"""

import tensorflow as tf
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler




if __name__=='__main__':
    TICK = 'SPCE'
    SPCE = yf.Ticker(TICK)
    hist = SPCE.history(period='max')
    plt.Figure()
    hist['Open'].plot()
    plt.show()
