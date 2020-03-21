#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

from abc import abstractmethod

class reward_strategy:

    def __init__(self):
        return

    @abstractmethod
    def get_reward(self):
        raise NotImplementedError("get_reward not implemented")

def simple_reward_strategy(reward_strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_reward(self, portfolio) -> float:
        raise NotImplementedError("get_reward not implemented")

def aggressive_reward_strategy(reward_strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
