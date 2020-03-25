#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Sunday, 22 March 2020
"""

from typing import Text
from stockBot.data import Data_Streamer
from stockBot.agents.rewards import Reward_Strategy, Simple_Reward_Strategy
from stockBot.agents.actions import Action_Strategy
from stockBot.environment.render import Renderer, File_Renderer
from stockBot.wallets import Wallet, Transaction
from stockBot.brokers import Broker

import gym
from gym.spaces import Discrete, Box
import pandas as pd
import numpy as np

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


class Environment(gym.Env):
    def __init__(self, broker:Broker, wallet:Wallet=None, action_strategy:Action_Strategy=None, data_streamer:Data_Streamer=None, reward_strategy:Reward_Strategy=None, **kwargs):
        super().__init__()

        self.broker          = broker
        self.action_strategy = action_strategy or Simple_Action_Strategy()
        self.wallet          = wallet or self.broker.wallet
        self.data_streamer   = data_streamer or Data_Streamer('SPCE')
        self.reward_strategy = reward_strategy or Simple_Reward_Strategy()

        self.look_back = kwargs.get('look_back', 5)

        self._observation_low   = kwargs.get('obesrvations_lows', -np.iinfo(np.int32).max)
        self._observation_max   = kwargs.get('obesrvations_maxs', np.iinfo(np.int32).max)
        self._observation_shape = (self.look_back, self.data_streamer.n_features)
        self._observation_dtype = kwargs.get('obesrvations_lows', np.int32)

        self.observation_space  = Box(low   = self._observation_low,
                                      high  = self._observation_max,
                                      shape = self._observation_shape,
                                      dtype = self._observation_dtype
                                      )

        self._actions_low       = self.action_strategy.low
        self._actions_high      = self.action_strategy.high
        self._actions_shape     = self.action_strategy.shape
        self._actions_dtype     = self.action_strategy.dtype

        self.action_space       = Box(low   = self._actions_low,
                                      high  = self._actions_high,
                                      shape = self._actions_shape,
                                      dtype = self._actions_dtype
                                      )

        self.history = {ticker_name:TimeSeries_History(self.look_back) for ticker_name in self.data_streamer.ticker_names}

        self.iter    = {ticker_name:i for ticker_name, i in zip(self.data_streamer.ticker_names, [0]*len(self.data_streamer.ticker_names))}

    # TODO
    def render(self, episode):
        raise NotImplementedError()

    # TODO
    def step(self, action, ticker_name):
        row, price = self.data_streamer.next(ticker_name)

        self.history[ticker_name].push(row)
        self.iter[ticker_name] += 1

        order = self.action_strategy.get_order(action)

        self.broker.update(ticker_name, self.iter[ticker_name])
        if order:
            transaction = Transaction(ticker_name, order, 10, price, 0.0)
            self.broker.commit_order(transaction)

        state = self.history[ticker_name].get()

        reward = self.reward_strategy.get_reward(self.wallet)

        done = True if self.wallet.balance <= 0 or not self.data_streamer.has_next(ticker_name) else False

        info = {
            'bite':'oui'
        }

        return state, reward, done, info


    def reset(self, ticker_name):
        self.history[ticker_name].reset()
        self.iter[ticker_name] = 0
        self.data_streamer.reset()

        row, price = self.data_streamer.next(ticker_name)
        self.history[ticker_name].push(row)
        state = self.history[ticker_name].get()

        return state
