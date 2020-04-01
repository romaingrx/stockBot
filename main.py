#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Friday, 28 March 2020
"""

from stockBot.finance import Wallet
from stockBot.brokers import Fake_Broker
from stockBot.agents import DQNAgent
from stockBot.data import Data_Streamer
from stockBot.environments import Continuous_Environment

tickers = 'TSLA'
initial_balance = 1000

history_capacity = 30

agent = DQNAgent(tickers, initial_balance, load_name=None, random=False)
agent.train()
