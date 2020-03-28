#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 28 March 2020
"""

from .reward_strategy_base import Reward_Strategy
from stockBot.finance import Wallet

class Aggressive_Reward_Strategy(Reward_Strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_reward(self, wallet:Wallet) -> float:
        raise NotImplementedError("get_reward not implemented")
