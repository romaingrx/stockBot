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

    def __init__(self):
        pass

    @reward_function
    def get_reward(self, *args, **kwargs):
        return self._get_reward(*args, **kwargs)
    @abstractmethod
    def _get_reward(self):
        raise NotImplementedError("get_reward not implemented")
