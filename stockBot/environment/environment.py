#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Sunday, 22 March 2020
"""

from typing import Text
from stockBot.data import Data_Streamer
from stockBot.agents.rewards import Reward_Strategy, Simple_Reward_Strategy
from stockBot.environment.render import Renderer, File_Renderer
from stockBot.wallets import Wallet

import gym
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
    def __init__(self, wallet:Wallet=None, data_streamer:Data_Streamer=None, reward_strategy:Reward_Strategy=None, **kwargs):
        super().__init__()

        self.wallet = wallet
        self.data_streamer = data_streamer or Data_Streamer('SPCE')
        self.reward_strategy = reward_strategy or Simple_Reward_Strategy()
        self.look_back = kwargs.get('look_back', 5)

        self.history = TimeSeries_History(self.look_back)

        self.iter = 0

        self.observation_shape = self.reset().shape


    # TODO
    def render(self, episode):
        raise NotImplementedError()

    # TODO
    def step(self):
        self.history.push(self.data_streamer.next('SPCE'))

        obs = self.history.get()

        reward = self.reward_strategy.get_reward(self.wallet)

        done = True if self.wallet.balance <= 0 or not self.data_streamer.has_next('SPCE') else False

        info = {
            'bite':'oui'
        }

        return obs, reward, done, info


    def reset(self):
        self.history.reset()
        self.data_streamer.reset()

        self.history.push(self.data_streamer.next('SPCE'))

        obs = self.history.get()

        return obs
