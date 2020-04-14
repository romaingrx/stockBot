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

import numpy as np

tickers = 'TSLA'
initial_balance = 10000

history_capacity = 30

agent = DQNAgent(tickers, initial_balance, random=False, features_function='stat')
agent.train(epochs=20)
# model = agent.neural_network.model
# for i in range(10):
#     state=np.random.rand(1,30,14)
#     print(model.predict(state))
# agent.simulate()
