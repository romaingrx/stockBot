#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Wednesday, 19 March 2020
"""

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import yfinance as yf

TS = TimeSeries(output_format='pandas')


# # # # # # #
# VARIABLES #
# # # # # # #

TESTSIZE = 0.2 # Size of seperation between train and validation data

# # # # # # # # # #
# FIXED VARIABLES #
# # # # # # # # # #

MODELNAME       = ''
MODELPATH       = './res/models/%s'%(MODELNAME)
TENSORBOARDPATH = './res/tensorboards/%s'%(MODELNAME)


# # # # # # #
# SETTINGS  #
# # # # # # #

plt.rcParams['figure.facecolor'] = '#A9A9A9'
plt.rcParams['axes.facecolor'] = '#A9A9A9'
