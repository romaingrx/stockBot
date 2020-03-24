#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

# WALLET DOIT CONTENIR TOUTES LES INFORMATIONS LIÉES Á L'HISTORIQUE DES TRANSACTIONS, LES ACTIONS DÉTENUES, LES DIFFÉRENTES BALANCES ET SURTOUT LA BALANCE POTENTIELLE

from .portfolio import Portfolio
from .ledger import Ledger
from .transactions import Transaction

from stockBot.exceptions import NotEnoughBalanceError
from stockBot.types import orderAction

class Wallet:

    def __init__(self, initial_balance):
        # TODO: Ajouter des attributs cohérents pour contenir toutes les informations nécessaires
        self.initial_balance = initial_balance
        self.balance         = initial_balance
        self.free_balance    = initial_balance
        self.locked_balance  = 0.0
        self._ledger = Ledger()
        self._portfolio = Portfolio()


    # TODO: ajoute la transaction dans _portfolio et _ledger et met ensuite à jour les balances
    def push(self, transaction:'Transaction'):
        assert isinstance(transaction, Transaction)
        if transaction.action is orderAction.BUY.value and transaction.amount > self.free_balance:
            raise NotEnoughBalanceError()

        self.free_balance += transaction.amount if transaction.action == orderAction.SELL.value else -transaction.amount

        self._portfolio.push(transaction)
        self._ledger.push(transaction)
        self.update()

    # TODO: met à jour toutes les balances en fonction du _portfolio
    def update(self):
        self.balance = self.free_balance + self._portfolio.current_balance
        self.locked_balance = self._portfolio.current_balance

    # TODO: représentation texte du Wallet
    def __str__(self):
        string  = 'Potential Balance : \t%.2f\n'%self.potential_balance
        string += 'Free balance : \t\t%.2f\n' %self.free_balance
        string += 'Locked balance : \t%.2f\n' %self.locked_balance
        string += str(self._ledger)
        return string

    # TODO: Met le Wallet comme initialement (initial balance)
    def reset(self):
            self._ledger.reset()
            self._portfolio.reset()
            self.free_balance = self.initial_balance
            self.locked_balance = 0.0
