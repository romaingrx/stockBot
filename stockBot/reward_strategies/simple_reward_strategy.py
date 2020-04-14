#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 28 March 2020
"""
import pandas as pd
import numpy as np

from .reward_strategy_base import Reward_Strategy
from stockBot.finance import Wallet

class Simple_Reward_Strategy(Reward_Strategy):

    def __init__(self, history_capacity=2, **kwargs):
        super().__init__(history_capacity)
        self._balance_history = pd.DataFrame()

    def _push_balance_history(self, current_balance):
        self._balance_history = self._balance_history.append({'balance':current_balance}, ignore_index=True)
        self._balance_history = self._balance_history[-min(self._history_capacity, len(self._balance_history)):]
        self.df = self._balance_history.fillna(0, axis=1)

    def _get_reward(self, wallet:Wallet) -> float:
        self._push_balance_history(wallet.balance)

        returns = self._balance_history.pct_change().dropna() + 1
        arr = np.cumprod(returns.values) - 1

        reward = arr[-1] if len(arr) > 0 else 0

        return reward

    def reset(self):
        del self._balance_history
        self._balance_history = pd.DataFrame()
