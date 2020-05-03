#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

from abc import ABC, abstractmethod
from stockBot.finance import Wallet
import numpy as np

def reward_function(function):
    def wrapper(*args, **kwargs):
        return np.float32(function(*args, **kwargs))
    return wrapper

class Reward_Strategy(ABC):

    def __init__(self, history_capacity=30, **kwargs):
        self.history_capacity = history_capacity

    @property
    def history_capacity(self):
        return self._history_capacity

    @history_capacity.setter
    def history_capacity(self, value):
        assert value >= 0
        self._history_capacity = value

    @reward_function
    def get_reward(self, *args, **kwargs):
        return self._get_reward(*args, **kwargs)

    @abstractmethod
    def _get_reward(self):
        raise NotImplementedError("get_reward not implemented")

    @abstractmethod
    def reset(self):
        raise NotImplementedError("get_reward not implemented")
