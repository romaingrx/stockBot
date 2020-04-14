#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Sunday, 22 March 2020
"""
from abc import abstractmethod
from typing import List, Text
import yfinance as yf
import numpy as np

from stockBot.types import streamerSource
from stockBot.exceptions import StreamerSourceError
from .streamers import streamer_mapper, yfinance, alpha_vantage, quandl

class Data_Streamer:

    def __init__(self, tickers:List[Text] or Text, src:streamerSource or Text=streamerSource.YFINANCE, random:bool=False, train_size:float=None, features_function=None, **kwargs):
        if not isinstance(src, streamerSource) and not src in streamerSource.values():
            raise StreamerSourceError(src)
        self.random           = random
        self.features_function = features_function or 'basic_features'
        self.history_capacity = kwargs.get('history_capacity', None)
        self.src          = src.value if isinstance(src, streamerSource) else src
        self.ticker_names = tickers if isinstance(tickers, list) else [tickers]
        self.Streamer     = streamer_mapper[self.src](self.ticker_names, self.features_function)
        self.DataFrames   = self.Streamer.DataFrames
        self.prices_rows  = self.Streamer.prices_rows
        self.n_features   = self.DataFrames[self.ticker_names[0]].shape[1]
        self.train_size   = train_size or 1
        self.iter         = {ticker_name:0 for ticker_name in self.ticker_names}
        self.lower_lim    = {ticker_name:0 for ticker_name in self.ticker_names}
        self.upper_lim    = {ticker_name:int(self.train_size*len(self.prices_rows[ticker_name].index)) for ticker_name in self.ticker_names}

    def has_next(self, ticker_name):
        return True if self.iter[ticker_name]<self.upper_lim[ticker_name] else False

    def next(self, ticker_name):
        """
            Return the date, the next row with all features and the price at the good step
        """
        if not self.has_next(ticker_name):
            raise IndexError()
        iter = self.iter[ticker_name]
        self.iter[ticker_name] += 1
        return self.prices_rows[ticker_name].index[iter], self.DataFrames[ticker_name].iloc[iter], self.prices_rows[ticker_name].values[iter]

    def reset_ticker(self, ticker_name):
        self.iter[ticker_name] = 0
        if self.random:
            length = len(self.close_prices[ticker_name].index)
            randint = self.random.randint(1,length/3)
            mid     = np.random.randint(self.history_capacity, length-randint)
            self.lower_lim[ticker_name] = mid - self.history_capacity
            self.upper_lim[ticker_name] = mid + randint
            self.iter[ticker_name]      = self.lower_lim[ticker_name]

    def get_price(self, ticker, date):
        return self.prices_rows[ticker][date]

    def reset(self):
        for ticker_name in self.ticker_names:
            self.reset_ticker(ticker_name)

already_downloaded = {}

def get_step_data(ticker_name, step):
    try:
        return already_downloaded[ticker_name][step]
    except:
        tick = yf.Ticker(ticker_name)
        df = tick.history('max')
        close_prices = df['Close']
        already_downloaded[ticker_name] = close_prices
        return already_downloaded[ticker_name][step]
