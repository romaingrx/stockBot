#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Friday, 27 March 2020
"""

from __init__ import PROJECTPATH, sys
sys.path.append(PROJECTPATH)

from stockBot.brokers import Fake_Broker
from stockBot.finance import Wallet
from stockBot.data import Data_Streamer
from stockBot.environments import Environment

import unittest

class Environment_Test(unittest.TestCase):

    def test_capacity(self):
        ticker = 'SPCE'; initial_balance = 1000
        broker = Fake_Broker(Wallet(initial_balance))
        data_streamer = Data_Streamer(ticker)
        for history_capacity in [5, 10, 15, 20]:
            env = Environment(data_streamer, broker, history_capacity=history_capacity)
            state = env.reset(ticker)
            self.assertEqual(len(state), history_capacity)
            state = env.step(0, ticker)
            data_streamer.reset()
            del env
    def test_reset(self):
        tickers = ['SPCE', 'TSLA', 'AAPL']; initial_balance = 1000
        broker = Fake_Broker(Wallet(initial_balance))
        data_streamer = Data_Streamer(tickers)
        env = Environment(data_streamer, broker)
        for ticker_name in tickers:
            for i in range(10):
                state = env.step(2, ticker_name)
            env.reset(ticker_name)
            self.assertEqual(env.iter[ticker_name], 0)
        del data_streamer
        del env




if __name__=='__main__':
    unittest.main()
