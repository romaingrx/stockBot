#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 29 March 2020
"""

import numpy as np

from .simple_reward_strategy import Simple_Reward_Strategy
from stockBot.finance import Wallet

class Sortino(Simple_Reward_Strategy):
    """
        Compute the sortino reward
        Link : https://www.daytrading.com/sortino-ratio
    """
    def __init__(self, history_capacity=30, target_returns=0, required_returns=0):
        super().__init__(history_capacity)
        self._target_returns = target_returns
        self._required_returns = required_returns

    def _get_reward(self, wallet:Wallet) -> float:
        self._push_balance_history(wallet.balance)
        if len(self._balance_history) == 1:
            return 0
        returns = self._balance_history.pct_change().dropna()

        downside_risk = returns.copy()
        downside_risk[returns < self._target_returns] = returns ** 2
        downside_risk = np.sqrt(np.std(downside_risk))

        expectation = np.mean(returns)

        reward = (expectation - self._required_returns + 1E-10)/(downside_risk + 1E-10)

        return float(reward) if not np.isnan(reward).any() else 0.0

    def reset(self):
        super().reset()
