#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

from .ledger import Ledger

class Wallet:

    def __init__(self, initial_balance):
        self.initial_balance = initial_balance
        self.free_balance    = initial_balance
        self.locked_balance  = 0.0
        self.locked_transaction = []
        self._ledger = Ledger()

    def initial_balance(self):
        return self.initial_balance

    def balance(self):
        return self.balance

    def add(self, transaction:'Transaction'):
        self._ledger.push(transaction)

    def __str__(self):
        str  = 'Balance : \t%.2f \n'%self.balance()
        str += 'Locked balance : \t%.2f\n' %locked_balance
        str += str(self._ledger.as_frame())
