#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Tuesday, 24 March 2020
"""


from abc import ABC, abstractmethod

from stockBot.wallets import Wallet

class Renderer(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def render(self, episode:int=None, wallet:Wallet=None):
        raise NotImplementedError()
    @abstractmethod
    def reset(self):
        pass
