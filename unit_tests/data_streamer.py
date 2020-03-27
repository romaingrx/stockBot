#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Friday, 27 March 2020
"""

import sys
sys.path.append('../stockBot')

import unittest

from stockBot.data import Data_Streamer

class Data_Streamer_Test(unittest.TestCase):

    def test_has_next(self):
        tickers = ['SPCE', 'TSLA']
        data_streamer = Data_Streamer(tickers)
        for ticker in tickers:
            self.assertTrue(data_streamer.has_next(ticker))


    def test_reset(self):
        tickers = ['SPCE']
        data_streamer = Data_Streamer(tickers)
