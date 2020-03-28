#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Tuesday, 24 March 2020
"""

from stockBot.brokers import Broker
from stockBot.finance import Transaction

class Bolero(Broker):

    def __init__(self):
        pass

    def buy(self, transaction:Transaction):
        raise NotImplementedError("buy not implemented")

    def sell(self, transaction:Transaction):
        raise NotImplementedError("sell not implemented")
