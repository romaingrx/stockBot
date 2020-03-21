#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

from typing import Optional, Text, Tuple, Dict

default_dict = dict({'ticker_name':None, 'action':None, 'quantity':None, 'price':None, 'quantity':None, 'fees':None, 'amount':None})

class Transaction:

    def __init__(self, ticker_name:Text, action:Text, quantity, price, fees, amount:Optional=None):
        self.action      = action
        self.ticker_name = ticker_name
        self.quantity    = quantity
        self.price       = price
        self.fees        = fees
        self.amount      = amount if amount else self.price * self.quantity

    def as_dict(self) -> dict:
        return dict({'action':self.action, 'ticker_name':self.ticker_name, 'quantity':self.quantity, 'price':self.price, 'fees':self.fees, 'amount':self.amount})

    def __str__(self):
        return str(self.as_dict())
