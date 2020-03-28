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

ticker = 'SPCE'
initial_balance = 1000

agent = DQNAgent(ticker, initial_balance)
agent.train()
