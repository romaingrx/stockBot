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
    def commit_order(self, transaction:Transaction):
        raise NotImplementedError("commit_order not implemented")

    @abstractmethod
    def buy(self, transaction:Transaction):
        raise NotImplementedError("buy not implemented")

    @abstractmethod
    def sell(self, transaction:Transaction):
        raise NotImplementedError("sell not implemented")

    @abstractmethod
    def _real_buy_send(self, transaction:Transaction):
        """
            WARNING: IT MANAGES YOUR REAL WALLET ON YOUR ONLINE BROKER
        """
        raise NotImplementedError("_real_buy_send not implemented")

    @abstractmethod
    def _real_sell_send(self, transaction:Transaction):
        """
            WARNING: IT MANAGES YOUR REAL WALLET ON YOUR ONLINE BROKER
        """
        raise NotImplementedError("_real_sell_send not implemented")
