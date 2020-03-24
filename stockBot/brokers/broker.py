#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Sunday, 22 March 2020
"""

from abc import abstractmethod
from stockBot.wallets import Transaction

class Broker:

    def __init__(self):
        pass

    @abstractmethod
    def buy(self, transaction:Transaction):
        raise NotImplementedError("buy not implemented")

    @abstractmethod
    def sell(self, transaction:Transaction):
        raise NotImplementedError("sell not implemented")
