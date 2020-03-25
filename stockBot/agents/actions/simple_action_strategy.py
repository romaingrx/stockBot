#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Wednesday, 25 March 2020
"""

from gym.spaces import Discrete
from typing import Text
import numpy as np

from .action_strategy_base import Action_Strategy
from stockBot.types import orderAction
from stockBot.wallets import Transaction
class Simple_Action_Strategy(Action_Strategy):

    def __init__(self):
        self.actions = [orderAction.BUY, orderAction.SELL, None]
        self.shape   = (len(self.actions),)
        self.dtype   = np.int32
        self.low     = 0
        self.high    = 2

    def get_order(self, action) -> orderAction:
        return self.actions[action]
