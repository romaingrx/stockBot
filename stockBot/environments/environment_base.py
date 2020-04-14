#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Sunday, 22 March 2020
"""

import gym
import numpy as np
import pandas as pd
from typing import Text
from gym.spaces import Discrete, Box
import time

from .history import TimeSeries_History
from stockBot.brokers import Broker
from stockBot.data import Data_Streamer
from stockBot.data import Data_Streamer
from stockBot.finance import Wallet, Transaction
from stockBot.renderers import Renderer, File_Renderer, Naive_Plot
from stockBot.reward_strategies import Reward_Strategy, Simple_Reward_Strategy
from stockBot.action_strategies import Action_Strategy, Simple_Action_Strategy


class Environment(gym.Env):
    def __init__(self, data_streamer:Data_Streamer, broker:Broker=None, wallet:Wallet=None, action_strategy:Action_Strategy=None, reward_strategy:Reward_Strategy=None, renderer:Renderer=None, **kwargs):
        super().__init__()

        self.broker          = broker
        self.data_streamer   = data_streamer
        self.action_strategy = action_strategy or Simple_Action_Strategy()
        self.wallet          = wallet or self.broker.wallet
        self.reward_strategy = reward_strategy or Simple_Reward_Strategy()
        self.renderer        = renderer

        self.history_capacity = kwargs.get('history_capacity', 30)
        self.reward_strategy.history_capacity = self.history_capacity


        self._observation_low   = kwargs.get('obesrvations_lows', -np.iinfo(np.int32).max)
        self._observation_max   = kwargs.get('obesrvations_maxs', np.iinfo(np.int32).max)
        self._observation_shape = (self.history_capacity, self.data_streamer.n_features)
        self._observation_dtype = kwargs.get('obesrvations_lows', np.int32)

        self.observation_space  = Box(low   = self._observation_low,
                                      high  = self._observation_max,
                                      shape = self._observation_shape,
                                      dtype = self._observation_dtype
                                      )

        self._actions_low       = self.action_strategy.low
        self._actions_high      = self.action_strategy.high
        self._actions_shape     = self.action_strategy.shape
        self._n_actions         = self.action_strategy.n
        self._actions_dtype     = self.action_strategy.dtype

        self.box_action_space   = Box(low   = self._actions_low,
                                      high  = self._actions_high,
                                      shape = self._actions_shape,
                                      dtype = self._actions_dtype
                                      )
        self.action_space       = Discrete(self._n_actions)

        self.history = {ticker_name:TimeSeries_History(self.history_capacity) for ticker_name in self.data_streamer.ticker_names}

        self.iter    = {ticker_name:0 for ticker_name in self.data_streamer.ticker_names}

    def render(self):
        self.renderer.render(self.wallet)

    # TODO
    def step(self, action, ticker_name):
        date, row, price = self.data_streamer.next(ticker_name)

        self.history[ticker_name].push(row)

        order = self.action_strategy.get_order(action)

        if order:
            if order.value == 'buy':
                max_actions = np.floor(self.broker.wallet.balance/price)
            elif order.value == 'sell':
                max_actions = np.ceil(self.broker.wallet.locked_balance/price)
            transaction = Transaction(ticker_name, order, max(0, max_actions), price, 0.0)
            self.broker.commit_order(transaction)

        self.broker.update(ticker_name, date)
        self.iter[ticker_name] += 1

        state = self.history[ticker_name].get()

        reward = self.reward_strategy.get_reward(self.wallet)

        done = True if self.wallet.balance <= 0 or not self.data_streamer.has_next(ticker_name) else False

        info = {
            'wallet balance':self.broker.wallet.balance,
            'percentage locked balance':'%.2f'%(100*(self.broker.wallet.locked_balance/self.broker.wallet.balance)),
            'number of active tickers':len(self.broker.wallet._portfolio),
            'number of actions':self.broker.wallet._portfolio.get_quantity(ticker_name),
            'reward':reward
            }

        return state, reward, done, info


    def reset(self, ticker_name):
        self.history[ticker_name].reset()
        self.iter[ticker_name] = 0
        self.data_streamer.reset()
        self.wallet.reset()
        self.reward_strategy.reset()
        
        date, row, price = self.data_streamer.next(ticker_name)
        self.history[ticker_name].push(row)
        state = self.history[ticker_name].get()

        return state

    def __del__(self):
        del self.box_action_space
        del self.observation_space
        del self.action_space
        del self.iter
        del self.history
