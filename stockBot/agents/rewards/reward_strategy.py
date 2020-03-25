#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

from abc import ABC, abstractmethod
from stockBot.wallets import Wallet
import numpy as np

def reward_function(function):
    def wrapper(*args, **kwargs):
        return np.float32(function(*args, **kwargs))
    return wrapper

class Reward_Strategy(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_reward(self):
        raise NotImplementedError("get_reward not implemented")

class Simple_Reward_Strategy(Reward_Strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @reward_function
    def get_reward(self, wallet:Wallet) -> float:
        diff = wallet.balance - wallet.initial_balance
        reward = diff / wallet.initial_balance
        return reward

class Aggressive_Reward_Strategy(Reward_Strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_reward(self, wallet:Wallet) -> float:
        raise NotImplementedError("get_reward not implemented")
