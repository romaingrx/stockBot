#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Sunday, 22 March 2020
"""

from stockBot.data.preprocess import df_preprocess_yfinance
from stockBot.data.streamer import streamer_mapper, yfinance, alpha_vantage, quandl

from abc import abstractmethod
from typing import List, Text
import numpy as np
import yfinance as yf

from stockBot.types import streamerSource
from stockBot.exceptions import StreamerSourceError


class Data_Streamer:

    def __init__(self, tickers:List[Text] or Text, src:streamerSource or Text=streamerSource.YFINANCE, api_key:Text=None):
        self._api_key = api_key
        if not isinstance(src, streamerSource) and not src in streamerSource.values():
            raise StreamerSourceError(src)
        self.src = src.value if isinstance(src, streamerSource) else src
        self.ticker_names = tickers if isinstance(tickers, list) else [tickers]
        self.Streamer = streamer_mapper[self.src](self.ticker_names, self._api_key)
        self.DataFrames = self.Streamer.DataFrames
        self.n_features = self.DataFrames[self.ticker_names[0]].shape[1]
        self.iter = 0

    def has_next(self, ticker_name):
        return True if self.iter<len(self.DataFrames[ticker_name]) else False

    def next(self, ticker_name):
        if not self.has_next(ticker_name):
            raise IndexError()
        row = self.DataFrames[ticker_name].iloc[self.iter]
        self.iter += 1
        return row, row['Close']

    def reset(self):
        self.iter = 0

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
