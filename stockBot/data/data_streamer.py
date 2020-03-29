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

    def __init__(self, tickers:List[Text] or Text, src:streamerSource or Text=streamerSource.YFINANCE, api_key:Text=None):
        self._api_key = api_key
        if not isinstance(src, streamerSource) and not src in streamerSource.values():
            raise StreamerSourceError(src)
        self.src = src.value if isinstance(src, streamerSource) else src
        self.ticker_names = tickers if isinstance(tickers, list) else [tickers]
        self.Streamer = streamer_mapper[self.src](self.ticker_names)
        self.DataFrames = self.Streamer.DataFrames
        self.prices_rows = self.Streamer.prices_rows
        self.n_features = self.DataFrames[self.ticker_names[0]].shape[1]
        self.iter = {ticker_name:0 for ticker_name in self.ticker_names}

    def has_next(self, ticker_name):
        return True if self.iter[ticker_name]<len(self.DataFrames[ticker_name]) else False

    def next(self, ticker_name):
        """
            Return the next row with all features and the price at the good step
        """
        if not self.has_next(ticker_name):
            raise IndexError()
        iter = self.iter[ticker_name]
        self.iter[ticker_name] += 1
        return self.DataFrames[ticker_name].iloc[iter], self.prices_rows[ticker_name].values[iter]

    def reset_ticker(self, ticker_name):
        self.iter[ticker_name] = 0

    def reset(self):
        for ticker_name in self.ticker_names:
            self.iter[ticker_name] = 0

already_downloaded = {}

def get_step_data(ticker_name, step):
    try:
        return already_downloaded[ticker_name][step]
    except:
        tick = yf.Ticker(ticker_name)
        df = tick.history('max')
        close_prices = df['Close'].values
        already_downloaded[ticker_name] = close_prices
        return already_downloaded[ticker_name][step]
