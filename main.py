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
broker = Fake_Broker(wallet)

for iter in range(10):
    broker.update(ticker,iter)
    print(broker.wallet)
    if iter == 0:
        transaction = Transaction(ticker, orderAction.BUY, 10, get_step_data(ticker, iter))
        broker.commit_order(transaction)
    if iter == 3:
        transaction = Transaction(ticker, orderAction.SELL, 10, get_step_data(ticker, iter))
        broker.commit_order(transaction)
    if iter == 5:
        transaction = Transaction(ticker, orderAction.BUY, 10, get_step_data(ticker, iter))
        broker.commit_order(transaction)
    if iter == 7:
        transaction = Transaction(ticker, orderAction.BUY, 10, get_step_data(ticker, iter))
        broker.commit_order(transaction)
    if iter == 8:
        transaction = Transaction(ticker, orderAction.SELL, 20, get_step_data(ticker, iter))
        broker.commit_order(transaction)

#
# agent = Agent(wallet=wallet)
# agent.train()


# port.push()







#
# import subprocess, os, sys
# from settings import TENSORBOARDPATH
# import threading
# import shlex
#
# class tensorboard(threading.Thread):
#
#     def __init__(self):
#         self.thread = threading.Thread(target=self.run, args=())
#         self.thread.daemon = True
#         self.thread.start()
#         self.PIPE = subprocess.PIPE
#
#     def run(self):
#         self.process = subprocess.Popen(shlex.split(['tensorboard', '--logdir', TENSORBOARDPATH%'']), stdout=self.PIPE)
#         # stdout, stderr = process.communicate()
#         # for stdout in iter(process.stdout,''):
#         #     print(stdout)
#         # return stdout
#
# import mplfinance as mpf
# from model import ReinforcementNetwork
# import visualizer, evaluate, preprocess
# import yfinance as yf, numpy as np, matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MinMaxScaler
# from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
#
# if __name__=='__main__':
#     look_back = 10
#     features_col = []
#
#     input_shape = (1+len(features_col), look_back)
#     layer_size = 500
#
#     trader = ReinforcementNetwork(input_shape, layer_size)
#
#     TICK = yf.Ticker('TSLA')
#     df = TICK.history('max')
#     df = preprocess.df_preprocess_yfinance(df)
#     close = df['Close'].values
#
#     def get_state(data, t, n):
#         ret = np.zeros(n)
#         begining = t - n
#         if begining >= 0:
#             ret = data[begining:t]
#         elif t > 0:
#             ret[-begining:] = data[0:t]
#         return ret.reshape((1,-1))
#
#
#     state = get_state(close, 0, look_back)
#
#     initial_money = 10000
#     starting_money = initial_money
#     len_close = len(close) - 1
#     weight = trader
#     skip = 1
#     state = get_state(close, 0, look_back)
#     inventory = []
#     quantity = 0
#     max_buy = 5
#     max_sell = 5
#
#     max_for = 10
#     for t in range(0, max_for , skip):
#         action, buy = trader.act(state)
#         next_state = get_state(close, t + 1, look_back)
#         print('action : ', action)
#         if action == 1 and initial_money >= close[t]:
#             if buy < 0:
#                 buy = 1
#             if buy > max_buy:
#                 buy_units = max_buy
#             else:
#                 buy_units = buy
#             total_buy = buy_units * close[t]
#             initial_money -= total_buy
#             inventory.append(total_buy)
#             quantity += buy_units
#             # print('Bought')
#         elif action == 2 and len(inventory) > 0:
#             if quantity > max_sell:
#                 sell_units = max_sell
#             else:
#                 sell_units = quantity
#             quantity -= sell_units
#             total_sell = sell_units * close[t]
#             initial_money += total_sell
#             # print('Sold')
#             print("Money at step %d = %.2f"%(t, initial_money))
#         state = next_state
#     ((initial_money - starting_money) / starting_money) * 100
#     print(inventory)
