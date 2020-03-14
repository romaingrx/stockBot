#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Thursday, 12 March 2020
"""

import yfinance as yf
import matplotlib.pyplot as plt
import sys
from sklearn.metrics import mean_squared_error
import numpy as np
import setting
import pandas as pd

DEFAULT = ['SPCE','TSLA','AMD']

def plot_prediction(title, df_real, df_test, args):
    fig = plt.Figure()
    ax = plt.axes() 
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price [$]')
    total_mse = np.mean([mean_squared_error(df_real[arg],df_test[arg]) for arg in args])
    df_real[args].plot(color='purple', linestyle='-',ax=ax, label='Real data')
    df_test[args].plot(color='red', linestyle='--',ax=ax, label='Predicted data')
    ax.plot([],[],linestyle=' ',label="MSE : %.2f"%(total_mse))
    plt.legend()
    plt.show()

def plot_fourier(df):
    plt.figure(dpi=100)
    plt.title('Fourier transforms on stock price')
    plt.xlabel('Date')
    plt.ylabel('Price [$]')
    FFT = np.fft.fft(np.asarray(df['Close'].tolist()))
    for num in [3, 6, 9, 15, 30, 50]: 
        fft = np.copy(FFT)
        fft[num:-num] = 0
        ifft = np.fft.ifft(fft) 
        plt.plot(pd.to_datetime(np.linspace(pd.Timestamp(df.index.values[0]).value,pd.Timestamp(df.index.values[-1]).value,len(ifft))), np.real(ifft), linestyle='--', label='Fourier transform with %d components'%num)
    plt.plot(df.index.values,df['Close'], color='purple', ls='-', label='Real')
    plt.legend()
    plt.show()


def visualize(args):
    tickers = list(map(lambda arg : yf.Ticker(arg), args))
    hist    = list(map(lambda arg : arg.history(period='1d'), tickers))
    print(hist[0]['Open'])
    return None


if __name__=='__main__':
    SPCE = yf.Ticker('SPCE')
    hist = SPCE.history(period='max')
    plot_fourier(hist)
