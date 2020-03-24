#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Monday, 23 March 2020
"""

from typing import List, Text, Dict

from stockBot.data.streamer import Streamer
import yfinance as yf
import pandas as pd


class Yfinance_Streamer(Streamer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_raw_DataFrames(self) -> Dict[Text, pd.DataFrame]:
            self.tickers = dict(map(lambda ticker_names : (str(ticker_names), yf.Ticker(ticker_names)), self.ticker_names))
            raw_dataframes = {ticker_name: ticker.history('max') for ticker_name, ticker in self.tickers.items()}
            return raw_dataframes

    def _cast_raw_DataFrames(self, dataframes:Dict[Text, pd.DataFrame]) -> Dict[Text, pd.DataFrame]:
        casted_dataframes = {ticker_name: df[self._raw_default_columns] for ticker_name, df in dataframes.items()}
        return casted_dataframes
