#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

from typing import Optional, Text, Tuple, Dict
from stockBot.types import orderAction
from stockBot.exceptions import OrderActionError
import datetime

class Transaction:

    def __init__(self, ticker_name:Text, action:Text or orderAction, quantity:int, price:float, fees:float, amount:Optional=None, date:datetime=datetime.datetime.now()):
        if not isinstance(action, orderAction):
            if not action in orderAction.values():
                raise OrderActionError(action)
        self.action      = action if not isinstance(action, orderAction) else action.value
        self.ticker_name = ticker_name
        self.quantity    = quantity
        self.price       = price
        self.fees        = fees
        self.amount      = amount if amount else self.price * self.quantity
        self.date = date

    def as_dict(self) -> dict:
        return dict({'action':self.action, 'ticker_name':self.ticker_name, 'quantity':self.quantity, 'price':self.price, 'fees':self.fees, 'amount':self.amount})

    def __str__(self):
        return str(self.as_dict())
