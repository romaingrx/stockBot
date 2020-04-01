#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Monday, 30 March 2020
"""

import numpy as np
import pandas as pd

class TimeSeries_History(object):

    def __init__(self, length:int):
        self.length = length
        self.df = pd.DataFrame()

    def push(self, obs:dict):
        self.df = self.df.append(obs, ignore_index=True)

        if len(self.df) > self.length:
            self.df = self.df[-self.length:]

        self.df = self.df.fillna(0, axis=1)

    def get(self) -> np.array:
        array = np.zeros((self.length, self.df.shape[1]), dtype=float)
        array[:len(self.df)] = self.df.to_numpy(copy=True)
        return array


    def reset(self):
        del self.df
        self.df = pd.DataFrame()

    def __del__(self):
        del self.df
