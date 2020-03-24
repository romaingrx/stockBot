#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Monday, 23 March 2020
"""

from typing import List, Text, Dict
import pandas as pd
import quandl

from stockBot.data.streamer import Streamer

class Quandl_Streamer(Streamer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_raw_DataFrames(self) -> Dict[Text, pd.DataFrame]:
        raise NotImplementedError("_get_raw_DataFrames not implemented")

    def _cast_raw_DataFrames(self, dataframes:Dict[Text, pd.DataFrame]) -> Dict[Text, pd.DataFrame]:
        """
            return a list of Dataframes with columns cast to raw_default_columns
        """
        raise NotImplementedError("_cast_raw_DataFrames not implemented")
