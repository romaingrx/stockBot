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

    def test_ticker_reset(self):
        tickers = ['SPCE', 'TSLA']
        data_streamer = Data_Streamer(tickers)
        for mult, ticker_name in enumerate(tickers):
            mult += 1
            for _ in range(mult*5):
                args = data_streamer.next(ticker_name)
                self.assertNotEqual(data_streamer.iter[ticker_name], 0)
            data_streamer.reset_ticker(ticker_name)
            self.assertEqual(data_streamer.iter[ticker_name], 0)


    def test_hard_reset(self):
        tickers = ['SPCE', 'TSLA']
        data_streamer = Data_Streamer(tickers)
        for mult, ticker_name in enumerate(tickers):
            mult += 1
            for _ in range(mult*5):
                args = data_streamer.next(ticker_name)
                self.assertNotEqual(data_streamer.iter[ticker_name], 0)
        data_streamer.reset()
        for ticker_name in tickers:
            self.assertEqual(data_streamer.iter[ticker_name], 0)

if __name__=='__main__':
    unittest.main()
