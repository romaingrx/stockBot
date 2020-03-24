#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Monday, 23 March 2020
"""

from abc import abstractmethod, ABCMeta, ABC
from typing import List, Text, Dict
import pandas as pd
from collections import namedtuple

class Streamer(ABC):

    def __init__(self, ticker_names:List[Text] or Text, api_key:Text=None):
        self._raw_default_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        self._api_key = api_key
        self.check_api_availability()
        self.ticker_names = ticker_names
        self.DataFrames = self.get_DataFrames()

    def check_api_availability(self):
        return

    def get_DataFrames(self) -> Dict[Text, pd.DataFrame]:
        _raw_DataFrames = self._get_raw_DataFrames()
        _casted_raw_DataFrames = self._cast_raw_DataFrames(_raw_DataFrames)
        return _casted_raw_DataFrames

    @abstractmethod
    def _get_raw_DataFrames(self) -> Dict[Text, pd.DataFrame]:
        raise NotImplementedError("_get_raw_DataFrames not implemented")

    @abstractmethod
    def _cast_raw_DataFrames(self, dataframes:Dict[Text, pd.DataFrame]) -> Dict[Text, pd.DataFrame]:
        """
            return a list of Dataframes with columns cast to raw_default_columns
        """
        raise NotImplementedError("_cast_raw_DataFrames not implemented")
