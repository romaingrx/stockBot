#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Monday, 23 March 2020
"""

from abc import abstractmethod, ABCMeta, ABC
from stockBot.data import features
from typing import List, Text, Dict
from collections import namedtuple
import sklearn.preprocessing
import pandas as pd
import functools

def MinMaxScaler(function):
    """
        Cast DataFrame values from 0 to 1
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        self = args[0]
        self.scalers = {ticker_name:sklearn.preprocessing.MinMaxScaler(feature_range=(0,1)) for ticker_name in self.ticker_names}
        dicDataFrames, dicPricesRows = function(*args, **kwargs)
        for ticker_name, df in dicDataFrames.items():
            dicDataFrames[ticker_name][df.columns] = self.scalers[ticker_name].fit_transform(df[df.columns])
        return dicDataFrames, dicPricesRows
    return wrapper

class Streamer(ABC):

    def __init__(self, ticker_names:List[Text] or Text, api_key:Text=None):
        self._raw_default_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.ticker_names = ticker_names
        self.DataFrames, self.prices_rows = self.get_DataFrames()


    @MinMaxScaler
    def get_DataFrames(self, fun='basic_features') -> Dict[Text, pd.DataFrame]:
        fun = getattr(features, fun)
        _raw_DataFrames = self._get_raw_DataFrames()
        _casted_raw_DataFrames = self._cast_raw_DataFrames(_raw_DataFrames)
        _added_features_DataFrames = {k:fun(v) for k, v in _casted_raw_DataFrames.items()}
        return _added_features_DataFrames, {ticker_name:_casted_raw_DataFrames[ticker_name]['Close'].copy() for ticker_name in self.ticker_names}

    @abstractmethod
    def _get_raw_DataFrames(self) -> Dict[Text, pd.DataFrame]:
        raise NotImplementedError("_get_raw_DataFrames not implemented")

    @abstractmethod
    def _cast_raw_DataFrames(self, dataframes:Dict[Text, pd.DataFrame]) -> Dict[Text, pd.DataFrame]:
        """
            return a list of Dataframes with columns cast to raw_default_columns
        """
        raise NotImplementedError("_cast_raw_DataFrames not implemented")
