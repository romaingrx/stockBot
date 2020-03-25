#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Friday, 03 February 2020
"""

from stockBot.agents import Agent
from stockBot.agents.models import Deep_Q_Learning
from stockBot.wallets import Transaction, Wallet, Portfolio
from stockBot.brokers import Fake_Broker
import numpy as np
import yfinance as yf
from stockBot.data import Data_Streamer, get_step_data
from stockBot.types import streamerSource, orderAction
from stockBot.environment import Environment

ticker = 'SPCE'
wallet = Wallet(1000)
# broker = Fake_Broker(wallet)
#
# for iter in range(10):
#     broker.update(ticker,iter)
#     print(broker.wallet)
#     if iter == 0:
#         transaction = Transaction(ticker, orderAction.BUY, 10, get_step_data(ticker, iter))
#         broker.commit_order(transaction)
#     if iter == 3:
#         transaction = Transaction(ticker, orderAction.SELL, 10, get_step_data(ticker, iter))
#         broker.commit_order(transaction)
#     if iter == 5:
#         transaction = Transaction(ticker, orderAction.BUY, 10, get_step_data(ticker, iter))
#         broker.commit_order(transaction)
#     if iter == 7:
#         transaction = Transaction(ticker, orderAction.BUY, 10, get_step_data(ticker, iter))
#         broker.commit_order(transaction)
#     if iter == 8:
#         transaction = Transaction(ticker, orderAction.SELL, 20, get_step_data(ticker, iter))
#         broker.commit_order(transaction)


broker = Fake_Broker(wallet)
agent = Agent(broker=broker)
agent.train()
